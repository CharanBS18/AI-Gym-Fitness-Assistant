import streamlit as st
from utils import api_client
from utils.theme import render_top_day_bar, render_hero_banner

render_top_day_bar(active_day="Day 1")

render_hero_banner(
    title="Virtual AI Gym Buddy",
    subtitle="Chat with your mood-aware fitness companion for advice, form tips, workout motivation, and recovery.",
    exercise_num="AI Chat Coach",
    target="Conversational Intelligence",
)

if "chat_loaded" not in st.session_state:
    try:
        history = api_client.get_chat_history()
        st.session_state["chat_messages"] = [
            {"message": h["message"], "reply": h["reply"], "mood": h["mood"]} for h in reversed(history)
        ]
    except RuntimeError:
        st.session_state["chat_messages"] = []
    st.session_state["chat_loaded"] = True

with st.container(border=True):
    st.markdown("<div style='font-size:1.1rem; font-weight:800; color:#111827; margin-bottom:1rem;'>💬 Conversation Stream</div>", unsafe_allow_html=True)
    if not st.session_state["chat_messages"]:
        st.info("Say hello to your AI Gym Buddy below to start chatting!")

    for turn in st.session_state["chat_messages"]:
        with st.chat_message("user"):
            st.markdown(f"<span style='font-weight:600; color:#111827;'>{turn['message']}</span>", unsafe_allow_html=True)
        with st.chat_message("assistant"):
            st.markdown(
                f"""<div><div style="font-weight:500; color:#1E293B; line-height:1.5;">{turn['reply']}</div><div style="margin-top:6px; font-size:0.75rem; font-weight:700; color:#FF5B26; text-transform:uppercase; letter-spacing:0.04em;">Mood: {turn['mood']}</div></div>""",
                unsafe_allow_html=True,
            )

user_input = st.chat_input("How are you feeling about today's workout?")
if user_input:
    try:
        result = api_client.send_chat_message(user_input)
        st.session_state["chat_messages"].append({
            "message": user_input, "reply": result["reply"], "mood": result["detected_mood"],
        })
        st.rerun()
    except RuntimeError as e:
        st.error(str(e))

