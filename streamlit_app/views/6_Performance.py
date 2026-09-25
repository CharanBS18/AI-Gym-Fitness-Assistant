import streamlit as st
from utils import api_client
from utils.theme import render_top_day_bar, render_hero_banner

render_top_day_bar(active_day="Day 1")

render_hero_banner(
    title="Pose-to-Performance Analyzer",
    subtitle="AI aggregates your weekly MediaPipe computer vision metrics into a holistic form score, tempo evaluation, and volume trend.",
    exercise_num="Analytics Engine",
    target="Weekly Form & Biometrics",
)

try:
    report = api_client.get_weekly_performance()
    with st.container(border=True):
        st.markdown(
            f"""<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.2rem;"><div style="font-size:1.1rem; font-weight:800; color:#111827;">📈 Weekly Aggregate Report</div><div style="font-size:0.85rem; font-weight:700; color:#64748B; background:#F1F5F9; padding:4px 12px; border-radius:20px;">Week Starting: {report['week_start']}</div></div>""",
            unsafe_allow_html=True,
        )
        c1, c2, c3 = st.columns(3)
        c1.metric("Sessions Logged", report["total_sessions"])
        c2.metric("Avg Form Score", f"{report['avg_form_score']}/100")
        c3.metric("Tempo Consistency", f"{report['avg_tempo_consistency']}/100")
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.metric("Overall Performance Index", f"{report['performance_score']}/100")
        
        st.markdown(
            f"""<div style="background:linear-gradient(135deg, #CFDEEB 0%, #DCE8F2 100%); border-radius:18px; padding:1.2rem 1.4rem; margin-top:1.2rem;"><div style="font-size:0.8rem; font-weight:800; color:#475569; text-transform:uppercase; letter-spacing:0.05em; margin-bottom:4px;">PROGRESSION TREND</div><div style="font-size:1.15rem; font-weight:800; color:#0F172A;">📊 {report['trend']}</div></div>""",
            unsafe_allow_html=True,
        )

        if report["total_sessions"] == 0:
            st.info("Complete a session in the AI Gym Trainer to see your real-time score here.")
except RuntimeError as e:
    st.error(str(e))

