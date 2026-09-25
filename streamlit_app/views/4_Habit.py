from datetime import date
import streamlit as st
from utils import api_client
from utils.theme import render_top_day_bar, render_hero_banner

render_top_day_bar(active_day="Day 1")

render_hero_banner(
    title="Daily Adherence & Habit Tracker",
    subtitle="Behavioral machine learning models calculate your skip-risk likelihood and keep your fitness streak on track.",
    exercise_num="Habit Engine",
    target="Consistency & Streak Monitoring",
)

today = date.today().isoformat()

with st.container(border=True):
    st.markdown("<div style='font-size:1.1rem; font-weight:800; color:#111827; margin-bottom:1rem;'>📅 Quick Check-in for Today</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("✅ I Completed My Workout Today", use_container_width=True, type="primary"):
        api_client.log_habit({"date": today, "workout_completed": True, "planned": True})
        st.success("Awesome job! Logged today's completed session.")
    if c2.button("⏭️ I Rested / Skipped Today", use_container_width=True, type="secondary"):
        api_client.log_habit({"date": today, "workout_completed": False, "planned": True})
        st.info("Logged a rest/skip day. Consistency builds over time!")

try:
    prediction = api_client.get_habit_prediction()
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div style='font-size:1.1rem; font-weight:800; color:#111827; margin-bottom:1rem;'>🔥 Current Habit & Risk Snapshot</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.metric("Active Streak", f"{prediction['current_streak']} days 🔥")
        c2.metric("Skip Risk Likelihood", f"{prediction['skip_risk_percent']}%")
        
        st.markdown(
            f"""<div style="background:linear-gradient(135deg, #F3E8FF 0%, #FBEBFE 100%); border-radius:18px; padding:1.2rem 1.4rem; margin-top:1.2rem; border:1px solid #DDD6FE;"><div style="font-size:0.8rem; font-weight:800; color:#6D28D9; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:4px;">AI COACH NUDGE</div><div style="font-size:1rem; font-weight:600; color:#1E1B4B; line-height:1.4;">💬 {prediction['nudge_message']}</div></div>""",
            unsafe_allow_html=True,
        )
except RuntimeError as e:
    st.error(str(e))

