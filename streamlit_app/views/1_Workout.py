"""
Module 1 (AI Gym Trainer) + feeds Module 6 (Pose-to-Performance Analyzer).

Unlike the browser-JS version, pose detection here runs server-side: each
incoming webcam frame is processed with MediaPipe Pose inside a
streamlit-webrtc VideoProcessor, which computes a joint angle and runs the
same rep-counting state machine, then draws the skeleton back onto the frame
you see in the browser.
"""
import time
from datetime import datetime, timezone

import av
import cv2
import mediapipe as mp
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, VideoProcessorBase, RTCConfiguration

from utils import api_client

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# landmark indices = [proximal, joint, distal], e.g. hip-knee-ankle
EXERCISE_CONFIG = {
    "squat": {"label": "Squat", "landmarks": (24, 26, 28), "direction": "flex", "enter": 140, "exit": 150},
    "pushup": {"label": "Push-up", "landmarks": (12, 14, 16), "direction": "flex", "enter": 140, "exit": 150},
    "bicep_curl": {"label": "Bicep Curl", "landmarks": (12, 14, 16), "direction": "flex", "enter": 110, "exit": 120},
    "lunge": {"label": "Lunge", "landmarks": (24, 26, 28), "direction": "flex", "enter": 140, "exit": 150},
    "shoulder_press": {"label": "Shoulder Press", "landmarks": (12, 14, 16), "direction": "extend", "enter": 140, "exit": 130},
}

RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})


def angle_between(a, b, c):
    import math
    ab = (a.x - b.x, a.y - b.y)
    cb = (c.x - b.x, c.y - b.y)
    dot = ab[0] * cb[0] + ab[1] * cb[1]
    mag_ab = math.hypot(*ab)
    mag_cb = math.hypot(*cb)
    if mag_ab == 0 or mag_cb == 0:
        return 180.0
    cos_angle = max(-1.0, min(1.0, dot / (mag_ab * mag_cb)))
    return math.degrees(math.acos(cos_angle))


