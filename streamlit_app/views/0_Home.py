import streamlit as st
from utils.auth import current_user
from utils import api_client
from utils.theme import (
    render_top_day_bar,
    render_hero_banner,
    render_exercise_stats_pills,
    render_exercise_list_card,
    render_level_friends_card,
    render_description_stepper,
)

user = current_user()
name = user.get("name", "there")

# 1. Top Horizontal Day Bar (from Pinterest reference)
render_top_day_bar(active_day="Day 1")

# 2. Main 2-Column Pinterest Layout (Left Hero & Details / Right Exercises & Level)
left_col, right_col = st.columns([1.75, 1], gap="large")

with left_col:
    # Large Sky Blue Hero Banner
    render_hero_banner(
        title=f"Welcome back, {name}!",
        subtitle="Let's crush your workout targets and keep your streak strong today.",
        exercise_num="Daily Routine",
        target=f"Goal: {user.get('goal', 'Fitness').capitalize()}",
    )

    # 4 Metric capsules from reference
    render_exercise_stats_pills(
        exercise_name="Core & Form",
        difficulty="2 / 5",
        total_time="45 min",
        real_time="Active",
    )

    # Description card with numbered step timeline
    render_description_stepper([
        ("Start point:", "Warm up with 5 minutes of light cardio and joint mobility stretches."),
        ("Actions:", "Proceed with your customized AI Workout Trainer sessions. Focus on consistent tempo and complete range of motion."),
    ])

with right_col:
    # Exercises card
    render_exercise_list_card([
        {"title": "Abdominal muscles", "time": "10 mins", "cal": "40 Kcal", "status": "progress", "bg": "#CFDEEB", "icon": "🧘"},
        {"title": "Squat & Lunges", "time": "15 mins", "cal": "90 Kcal", "status": "completed", "bg": "#EDE9FE", "icon": "🏋️"},
        {"title": "Push-up Routine", "time": "10 mins", "cal": "65 Kcal", "status": "completed", "bg": "#BAE6FD", "icon": "💪"},
        {"title": "High Knee Jumping", "time": "10 mins", "cal": "110 Kcal", "status": "missed", "bg": "#FCE7F3", "icon": "🏃"},
    ])

    # Lavender Level & Friends card
    render_level_friends_card(
        level="BEGINNER" if user.get("goal") != "strength" else "ADVANCED",
        xp="1,021 XP",
        friends_count=10,
    )

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
st.markdown("<h3 style='font-size:1.3rem; font-weight:800; color:#111827; margin-bottom:1rem;'>📊 Real-time Performance & Health Stats</h3>", unsafe_allow_html=True)

# Personal quick-stats row
col1, col2, col3, col4 = st.columns(4)

try:
    perf = api_client.get_weekly_performance()
    col1.metric("Performance Score", f"{perf['performance_score']}/100", help="This week's average across your workout sessions")
    col2.metric("Sessions This Week", perf["total_sessions"])
except RuntimeError:
    col1.metric("Performance Score", "—")
    col2.metric("Sessions This Week", "—")

try:
    habit = api_client.get_habit_prediction()
    col3.metric("Current Streak", f"{habit['current_streak']} 🔥")
    col4.metric("Skip Risk", f"{habit['skip_risk_percent']}%")
except RuntimeError:
    col3.metric("Current Streak", "—")
    col4.metric("Skip Risk", "—")

try:
    diet = api_client.get_diet_plan()
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div style='font-size:0.8rem; font-weight:800; color:#64748B; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:0.75rem;'>🥗 DIET & NUTRITION TARGETS</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Target Calories", f"{diet['target_calories']} kcal/day")
        c2.metric("BMI", f"{diet['bmi']} ({diet['bmi_category']})")
        c3.metric("Primary Goal", user.get("goal", "—").capitalize())
except RuntimeError:
    pass

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
st.markdown("<h3 style='font-size:1.3rem; font-weight:800; color:#111827; margin-bottom:1rem;'>⚡ Explore AI Modules</h3>", unsafe_allow_html=True)

modules = [
    ("🏋️ AI Gym Trainer", "Webcam pose detection, live rep counting & real-time form feedback.", "views/1_Workout.py"),
    ("🥗 AI Dietician & Coach", "BMI, BMR, macros, custom meal plan & smart grocery list.", "views/2_Diet.py"),
    ("📡 Smart Gym Assistant", "Simulated sensor feed drives resistance & rest recommendations.", "views/3_Smart_Gym.py"),
    ("🔥 AI Fitness Habit Tracker", "Skip-risk prediction, streak tracking & motivational nudges.", "views/4_Habit.py"),
    ("💬 Virtual Gym Buddy", "Mood-aware AI chat companion for daily motivation.", "views/5_Chat.py"),
    ("📈 Performance Analyzer", "Weekly performance score & trend from your sessions.", "views/6_Performance.py"),
    ("📍 Gym Recommender", "Nearby gyms matched to your goal and location.", "views/7_Gym_Finder.py"),
]

cols = st.columns(2)
for i, (title, desc, _) in enumerate(modules):
    with cols[i % 2]:
        with st.container(border=True):
            st.markdown(f"<div style='font-weight:800; font-size:1.1rem; color:#111827; margin-bottom:4px;'>{title}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:0.9rem; color:#64748B; line-height:1.4;'>{desc}</div>", unsafe_allow_html=True)

