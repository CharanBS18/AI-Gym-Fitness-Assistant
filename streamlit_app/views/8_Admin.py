"""
Admin dashboard - only reachable if app.py added it to navigation, which
only happens when the logged-in user's cached profile has is_admin = true.
"""
import streamlit as st
from utils import api_client
from utils.theme import render_top_day_bar, render_hero_banner

render_top_day_bar(active_day="Day 1")

render_hero_banner(
    title="Admin Control & Telemetry",
    subtitle="Platform-wide audit of user registrations, real-time workouts, performance metrics, and adherence.",
    exercise_num="Platform Governance",
    target="Admin Master Dashboard",
)

try:
    overview = api_client.admin_overview()
except RuntimeError as e:
    st.error(str(e))
    st.stop()

st.markdown("<div style='font-size:1.1rem; font-weight:800; color:#111827; margin-bottom:1rem;'>📊 Platform Overview</div>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Users", overview["total_users"])
c2.metric("Workout Sessions", overview["total_workout_sessions"])
c3.metric("Chat Messages", overview["total_chat_messages"])
c4.metric("Diet Plans", overview["total_diet_plans"])
c5.metric("Avg Form Score", f"{overview['platform_avg_form_score']}/100")

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

try:
    users = api_client.admin_list_users()
except RuntimeError as e:
    st.error(str(e))
    st.stop()

if not users:
    st.info("No users registered yet.")
    st.stop()

with st.container(border=True):
    st.markdown("<div style='font-size:1.1rem; font-weight:800; color:#111827; margin-bottom:1rem;'>👥 Registered Athletes & Members</div>", unsafe_allow_html=True)
    st.dataframe(
        [
            {
                "Name": u["name"],
                "Email": u["email"],
                "Age": u.get("age") or "—",
                "Height (cm)": u.get("height_cm") or "—",
                "Weight (kg)": u.get("weight_kg") or "—",
                "Goal": u.get("goal") or "—",
                "Role": "👑 Admin" if u.get("is_admin") else "Member",
                "Joined": (u.get("created_at") or "")[:10],
            }
            for u in users
        ],
        use_container_width=True,
        hide_index=True,
    )

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("<div style='font-size:1.1rem; font-weight:800; color:#111827; margin-bottom:1rem;'>🔍 Inspect Individual User Performance</div>", unsafe_allow_html=True)
    labels = {f"{u['name']} ({u['email']})": u["id"] for u in users}
    
    col_sel, col_btn = st.columns([3, 1])
    with col_sel:
        selected_label = st.selectbox("Select Member Profile", list(labels.keys()))
        selected_id = labels[selected_label]
    with col_btn:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        load_clicked = st.button("📊 Load Member Activity", use_container_width=True, type="primary")

    if load_clicked:
        try:
            activity = api_client.admin_user_activity(selected_id)
            st.session_state["admin_selected_activity"] = activity
        except RuntimeError as e:
            st.error(str(e))

activity = st.session_state.get("admin_selected_activity")
if activity:
    profile = activity["profile"]
    st.markdown(f"<div style='font-size:1.2rem; font-weight:800; color:#111827; margin: 1.5rem 0 1rem 0;'>📈 Detailed Report: {profile['name']}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        with st.container(border=True):
            st.markdown("<div style='font-weight:800; color:#111827; margin-bottom:0.75rem;'>🏋️ Recent Workout Sessions</div>", unsafe_allow_html=True)
            if activity["recent_workouts"]:
                st.dataframe(
                    [
                        {
                            "Exercise": w["exercise"],
                            "Reps": w["rep_count"],
                            "Form Score": f"{w['form_score']}/100",
                            "Date": (w.get("created_at") or "")[:10],
                        }
                        for w in activity["recent_workouts"]
                    ],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.caption("No workout sessions logged yet.")

            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            st.markdown("<div style='font-weight:800; color:#111827; margin-bottom:0.5rem;'>📈 Latest Performance Score</div>", unsafe_allow_html=True)
            perf = activity["latest_performance"]
            if perf:
                st.metric("Performance Index", f"{perf['performance_score']}/100")
            else:
                st.caption("No performance report generated yet.")

    with col2:
        with st.container(border=True):
            st.markdown("<div style='font-weight:800; color:#111827; margin-bottom:0.75rem;'>🔥 Habit Adherence Logs</div>", unsafe_allow_html=True)
            if activity["recent_habit_logs"]:
                completed = sum(1 for h in activity["recent_habit_logs"] if h["workout_completed"])
                st.caption(f"{completed} of {len(activity['recent_habit_logs'])} recent planned days completed")
                st.dataframe(
                    [{"Date": h["date"], "Status": "✅ Completed" if h["workout_completed"] else "❌ Skipped"} for h in activity["recent_habit_logs"]],
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.caption("No habit logs yet.")

            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            st.markdown("<div style='font-weight:800; color:#111827; margin-bottom:0.5rem;'>🥗 Active Diet Targets</div>", unsafe_allow_html=True)
            diet = activity["diet_plan"]
            if diet:
                st.markdown(
                    f"""<div style="background:#FEF3C7; border:1px solid #FDE68A; border-radius:14px; padding:0.8rem 1rem; color:#92400E; font-weight:600;">Target: {diet['target_calories']} kcal/day · BMI {diet['bmi']} ({diet['bmi_category']})</div>""",
                    unsafe_allow_html=True,
                )
            else:
                st.caption("No diet plan generated yet.")

