import { useEffect, useRef, useState } from "react";
import api from "../api";

/*
 * Module 1: AI Gym Trainer (Workout Detection & Feedback System)
 *
 * Runs MediaPipe Pose fully client-side on the webcam feed. For each frame we
 * compute the relevant joint angle (knee angle for squats/lunges, elbow angle
 * for pushups/curls/presses) and run a small state machine that only counts a
 * rep once the joint has actually crossed into - and back out of - the target
 * range of motion. That gives real, pose-driven rep counting and lets us
 * capture the angle reached at the peak of every single rep, which is what
 * the backend uses for form scoring (Module 6: Pose-to-Performance Analyzer).
 */

// landmark indices = [proximal, joint, distal], e.g. hip-knee-ankle
const EXERCISE_CONFIG = {
  squat: { label: "Squat", landmarks: [24, 26, 28], direction: "flex", enter: 140, exit: 150 },
  pushup: { label: "Push-up", landmarks: [12, 14, 16], direction: "flex", enter: 140, exit: 150 },
  bicep_curl: { label: "Bicep Curl", landmarks: [12, 14, 16], direction: "flex", enter: 110, exit: 120 },
  lunge: { label: "Lunge", landmarks: [24, 26, 28], direction: "flex", enter: 140, exit: 150 },
  shoulder_press: { label: "Shoulder Press", landmarks: [12, 14, 16], direction: "extend", enter: 140, exit: 130 },
};

function angleBetween(a, b, c) {
  const ab = { x: a.x - b.x, y: a.y - b.y };
  const cb = { x: c.x - b.x, y: c.y - b.y };
  const dot = ab.x * cb.x + ab.y * cb.y;
  const magAb = Math.hypot(ab.x, ab.y);
  const magCb = Math.hypot(cb.x, cb.y);
  if (magAb === 0 || magCb === 0) return 180;
  const cos = Math.min(1, Math.max(-1, dot / (magAb * magCb)));
  return (Math.acos(cos) * 180) / Math.PI;
}

