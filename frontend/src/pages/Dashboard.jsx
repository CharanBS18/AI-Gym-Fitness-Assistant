import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const modules = [
  { to: "/workout", title: "🏋️ AI Gym Trainer", desc: "Webcam pose detection, rep counting & real-time form feedback." },
  { to: "/diet", title: "🥗 AI Dietician & Calorie Coach", desc: "BMI, BMR, macros, meal plan & grocery list." },
  { to: "/smart-gym", title: "📡 Smart Gym Assistant (AI + IoT)", desc: "Simulated sensor feed drives resistance & rest recommendations." },
  { to: "/habit", title: "🔥 AI Fitness Habit Tracker", desc: "Skip-risk prediction, streaks & motivational nudges." },
  { to: "/chat", title: "💬 Virtual Gym Buddy", desc: "Mood-aware AI chat companion." },
  { to: "/performance", title: "📈 Pose-to-Performance Analyzer", desc: "Weekly performance score & trend from your sessions." },
  { to: "/gyms", title: "📍 Gym Recommender & Planner", desc: "Nearby gyms matched to your goal." },
];

export default function Dashboard() {
  const { user } = useAuth();
  const name = user?.name || "Athlete";

  return (
    <div className="dashboard">
      {/* Top Day Tabs */}
      <div style={{ display: "flex", gap: "2rem", alignItems: "center", borderBottom: "1px solid #F1F4F9", paddingBottom: "1rem", marginBottom: "1.5rem" }}>
        <div style={{ fontWeight: 800, fontSize: "1.15rem", color: "#111827", display: "flex", alignItems: "center", gap: "6px" }}>
          <span>•</span> Day 1 👶
        </div>
        <div style={{ fontWeight: 600, fontSize: "1.15rem", color: "#94A3B8" }}>Day 2</div>
        <div style={{ fontWeight: 600, fontSize: "1.15rem", color: "#94A3B8" }}>Day 3</div>
        <div style={{ fontWeight: 600, fontSize: "1.15rem", color: "#94A3B8" }}>Day 4</div>
      </div>

      {/* Main 2-Column Pinterest Grid */}
      <div style={{ display: "grid", gridTemplateColumns: "1.75fr 1fr", gap: "1.5rem", marginBottom: "2rem" }}>
        {/* Left Column */}
        <div>
          {/* Sky Blue Hero Banner */}
          <div style={{
            background: "linear-gradient(135deg, #CFDEEB 0%, #DCE8F2 100%)",
            borderRadius: "28px",
            padding: "2rem 2.2rem",
            position: "relative",
            boxShadow: "0 10px 30px rgba(18, 38, 63, 0.05)",
            marginBottom: "1rem"
          }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
              <div>
                <div style={{ fontSize: "1.35rem", fontWeight: 800, color: "#111827" }}>Daily Workout</div>
                <div style={{ fontSize: "0.95rem", color: "#64748B", fontWeight: 500 }}>Abdominal muscles & Core</div>
              </div>
              <div style={{
                width: "44px", height: "44px", borderRadius: "14px", background: "#FF4757", color: "#FFF",
                display: "flex", alignItems: "center", justifyContent: "center", fontSize: "1.2rem",
                boxShadow: "0 4px 14px rgba(255, 71, 87, 0.35)"
              }}>
                ❤️
              </div>
            </div>

            <div style={{ marginTop: "1.5rem", maxWidth: "80%" }}>
              <h2 style={{ fontSize: "1.85rem", fontWeight: 800, color: "#0F172A", margin: "0 0 0.4rem 0" }}>
                Welcome back, {name}!
              </h2>
              <p style={{ fontSize: "0.95rem", color: "#475569", margin: 0, fontWeight: 500 }}>
                Let's look at your daily activity overview, nutrition, and training routines.
              </p>
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
                <div style={{ fontWeight: 800, fontSize: "0.95rem", color: "#111827" }}>Stretching</div>
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
                <div style={{ fontWeight: 800, fontSize: "0.95rem", color: "#111827" }}>45sec</div>
                <div style={{ fontSize: "0.68rem", fontWeight: 700, color: "#94A3B8", textTransform: "uppercase" }}>TOTAL TIME</div>
              </div>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <div style={{ width: "38px", height: "38px", borderRadius: "12px", background: "#FCE7F3", color: "#DB2777", display: "flex", alignItems: "center", justifyContent: "center" }}>⏳</div>
              <div>
                <div style={{ fontWeight: 800, fontSize: "0.95rem", color: "#111827" }}>30sec</div>
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
                <div style={{ fontSize: "0.9rem", color: "#64748B" }}>Begin in a kneeling position, hands-on thighs and toes curled underneath the buttocks.</div>
              </div>
            </div>
            <div style={{ display: "flex", gap: "14px" }}>
              <div style={{ width: "30px", height: "30px", borderRadius: "50%", background: "#0F172A", color: "white", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 800, fontSize: "0.85rem" }}>2</div>
              <div>
                <div style={{ fontWeight: 700, fontSize: "0.95rem", color: "#111827" }}>Actions:</div>
                <div style={{ fontSize: "0.9rem", color: "#64748B" }}>Move forward on the knees bringing the forearms to the floor, hands close together. Lift the legs and take steady breaths.</div>
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

      <h3 style={{ fontSize: "1.3rem", fontWeight: 800, color: "#111827", marginBottom: "1rem" }}>⚡ Explore AI Modules</h3>
      <div className="module-grid">
        {modules.map((m) => (
          <Link key={m.to} to={m.to} className="module-card">
            <h3>{m.title}</h3>
            <p>{m.desc}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}

