"""
Shared login/register gate. Every module page calls require_login() at the
top - it renders a login/register form and st.stop()s the script if the user
isn't authenticated yet, so the rest of that page's code never runs.

Also fetches and caches the user's own profile (name, is_admin, etc.) right
after login/register via GET /auth/me, so:
  - the sidebar and Home dashboard can greet the user by name without an
    extra API call on every page, and
  - app.py can decide whether to show the Admin page in navigation, based
    on session_state["profile"]["is_admin"].
"""
import streamlit as st
from utils import api_client


def current_user() -> dict:
    """The logged-in user's cached profile (empty dict if not loaded yet)."""
    return st.session_state.get("profile") or {}


def is_admin() -> bool:
    return bool(current_user().get("is_admin"))


def _load_profile() -> bool:
    try:
        st.session_state["profile"] = api_client.get_me()
        return True
    except RuntimeError:
        # token expired/invalid - drop it and fall back to the login screen
        st.session_state.pop("token", None)
        st.session_state.pop("profile", None)
        return False


def require_login():
    if st.session_state.get("token"):
        if st.session_state.get("profile") or _load_profile():
            return  # already logged in with a cached profile - let the page continue

    st.markdown(
        """<div style="text-align:center; padding: 2rem 0 1rem;"><div style="display:inline-flex; align-items:center; justify-content:center; width:64px; height:64px; border-radius:20px; background:#111827; color:#FFFFFF; font-size:2rem; margin-bottom:1rem; box-shadow:0 10px 25px rgba(0,0,0,0.15);">⚡</div><h1 style="margin-bottom:0.25rem; font-size:2.2rem; font-weight:800; color:#111827; letter-spacing:-0.03em;">Beefit Fitness Assistant</h1><p style="color:#718096; font-size:1.05rem; font-weight:500;">Your smart AI-driven training, nutrition & daily habit dashboard</p></div>""",
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 1.8, 1])
    with center:
        with st.container(border=True):
            tab_login, tab_register = st.tabs(["🔐 Sign In", "✨ Create Account"])

            with tab_login:
                with st.form("login_form"):
                    email = st.text_input("Email Address", placeholder="name@example.com")
                    password = st.text_input("Password", type="password", placeholder="••••••••")
                    submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")
                if submitted:
                    try:
                        result = api_client.login(email, password)
                        st.session_state["token"] = result["access_token"]
                        _load_profile()
                        st.rerun()
                    except RuntimeError as e:
                        st.error(str(e))

            with tab_register:
                with st.form("register_form"):
                    name = st.text_input("Full Name", placeholder="e.g. Alex Johnson")
                    reg_email = st.text_input("Email Address", key="reg_email", placeholder="name@example.com")
                    reg_password = st.text_input("Password", type="password", key="reg_password", placeholder="Create secure password")
                    col1, col2, col3 = st.columns(3)
                    age = col1.number_input("Age", min_value=0, max_value=120, value=25)
                    height_cm = col2.number_input("Height (cm)", min_value=0.0, value=170.0)
                    weight_kg = col3.number_input("Weight (kg)", min_value=0.0, value=70.0)
                    goal = st.selectbox("Primary Goal", ["lose", "maintain", "gain"])
                    reg_submitted = st.form_submit_button("Create Account", use_container_width=True, type="primary")
                if reg_submitted:
                    try:
                        result = api_client.register({
                            "name": name, "email": reg_email, "password": reg_password,
                            "age": int(age), "height_cm": height_cm, "weight_kg": weight_kg, "goal": goal,
                        })
                        st.session_state["token"] = result["access_token"]
                        _load_profile()
                        st.rerun()
                    except RuntimeError as e:
                        st.error(str(e))

    st.stop()


def logout_button():
    profile = current_user()
    st.sidebar.markdown(
        """<div style="display:flex; align-items:center; gap:10px; margin-bottom:1.2rem; padding:0.5rem 0.2rem;"><div style="width:40px; height:40px; border-radius:14px; background:#111827; color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:1.3rem; box-shadow:0 4px 12px rgba(0,0,0,0.1);">⚡</div><div><div style="font-weight:800; font-size:1.1rem; color:#111827; letter-spacing:-0.02em;">Beefit</div><div style="font-size:0.75rem; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.05em;">AI ASSISTANT</div></div></div>""",
        unsafe_allow_html=True,
    )
    
    if profile.get("name"):
        badge = " 👑 Admin" if profile.get("is_admin") else ""
        st.sidebar.markdown(
            f"""<div style="display:flex; align-items:center; gap:12px; background:#FFFFFF; border:1px solid #EEF2F6; border-radius:18px; padding:0.8rem 1rem; margin-bottom:1rem; box-shadow:0 2px 8px rgba(0,0,0,0.02);"><div style="width:38px; height:38px; border-radius:50%; background:#FFE4D9; color:#FF5B26; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.1rem;">👤</div><div style="overflow:hidden;"><div style="font-weight:700; font-size:0.9rem; color:#111827; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">{profile['name']}{badge}</div><div style="font-size:0.75rem; color:#94A3B8; white-space:nowrap; text-overflow:ellipsis; overflow:hidden;">{profile.get('email', '')}</div></div></div>""",
            unsafe_allow_html=True,
        )
    if st.sidebar.button("Log out", use_container_width=True, type="secondary"):
        st.session_state.pop("token", None)
        st.session_state.pop("profile", None)
        st.rerun()
    st.sidebar.markdown("<div style='height: 1px; background: #E2E8F0; margin: 1rem 0;'></div>", unsafe_allow_html=True)
