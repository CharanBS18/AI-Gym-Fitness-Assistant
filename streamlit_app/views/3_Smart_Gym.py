import streamlit as st
from utils import api_client
from utils.theme import render_top_day_bar, render_hero_banner

render_top_day_bar(active_day="Day 1")

render_hero_banner(
    title="Smart Gym IoT Assistant",
    subtitle="Simulate real-time sensor streams and receive dynamic AI recommendations for load, resistance, and rest recovery periods.",
    exercise_num="IoT Telemetry",
    target="Connected Equipment Engine",
)

with st.container(border=True):
    st.markdown("<div style='font-size:1.1rem; font-weight:800; color:#111827; margin-bottom:1rem;'>📡 Select Connected Fitness Machine</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        equipment = st.selectbox(
            "Equipment Type", ["treadmill", "rowing_machine", "stationary_bike", "resistance_machine"],
            format_func=lambda x: x.replace("_", " ").title(),
        )
    with c2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        read_clicked = st.button("📡 Fetch Sensor Reading", use_container_width=True, type="primary")

    if read_clicked:
        st.session_state["iot_reading"] = api_client.simulate_iot_reading(equipment)
        st.session_state.pop("iot_recommendation", None)

reading = st.session_state.get("iot_reading")
if reading:
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<div style='font-size:1.1rem; font-weight:800; color:#111827; margin-bottom:1rem;'>📊 Live Simulated Sensor Stream</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("Heart Rate", f"{reading['heart_rate']} bpm")
        c2.metric("Current Resistance", reading["current_resistance"])
        c3.metric("Reps Completed", reading["reps_completed"])

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        if st.button("✨ Generate AI Telemetry Optimization", use_container_width=True, type="primary"):
            try:
                st.session_state["iot_recommendation"] = api_client.get_iot_recommendation(reading)
            except RuntimeError as e:
                st.error(str(e))

rec = st.session_state.get("iot_recommendation")
if rec:
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(
            f"""<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;"><div style="font-size:1.1rem; font-weight:800; color:#111827;">💡 AI Intensity Recommendation</div><div style="background:#FFE4D9; color:#FF5B26; font-weight:800; font-size:0.85rem; padding:4px 12px; border-radius:20px;">{rec['intensity_status'].upper()}</div></div>""",
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        c1.metric("Optimal Resistance", rec["recommended_resistance"])
        c2.metric("Target Rest Period", f"{rec['recommended_rest_seconds']}s")
        st.markdown(
            f"""<div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:16px; padding:1rem 1.25rem; margin-top:1rem; color:#334155; font-size:0.95rem; line-height:1.5;">💬 {rec['message']}</div>""",
            unsafe_allow_html=True,
        )