export default function Workout() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const poseRef = useRef(null);
  const cameraRef = useRef(null);

  const [exercise, setExercise] = useState("squat");
  const exerciseRef = useRef(exercise);
  const [running, setRunning] = useState(false);
  const [repCount, setRepCount] = useState(0);
  const [currentAngle, setCurrentAngle] = useState(null);
  const [visibilityWarning, setVisibilityWarning] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [sdkReady, setSdkReady] = useState(true);

  const repsRef = useRef([]);
  const phaseRef = useRef("rest");
  const peakAngleRef = useRef(null);
  const startTimeRef = useRef(null);
  const lowVisFramesRef = useRef(0);

  useEffect(() => {
    exerciseRef.current = exercise;
    resetSession();
  }, [exercise]);

  const resetSession = () => {
    repsRef.current = [];
    phaseRef.current = "rest";
    peakAngleRef.current = null;
    setRepCount(0);
    setResult(null);
  };

  const onResults = (results) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    canvas.width = results.image.width;
    canvas.height = results.image.height;
    ctx.save();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(results.image, 0, 0, canvas.width, canvas.height);

    if (results.poseLandmarks) {
      if (window.drawConnectors && window.POSE_CONNECTIONS) {
        window.drawConnectors(ctx, results.poseLandmarks, window.POSE_CONNECTIONS, { color: "#22c55e", lineWidth: 3 });
        window.drawLandmarks(ctx, results.poseLandmarks, { color: "#f97316", radius: 3 });
      }

      const cfg = EXERCISE_CONFIG[exerciseRef.current];
      const [ia, ib, ic] = cfg.landmarks;
      const a = results.poseLandmarks[ia];
      const b = results.poseLandmarks[ib];
      const c = results.poseLandmarks[ic];

      const minVisibility = Math.min(a.visibility ?? 1, b.visibility ?? 1, c.visibility ?? 1);
      if (minVisibility < 0.5) {
        lowVisFramesRef.current += 1;
        setVisibilityWarning(lowVisFramesRef.current > 15);
      } else {
        lowVisFramesRef.current = 0;
        setVisibilityWarning(false);
      }

      const angle = angleBetween(a, b, c);
      setCurrentAngle(Math.round(angle));
      runRepStateMachine(angle, cfg);
    }
    ctx.restore();
  };

  const runRepStateMachine = (angle, cfg) => {
    if (cfg.direction === "flex") {
      if (angle < cfg.enter) {
        phaseRef.current = "down";
        peakAngleRef.current = peakAngleRef.current === null ? angle : Math.min(peakAngleRef.current, angle);
      } else if (angle > cfg.exit && phaseRef.current === "down") {
        completeRep(peakAngleRef.current);
      }
    } else {
      if (angle > cfg.enter) {
        phaseRef.current = "up";
        peakAngleRef.current = peakAngleRef.current === null ? angle : Math.max(peakAngleRef.current, angle);
      } else if (angle < cfg.exit && phaseRef.current === "up") {
        completeRep(peakAngleRef.current);
      }
    }
  };

  const completeRep = (peakAngle) => {
    repsRef.current.push({
      exercise: exerciseRef.current,
      joint_angle: peakAngle,
      timestamp: new Date().toISOString(),
    });
    setRepCount(repsRef.current.length);
    phaseRef.current = "rest";
    peakAngleRef.current = null;
  };

  const startCamera = async () => {
    if (!window.Pose || !window.Camera) {
      setSdkReady(false);
      return;
    }
    resetSession();
    startTimeRef.current = Date.now();

    const pose = new window.Pose({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose@0.5.1675469404/${file}`,
    });
    pose.setOptions({
      modelComplexity: 1,
      smoothLandmarks: true,
      minDetectionConfidence: 0.6,
      minTrackingConfidence: 0.6,
    });
    pose.onResults(onResults);
    poseRef.current = pose;

    const camera = new window.Camera(videoRef.current, {
      onFrame: async () => {
        await pose.send({ image: videoRef.current });
      },
      width: 640,
      height: 480,
    });
    cameraRef.current = camera;
    camera.start();
    setRunning(true);
  };

  const stopCameraAndSubmit = async () => {
    cameraRef.current?.stop();
    setRunning(false);

    const durationSeconds = (Date.now() - startTimeRef.current) / 1000;
    const formIssues = [];
    if (repsRef.current.length === 0) {
      formIssues.push("no valid reps detected - make sure your full body is visible and try again");
    }

    setLoading(true);
    try {
      const res = await api.post("/workout/session", {
        exercise: exerciseRef.current,
        reps: repsRef.current,
        duration_seconds: durationSeconds,
        form_issues: formIssues,
      });
      setResult(res.data);
    } catch (err) {
      setResult({ error: err.response?.data?.detail || "Failed to save session" });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    return () => cameraRef.current?.stop();
  }, []);

  return (
    <div className="page">
      {/* Top Day Tabs */}
      <div style={{ display: "flex", gap: "2rem", alignItems: "center", borderBottom: "1px solid #F1F4F9", paddingBottom: "1rem", marginBottom: "1.5rem" }}>
        <div style={{ fontWeight: 800, fontSize: "1.15rem", color: "#111827", display: "flex", alignItems: "center", gap: "6px" }}>
          <span>•</span> Day 1 👶
        </div>
        <div style={{ fontWeight: 600, fontSize: "1.15rem", color: "#94A3B8" }}>Day 2</div>
        <div style={{ fontWeight: 600, fontSize: "1.15rem", color: "#94A3B8" }}>Day 3</div>
        <div style={{ fontWeight: 600, fontSize: "1.15rem", color: "#94A3B8" }}>Day 4</div>
      </div>

      {!sdkReady && (
        <p className="error">
          MediaPipe scripts failed to load (check your internet connection - they load from a CDN).
        </p>
      )}

      {/* Main 2-Column Pinterest Grid */}
      <div style={{ display: "grid", gridTemplateColumns: "1.75fr 1fr", gap: "1.5rem", marginBottom: "2rem" }}>
        {/* Left Column */}
        <div>
          {/* Hero Player Card */}
          <div style={{
            background: "linear-gradient(135deg, #CFDEEB 0%, #DCE8F2 100%)",
            borderRadius: "28px",
            padding: "1.5rem 1.8rem",
            position: "relative",
            boxShadow: "0 10px 30px rgba(18, 38, 63, 0.05)",
            marginBottom: "1rem"
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
              <div>
                <div style={{ fontSize: "1.35rem", fontWeight: 800, color: "#111827" }}>Exercise: {EXERCISE_CONFIG[exercise].label}</div>
                <div style={{ fontSize: "0.9rem", color: "#64748B", fontWeight: 500 }}>Target: Abdominal muscles & form accuracy</div>
              </div>
              <div style={{
                width: "44px", height: "44px", borderRadius: "14px", background: "#FF4757", color: "#FFF",
                display: "flex", alignItems: "center", justifyContent: "center", fontSize: "1.2rem",
                boxShadow: "0 4px 14px rgba(255, 71, 87, 0.35)"
              }}>
                ❤️
              </div>
            </div>

            <div className="workout-controls" style={{ marginBottom: "1rem" }}>
              <label style={{ fontWeight: 700, fontSize: "0.9rem", color: "#1E293B" }}>
                Movement:{" "}
                <select value={exercise} onChange={(e) => setExercise(e.target.value)} disabled={running} style={{ maxWidth: "220px", display: "inline-block", marginLeft: "8px" }}>
                  {Object.entries(EXERCISE_CONFIG).map(([key, cfg]) => (
                    <option key={key} value={key}>{cfg.label}</option>
                  ))}
                </select>
              </label>
              {!running ? (
                <button onClick={startCamera}>Start Session</button>
              ) : (
                <button onClick={stopCameraAndSubmit} style={{ background: "#0F172A" }}>Stop & Save Session</button>
              )}
            </div>

            <div className="video-wrap" style={{ width: "100%", textAlign: "center" }}>
              <video ref={videoRef} style={{ display: "none" }} playsInline />
              <canvas ref={canvasRef} className="pose-canvas" style={{ width: "100%", maxHeight: "360px", objectFit: "contain", borderRadius: "20px" }} />
            </div>

            <div className="live-stats" style={{ justifyContent: "space-between", background: "rgba(255, 255, 255, 0.7)", padding: "0.75rem 1.2rem", borderRadius: "16px", marginTop: "1rem" }}>
              <span style={{ color: "#111827" }}>Live Reps: <strong style={{ fontSize: "1.2rem", color: "#FF5B26" }}>{repCount}</strong></span>
              <span style={{ color: "#111827" }}>Joint Angle: <strong style={{ fontSize: "1.2rem", color: "#111827" }}>{currentAngle ?? "-"}°</strong></span>
              {visibilityWarning && <span className="warn" style={{ color: "#D97706", fontWeight: "bold" }}>⚠ Step back for full visibility</span>}
            </div>
          </div>

          {/* 4 Metric Pills */}
          <div style={{
            display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "0.8rem",
            background: "#FFFFFF", border: "1px solid #EEF2F6", borderRadius: "22px",
            padding: "1rem 1.2rem", boxShadow: "0 4px 16px rgba(0,0,0,0.02)", marginBottom: "1.2rem"
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <div style={{ width: "38px", height: "38px", borderRadius: "12px", background: "#FEF3C7", color: "#D97706", display: "flex", alignItems: "center", justifyContent: "center" }}>🏃</div>
              <div>
                <div style={{ fontWeight: 800, fontSize: "0.95rem", color: "#111827" }}>{EXERCISE_CONFIG[exercise].label}</div>
                <div style={{ fontSize: "0.68rem", fontWeight: 700, color: "#94A3B8", textTransform: "uppercase" }}>EXERCISE</div>
              </div>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <div style={{ width: "38px", height: "38px", borderRadius: "12px", background: "#EDE9FE", color: "#7C3AED", display: "flex", alignItems: "center", justifyContent: "center" }}>⭐</div>
              <div>
                <div style={{ fontWeight: 800, fontSize: "0.95rem", color: "#111827" }}>2</div>
                <div style={{ fontSize: "0.68rem", fontWeight: 700, color: "#94A3B8", textTransform: "uppercase" }}>DIFFICULT</div>
              </div>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <div style={{ width: "38px", height: "38px", borderRadius: "12px", background: "#DCFCE7", color: "#059669", display: "flex", alignItems: "center", justifyContent: "center" }}>⏱️</div>
              <div>
                <div style={{ fontWeight: 800, fontSize: "0.95rem", color: "#111827" }}>Live</div>
                <div style={{ fontSize: "0.68rem", fontWeight: 700, color: "#94A3B8", textTransform: "uppercase" }}>TOTAL TIME</div>
              </div>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <div style={{ width: "38px", height: "38px", borderRadius: "12px", background: "#FCE7F3", color: "#DB2777", display: "flex", alignItems: "center", justifyContent: "center" }}>⏳</div>
              <div>
                <div style={{ fontWeight: 800, fontSize: "0.95rem", color: "#111827" }}>Active</div>
                <div style={{ fontSize: "0.68rem", fontWeight: 700, color: "#94A3B8", textTransform: "uppercase" }}>REAL TIME</div>
              </div>
            </div>
          </div>

          {/* Description Card */}
          <div style={{ background: "#FFFFFF", border: "1px solid #EEF2F6", borderRadius: "24px", padding: "1.4rem", boxShadow: "0 4px 20px rgba(0,0,0,0.03)" }}>
            <div style={{ fontSize: "0.8rem", fontWeight: 800, color: "#64748B", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: "1rem" }}>
              DESCRIPTION
            </div>
            <div style={{ display: "flex", gap: "14px", marginBottom: "1rem" }}>
              <div style={{ width: "30px", height: "30px", borderRadius: "50%", background: "#0F172A", color: "white", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 800, fontSize: "0.85rem" }}>1</div>
              <div>
                <div style={{ fontWeight: 700, fontSize: "0.95rem", color: "#111827" }}>Start point:</div>
                <div style={{ fontSize: "0.9rem", color: "#64748B" }}>Adopt proper starting posture with neutral spine and core engaged.</div>
              </div>
            </div>
            <div style={{ display: "flex", gap: "14px" }}>
              <div style={{ width: "30px", height: "30px", borderRadius: "50%", background: "#0F172A", color: "white", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 800, fontSize: "0.85rem" }}>2</div>
              <div>
                <div style={{ fontWeight: 700, fontSize: "0.95rem", color: "#111827" }}>Actions:</div>
                <div style={{ fontSize: "0.9rem", color: "#64748B" }}>Perform the movement with smooth, controlled cadence and complete range of motion.</div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div>
          {/* Exercises Card */}
          <div style={{ background: "#FFFFFF", border: "1px solid #EEF2F6", borderRadius: "24px", padding: "1.4rem", boxShadow: "0 4px 20px rgba(0,0,0,0.03)" }}>
            <div style={{ fontSize: "0.8rem", fontWeight: 800, color: "#64748B", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: "1rem" }}>
              EXERCISES
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
              {[
                { title: "Abdominal muscles", time: "10 mins", cal: "40Kcal", status: "progress", bg: "#CFDEEB", icon: "🧘" },
                { title: "Jumping on ball", time: "15 mins", cal: "90Kcal", status: "completed", bg: "#EDE9FE", icon: "🔵" },
                { title: "With dumbbells", time: "10 mins", cal: "50Kcal", status: "completed", bg: "#BAE6FD", icon: "🏋️" },
                { title: "Jumping", time: "10 mins", cal: "110Kcal", status: "missed", bg: "#FCE7F3", icon: "🏃" },
              ].map((ex) => (
                <div key={ex.title} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", paddingBottom: "0.6rem", borderBottom: "1px solid #F1F5F9" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                    <div style={{ width: "46px", height: "38px", borderRadius: "12px", background: ex.bg, display: "flex", alignItems: "center", justifyContent: "center", fontSize: "1.2rem" }}>{ex.icon}</div>
                    <div>
                      <div style={{ fontWeight: 700, fontSize: "0.9rem", color: "#111827" }}>{ex.title}</div>
                      <div style={{ fontSize: "0.78rem", color: "#64748B" }}>⏱️ {ex.time} · ⚡ {ex.cal}</div>
                    </div>
                  </div>
                  {ex.status === "completed" ? (
                    <div style={{ width: "22px", height: "22px", borderRadius: "50%", background: "#10B981", color: "white", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "0.75rem", fontWeight: "bold" }}>✓</div>
                  ) : ex.status === "progress" ? (
                    <div style={{ width: "22px", height: "22px", borderRadius: "50%", border: "2.5px solid #FF5B26", borderTopColor: "transparent" }}></div>
                  ) : (
                    <div style={{ width: "22px", height: "22px", borderRadius: "50%", background: "#EF4444", color: "white", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "0.75rem", fontWeight: "bold" }}>✕</div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Level & Friends Card */}
          <div style={{ background: "linear-gradient(135deg, #F3E8FF 0%, #FBEBFE 100%)", borderRadius: "24px", padding: "1.4rem", marginTop: "1.2rem", boxShadow: "0 4px 20px rgba(124, 58, 237, 0.06)" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                <div style={{ width: "38px", height: "38px", borderRadius: "50%", background: "#FFFFFF", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "1.1rem" }}>👶</div>
                <div>
                  <div style={{ fontSize: "0.95rem", fontWeight: 800, color: "#1E1B4B" }}>BEGINNER</div>
                  <div style={{ fontSize: "0.7rem", fontWeight: 700, color: "#6B7280" }}>YOUR LEVEL</div>
                </div>
              </div>
              <div style={{ fontWeight: 800, fontSize: "1.1rem", color: "#1E1B4B" }}>🏋️ 1021</div>
            </div>
            <div>
              <div style={{ fontSize: "0.75rem", fontWeight: 800, color: "#6B7280", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: "0.5rem" }}>MY FRIENDS</div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <div style={{ display: "flex", alignItems: "center" }}>
                  <div style={{ width: "32px", height: "32px", borderRadius: "50%", background: "#FED7AA", border: "2px solid #FFF", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "0.85rem", marginRight: "-8px" }}>👱‍♀️</div>
                  <div style={{ width: "32px", height: "32px", borderRadius: "50%", background: "#BAE6FD", border: "2px solid #FFF", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "0.85rem", marginRight: "-8px" }}>👨‍🦱</div>
                  <div style={{ width: "32px", height: "32px", borderRadius: "50%", background: "#FECDD3", border: "2px solid #FFF", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "0.85rem", marginRight: "-8px" }}>👩‍🦰</div>
                  <div style={{ width: "32px", height: "32px", borderRadius: "50%", background: "#DDD6FE", border: "2px solid #FFF", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "0.75rem", fontWeight: 700, color: "#5B21B6", marginRight: "8px" }}>+10</div>
                </div>
                <div style={{ width: "36px", height: "36px", borderRadius: "12px", background: "#FF5B26", color: "white", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "1rem", boxShadow: "0 4px 12px rgba(255, 91, 38, 0.35)", cursor: "pointer" }}>🎁</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {loading && <p>Analyzing session…</p>}

      {result && !result.error && (
        <div className="result-card">
          <h3 style={{ fontSize: "1.2rem", fontWeight: 800, color: "#111827", marginBottom: "0.8rem" }}>🎉 Session Result</h3>
          <p>Valid reps counted: <strong style={{ color: "#FF5B26", fontSize: "1.2rem" }}>{result.rep_count}</strong></p>
          <p>Form score: <strong>{result.form_score}/100</strong></p>
          <p>Tempo consistency: <strong>{result.tempo_consistency}/100</strong></p>
          <ul style={{ marginTop: "0.5rem" }}>
            {result.feedback.map((f, i) => <li key={i} style={{ color: "#475569", margin: "4px 0" }}>{f}</li>)}
          </ul>
        </div>
      )}
      {result?.error && <p className="error">{result.error}</p>}
    </div>
  );
}