class PoseProcessor(VideoProcessorBase):
    def __init__(self):
        import threading
        self.lock = threading.Lock()
        self.exercise = "squat"
        self.pose = mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6)
        self.reps = []
        self.phase = "rest"
        self.peak_angle = None
        self.current_angle = None
        self.low_visibility = False
        self.start_time = time.time()

    def reset(self):
        with self.lock:
            self.reps = []
            self.phase = "rest"
            self.peak_angle = None
            self.start_time = time.time()

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            landmarks = results.pose_landmarks.landmark
            cfg = EXERCISE_CONFIG[self.exercise]
            ia, ib, ic = cfg["landmarks"]
            a, b, c = landmarks[ia], landmarks[ib], landmarks[ic]

            min_vis = min(a.visibility, b.visibility, c.visibility)
            angle = angle_between(a, b, c)

            with self.lock:
                self.low_visibility = min_vis < 0.5
                self.current_angle = angle
                if not self.low_visibility:
                    self._update_state_machine(angle, cfg)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

    def _update_state_machine(self, angle, cfg):
        if cfg["direction"] == "flex":
            if angle < cfg["enter"]:
                self.phase = "down"
                self.peak_angle = angle if self.peak_angle is None else min(self.peak_angle, angle)
            elif angle > cfg["exit"] and self.phase == "down":
                self._complete_rep()
        else:
            if angle > cfg["enter"]:
                self.phase = "up"
                self.peak_angle = angle if self.peak_angle is None else max(self.peak_angle, angle)
            elif angle < cfg["exit"] and self.phase == "up":
                self._complete_rep()

    def _complete_rep(self):
        self.reps.append({
            "exercise": self.exercise,
            "joint_angle": self.peak_angle,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self.phase = "rest"
        self.peak_angle = None


from utils.theme import (
    render_top_day_bar,
    render_hero_banner,
    render_exercise_stats_pills,
    render_exercise_list_card,
    render_level_friends_card,
    render_description_stepper,
)

# Top Day navigation bar
render_top_day_bar(active_day="Day 1")

left_col, right_col = st.columns([1.75, 1], gap="large")

with left_col:
    exercise_key = st.selectbox(
        "Choose Exercise Movement", options=list(EXERCISE_CONFIG.keys()),
        format_func=lambda k: EXERCISE_CONFIG[k]["label"],
    )

    current_label = EXERCISE_CONFIG[exercise_key]["label"]

    st.markdown(
        f"""<div style="display:flex; justify-content:space-between; align-items:center; background:linear-gradient(135deg, #CFDEEB 0%, #DCE8F2 100%); border-radius:24px; padding:1.2rem 1.6rem; margin-bottom:1rem; box-shadow:0 4px 16px rgba(0,0,0,0.03);"><div><div style="font-size:1.3rem; font-weight:800; color:#111827;">Exercise: {current_label}</div><div style="font-size:0.85rem; color:#64748B; font-weight:500;">AI Real-Time Pose Tracking & Rep Counting</div></div><div style="width:40px; height:40px; border-radius:12px; background:#FF4757; color:white; display:flex; align-items:center; justify-content:center; font-size:1.1rem; box-shadow:0 4px 12px rgba(255, 71, 87, 0.35);">❤️</div></div>""",
        unsafe_allow_html=True,
    )

    # WebRTC Pose Camera Frame
    with st.container(border=True):
        webrtc_ctx = webrtc_streamer(
            key="workout-pose",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTC_CONFIGURATION,
            video_processor_factory=PoseProcessor,
            media_stream_constraints={"video": True, "audio": False},
        )

    btn_col1, btn_col2 = st.columns(2)
    reset_clicked = btn_col1.button("🔄 Reset Counter", use_container_width=True, type="secondary")
    save_clicked = btn_col2.button("✅ Stop & Save Session", use_container_width=True, type="primary")

    if webrtc_ctx.video_processor:
        webrtc_ctx.video_processor.exercise = exercise_key
        if reset_clicked:
            webrtc_ctx.video_processor.reset()

    # Dynamic metric pills below hero
    render_exercise_stats_pills(
        exercise_name=current_label,
        difficulty="2" if exercise_key in ["squat", "pushup"] else "3",
        total_time="Live",
        real_time="Active",
    )

    # Step descriptions for current exercise
    exercise_steps = {
        "squat": [
            ("Start point:", "Stand with feet shoulder-width apart, chest upright, hands clasped in front of your chest."),
            ("Actions:", "Lower your hips back and down as if sitting into a chair. Keep knees tracking over toes, descend until thighs are parallel, then press through heels to stand."),
        ],
        "pushup": [
            ("Start point:", "Place hands flat on the floor slightly wider than shoulder-width, body in a rigid high plank position."),
            ("Actions:", "Lower your chest until elbows reach 90 degrees, core braced, then push firmly back up to full extension."),
        ],
        "bicep_curl": [
            ("Start point:", "Stand tall with dumbbells in hand, palms facing forward, elbows tucked close to your torso."),
            ("Actions:", "Curl the weights upward while contracting biceps until fully flexed, then lower slowly with controlled tempo."),
        ],
        "lunge": [
            ("Start point:", "Stand upright with hands on hips, core engaged and feet hip-distance apart."),
            ("Actions:", "Step forward with one leg, lowering hips until both knees are bent at approximately a 90-degree angle, then return."),
        ],
        "shoulder_press": [
            ("Start point:", "Hold weights at shoulder height with palms facing outward and elbows bent at 90 degrees."),
            ("Actions:", "Press weights vertically overhead until arms are extended, pausing at the top before descending slowly."),
        ]
    }

    render_description_stepper(exercise_steps.get(exercise_key, [
        ("Start point:", "Adopt proper starting posture with shoulders retracted and core engaged."),
        ("Actions:", "Perform movement with smooth tempo and complete range of motion."),
    ]))

with right_col:
    # Live stats placeholder during workout
    stats_placeholder = st.empty()
    result_placeholder = st.empty()

    # Exercises List Card
    render_exercise_list_card([
        {"title": "Abdominal muscles", "time": "10 mins", "cal": "40 Kcal", "status": "progress", "bg": "#CFDEEB", "icon": "🧘"},
        {"title": "Squat & Lunges", "time": "15 mins", "cal": "90 Kcal", "status": "completed", "bg": "#EDE9FE", "icon": "🏋️"},
        {"title": "Push-up Routine", "time": "10 mins", "cal": "65 Kcal", "status": "completed", "bg": "#BAE6FD", "icon": "💪"},
        {"title": "High Knee Jumping", "time": "10 mins", "cal": "110 Kcal", "status": "missed", "bg": "#FCE7F3", "icon": "🏃"},
    ])

    # Level & Friends Card
    render_level_friends_card(level="BEGINNER", xp="1,021 XP", friends_count=10)

if save_clicked and webrtc_ctx.video_processor:
    processor = webrtc_ctx.video_processor
    with processor.lock:
        reps_snapshot = list(processor.reps)
        duration = time.time() - processor.start_time

    form_issues = []
    if not reps_snapshot:
        form_issues.append("no valid reps detected - make sure your full body is visible and try again")

    try:
        result = api_client.submit_workout_session({
            "exercise": exercise_key,
            "reps": reps_snapshot,
            "duration_seconds": duration,
            "form_issues": form_issues,
        })
        with result_placeholder.container(border=True):
            st.markdown("<div style='font-size:1.1rem; font-weight:800; color:#111827; margin-bottom:0.75rem;'>🎉 Session Result</div>", unsafe_allow_html=True)
            st.metric("Valid Reps Counted", result["rep_count"])
            c1, c2 = st.columns(2)
            c1.metric("Form Score", f"{result['form_score']}/100")
            c2.metric("Tempo Consistency", f"{result['tempo_consistency']}/100")
            for f in result["feedback"]:
                st.markdown(f"<div style='font-size:0.9rem; color:#475569; margin-top:4px;'>• {f}</div>", unsafe_allow_html=True)
    except RuntimeError as e:
        st.error(str(e))

elif webrtc_ctx.state.playing:
    while webrtc_ctx.state.playing:
        processor = webrtc_ctx.video_processor
        if processor:
            with processor.lock:
                reps = len(processor.reps)
                angle = processor.current_angle
                low_vis = processor.low_visibility
            with stats_placeholder.container():
                with st.container(border=True):
                    st.markdown("<div style='font-size:0.8rem; font-weight:800; color:#64748B; text-transform:uppercase;'>⚡ LIVE TRACKING</div>", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    c1.metric("Reps", reps)
                    c2.metric("Joint Angle", f"{angle:.0f}°" if angle is not None else "-")
                    if low_vis:
                        st.warning("⚠ Step back so your full body is visible")
        time.sleep(0.3)
