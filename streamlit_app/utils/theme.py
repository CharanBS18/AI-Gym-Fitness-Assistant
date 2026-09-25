import textwrap
import streamlit as st

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

:root {
    --bg-canvas: #DFE5EE;
    --card-bg: #FFFFFF;
    --primary-coral: #FF5B26;
    --primary-coral-hover: #E84D1A;
    --primary-red: #FF4757;
    --hero-blue: #D5E2EC;
    --hero-blue-grad: linear-gradient(135deg, #CFDEEB 0%, #DCE8F2 100%);
    --lavender-card: linear-gradient(135deg, #F3E8FF 0%, #FBEBFE 100%);
    --text-dark: #111827;
    --text-muted: #718096;
    --text-light: #A0AEC0;
    --border-subtle: #EEF2F6;
    --radius-pill: 9999px;
    --radius-card: 28px;
    --radius-hero: 32px;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    color: var(--text-dark);
}

/* Background canvas */
.stApp {
    background-color: #DFE5EE !important;
    background-image: radial-gradient(#CCD5E2 1px, transparent 1px);
    background-size: 24px 24px;
}

/* Main Container Frame - Pinterest Rounded White Container */
.stMainBlockContainer, [data-testid="stMainBlockContainer"] {
    background: #FFFFFF !important;
    border-radius: 36px !important;
    box-shadow: 0 24px 50px -12px rgba(27, 43, 74, 0.12), 0 0 0 1px rgba(255, 255, 255, 0.7) !important;
    padding: 2.5rem 3rem !important;
    margin-top: 1.5rem !important;
    margin-bottom: 2rem !important;
    max-width: 1400px !important;
}

/* Sidebar / Rail Navigation */
section[data-testid="stSidebar"] {
    background: #F1F4F9 !important;
    border-right: 1px solid #E2E8F0 !important;
}

section[data-testid="stSidebar"] > div {
    background: transparent !important;
}

/* Navigation Links */
[data-testid="stSidebarNav"] {
    padding-top: 1rem !important;
}

[data-testid="stSidebarNav"] a {
    border-radius: 20px !important;
    padding: 0.65rem 1rem !important;
    margin-bottom: 0.35rem !important;
    font-weight: 600 !important;
    color: #64748B !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebarNav"] a:hover {
    background-color: #E2E8F0 !important;
    color: #1E293B !important;
    transform: translateX(3px);
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: #FF5B26 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(255, 91, 38, 0.35) !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] span {
    color: #FFFFFF !important;
}

/* Buttons */
.stButton > button, button[data-testid*="baseButton"] {
    border-radius: 50px !important;
    font-weight: 700 !important;
    padding: 0.6rem 1.6rem !important;
    font-size: 0.95rem !important;
    letter-spacing: -0.01em !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: none !important;
}

.stButton > button[kind="primary"], button[data-testid*="baseButton-primary"], .stButton > button[type="primary"] {
    background: linear-gradient(135deg, #FF6433 0%, #FF5B26 100%) !important;
    color: #FFFFFF !important;
    box-shadow: 0 6px 18px rgba(255, 91, 38, 0.32) !important;
}

.stButton > button[kind="primary"]:hover, button[data-testid*="baseButton-primary"]:hover, .stButton > button[type="primary"]:hover {
    background: linear-gradient(135deg, #FF5B26 0%, #E84D1A 100%) !important;
    box-shadow: 0 8px 22px rgba(255, 91, 38, 0.45) !important;
    transform: translateY(-2px);
}

.stButton > button[kind="secondary"], button[data-testid*="baseButton-secondary"], .stButton > button[type="secondary"] {
    background: #F1F5F9 !important;
    color: #334155 !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: none !important;
}

.stButton > button[kind="secondary"]:hover, button[data-testid*="baseButton-secondary"]:hover, .stButton > button[type="secondary"]:hover {
    background: #E2E8F0 !important;
    color: #0F172A !important;
    transform: translateY(-1px);
}

/* Metric Cards */
div[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #EEF2F6 !important;
    border-radius: 20px !important;
    padding: 1.1rem 1.3rem !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06) !important;
}

div[data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: #718096 !important;
    font-weight: 700 !important;
}

div[data-testid="stMetricValue"] {
    font-size: 1.65rem !important;
    font-weight: 800 !important;
    color: #111827 !important;
    font-family: 'Outfit', sans-serif !important;
}

/* Containers with border */
[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 24px !important;
    border: 1px solid #EEF2F6 !important;
    background: #FFFFFF !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.03) !important;
    padding: 1.25rem !important;
}

/* Form inputs */
input[type="text"], input[type="password"], input[type="number"], select, textarea {
    border-radius: 14px !important;
    border: 1.5px solid #E2E8F0 !important;
    background: #F8FAFC !important;
    color: #0F172A !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1rem !important;
    transition: all 0.2s ease !important;
}

input:focus, select:focus, textarea:focus {
    border-color: #FF5B26 !important;
    box-shadow: 0 0 0 3px rgba(255, 91, 38, 0.15) !important;
    background: #FFFFFF !important;
}

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #F1F4F9 !important;
    border-radius: 30px !important;
    padding: 4px !important;
    gap: 4px !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 26px !important;
    padding: 0.5rem 1.4rem !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    color: #64748B !important;
    border: none !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
    background: #FFFFFF !important;
    color: #111827 !important;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.06) !important;
}

/* Chat Messages */
[data-testid="stChatMessage"] {
    border-radius: 20px !important;
    padding: 1rem 1.25rem !important;
    margin-bottom: 0.75rem !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03) !important;
}

[data-testid="stChatMessage"][data-testid*="user"] {
    background: #F8FAFC !important;
    border: 1px solid #E2E8F0 !important;
}

[data-testid="stChatMessage"][data-testid*="assistant"] {
    background: #FFF7F4 !important;
    border: 1px solid #FFE4D9 !important;
}

/* Headers */
h1, h2, h3, h4 {
    font-family: 'Outfit', 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
    color: #111827 !important;
    letter-spacing: -0.02em !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #F1F4F9;
}
::-webkit-scrollbar-thumb {
    background: #CBD5E1;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #94A3B8;
}
</style>
"""

def inject_theme():
    """Call at the top of pages or app.py to enforce Pinterest design system."""
    st.markdown(textwrap.dedent(THEME_CSS), unsafe_allow_html=True)


def render_top_day_bar(active_day="Day 1", days=None):
    if days is None:
        days = [
            ("Day 1 👶", "Day 1"),
            ("Day 2", "Day 2"),
            ("Day 3", "Day 3"),
            ("Day 4", "Day 4"),
        ]
    
    tabs_html = ""
    for label, key in days:
        is_active = key == active_day
        if is_active:
            tabs_html += f"""<div style="display:inline-flex; align-items:center; gap:6px; font-weight:800; font-size:1.15rem; color:#111827; margin-right:2rem; cursor:pointer;"><span style="font-size:1.2rem; color:#111827;">•</span> {label}</div>"""
        else:
            tabs_html += f"""<div style="display:inline-flex; align-items:center; font-weight:600; font-size:1.15rem; color:#94A3B8; margin-right:2rem; cursor:pointer;">{label}</div>"""
            
    html = f"""<div style="display:flex; align-items:center; justify-content:flex-start; padding: 0.5rem 0 1.5rem; border-bottom: 1px solid #F1F4F9; margin-bottom: 1.5rem;">{tabs_html}</div>"""
    st.markdown(html, unsafe_allow_html=True)


def render_hero_banner(title, subtitle, exercise_num="Exercise 1/5", target="Abdominal muscles"):
    bg_style = "background: linear-gradient(135deg, #CFDEEB 0%, #DCE8F2 100%);"
    
    html = f"""<div style="position:relative; width:100%; border-radius:28px; {bg_style} padding: 2.2rem 2.4rem; min-height: 200px; overflow:hidden; box-shadow: 0 10px 30px rgba(18, 38, 63, 0.05); margin-bottom: 1rem;"><div style="display:flex; justify-content:space-between; align-items:flex-start;"><div><div style="font-size: 1.35rem; font-weight: 800; color: #111827; font-family:'Outfit',sans-serif;">{exercise_num}</div><div style="font-size: 0.95rem; font-weight: 500; color: #64748B; margin-top: 2px;">{target}</div></div><div style="display:flex; align-items:center; justify-content:center; width: 44px; height: 44px; border-radius: 14px; background: #FF4757; color: white; font-size: 1.2rem; box-shadow: 0 4px 14px rgba(255, 71, 87, 0.35); cursor:pointer;">❤️</div></div><div style="margin-top: 1.2rem; max-width: 80%;"><h2 style="font-size: 1.85rem; font-weight: 800; color: #0F172A; margin: 0 0 0.4rem 0; line-height: 1.2;">{title}</h2><p style="font-size: 0.95rem; color: #475569; margin: 0; font-weight: 500;">{subtitle}</p></div></div>"""
    st.markdown(html, unsafe_allow_html=True)


def render_exercise_stats_pills(exercise_name="Stretching", difficulty="2", total_time="45sec", real_time="30sec"):
    html = f"""<div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; background:#FFFFFF; border:1px solid #EEF2F6; border-radius:22px; padding: 1rem 1.4rem; box-shadow: 0 4px 16px rgba(0,0,0,0.02); margin-bottom: 1.5rem;"><div style="display:flex; align-items:center; gap: 12px;"><div style="width:42px; height:42px; border-radius:14px; background:#FEF3C7; color:#D97706; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">🏃</div><div><div style="font-weight:800; font-size:1rem; color:#111827;">{exercise_name}</div><div style="font-size:0.7rem; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.06em;">EXERCISE</div></div></div><div style="display:flex; align-items:center; gap: 12px;"><div style="width:42px; height:42px; border-radius:14px; background:#EDE9FE; color:#7C3AED; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">⭐</div><div><div style="font-weight:800; font-size:1rem; color:#111827;">{difficulty}</div><div style="font-size:0.7rem; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.06em;">DIFFICULT</div></div></div><div style="display:flex; align-items:center; gap: 12px;"><div style="width:42px; height:42px; border-radius:14px; background:#DCFCE7; color:#059669; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">⏱️</div><div><div style="font-weight:800; font-size:1rem; color:#111827;">{total_time}</div><div style="font-size:0.7rem; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.06em;">TOTAL TIME</div></div></div><div style="display:flex; align-items:center; gap: 12px;"><div style="width:42px; height:42px; border-radius:14px; background:#FCE7F3; color:#DB2777; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">⏳</div><div><div style="font-weight:800; font-size:1rem; color:#111827;">{real_time}</div><div style="font-size:0.7rem; font-weight:700; color:#94A3B8; text-transform:uppercase; letter-spacing:0.06em;">REAL TIME</div></div></div></div>"""
    st.markdown(html, unsafe_allow_html=True)


def render_exercise_list_card(items=None):
    if items is None:
        items = [
            {"title": "Abdominal muscles", "time": "10 mins", "cal": "40Kcal", "status": "progress", "bg": "#CFDEEB", "icon": "🧘"},
            {"title": "Jumping on ball", "time": "15 mins", "cal": "90Kcal", "status": "completed", "bg": "#EDE9FE", "icon": "🔵"},
            {"title": "With dumbbells", "time": "10 mins", "cal": "50Kcal", "status": "completed", "bg": "#BAE6FD", "icon": "🏋️"},
            {"title": "Jumping", "time": "10 mins", "cal": "110Kcal", "status": "missed", "bg": "#FCE7F3", "icon": "🏃"},
        ]

    items_html = ""
    for it in items:
        status_icon = ""
        if it["status"] == "completed":
            status_icon = '<div style="width:24px; height:24px; border-radius:50%; background:#10B981; color:white; display:flex; align-items:center; justify-content:center; font-size:0.75rem; font-weight:bold;">✓</div>'
        elif it["status"] == "progress":
            status_icon = '<div style="width:24px; height:24px; border-radius:50%; border:3px solid #FF5B26; border-top-color:transparent; display:inline-block;"></div>'
        else:
            status_icon = '<div style="width:24px; height:24px; border-radius:50%; background:#EF4444; color:white; display:flex; align-items:center; justify-content:center; font-size:0.75rem; font-weight:bold;">✕</div>'

        items_html += f"""<div style="display:flex; align-items:center; justify-content:space-between; padding: 0.75rem 0.5rem; border-bottom: 1px solid #F1F5F9;"><div style="display:flex; align-items:center; gap: 14px;"><div style="width:52px; height:42px; border-radius:14px; background:{it['bg']}; display:flex; align-items:center; justify-content:center; font-size:1.3rem;">{it['icon']}</div><div><div style="font-weight:700; font-size:0.95rem; color:#111827;">{it['title']}</div><div style="display:flex; align-items:center; gap:10px; font-size:0.8rem; color:#64748B; margin-top:2px;"><span>⏱️ {it['time']}</span><span>⚡ {it['cal']}</span></div></div></div><div>{status_icon}</div></div>"""

    html = f"""<div style="background:#FFFFFF; border:1px solid #EEF2F6; border-radius:24px; padding: 1.4rem; box-shadow: 0 4px 20px rgba(0,0,0,0.03);"><div style="font-size:0.8rem; font-weight:800; color:#64748B; text-transform:uppercase; letter-spacing:0.08em; margin-bottom: 1rem;">EXERCISES</div>{items_html}</div>"""
    st.markdown(html, unsafe_allow_html=True)


def render_level_friends_card(level="BEGINNER", xp="1021", friends_count=10):
    html = f"""<div style="background: linear-gradient(135deg, #F3E8FF 0%, #FBEBFE 100%); border-radius: 24px; padding: 1.4rem; box-shadow: 0 4px 20px rgba(124, 58, 237, 0.06); margin-top: 1.25rem;"><div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 1.2rem;"><div style="display:flex; align-items:center; gap:10px;"><div style="width:40px; height:40px; border-radius:50%; background:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:1.2rem; box-shadow:0 2px 8px rgba(0,0,0,0.05);">👶</div><div><div style="font-size:0.95rem; font-weight:800; color:#1E1B4B; letter-spacing:0.04em;">{level}</div><div style="font-size:0.7rem; font-weight:700; color:#6B7280; text-transform:uppercase;">YOUR LEVEL</div></div></div><div style="display:flex; align-items:center; gap:6px; font-weight:800; font-size:1.1rem; color:#1E1B4B;">🏋️ {xp}</div></div><div><div style="font-size:0.75rem; font-weight:800; color:#6B7280; text-transform:uppercase; letter-spacing:0.06em; margin-bottom: 0.6rem;">MY FRIENDS</div><div style="display:flex; align-items:center; justify-content:space-between;"><div style="display:flex; align-items:center;"><div style="width:34px; height:34px; border-radius:50%; background:#FED7AA; border:2px solid #FFFFFF; display:flex; align-items:center; justify-content:center; font-size:0.9rem; margin-right:-8px;">👱‍♀️</div><div style="width:34px; height:34px; border-radius:50%; background:#BAE6FD; border:2px solid #FFFFFF; display:flex; align-items:center; justify-content:center; font-size:0.9rem; margin-right:-8px;">👨‍🦱</div><div style="width:34px; height:34px; border-radius:50%; background:#FECDD3; border:2px solid #FFFFFF; display:flex; align-items:center; justify-content:center; font-size:0.9rem; margin-right:-8px;">👩‍🦰</div><div style="width:34px; height:34px; border-radius:50%; background:#DDD6FE; border:2px solid #FFFFFF; display:flex; align-items:center; justify-content:center; font-size:0.8rem; font-weight:700; color:#5B21B6; margin-right:8px;">+{friends_count}</div></div><div style="width:38px; height:38px; border-radius:14px; background:#FF5B26; color:white; display:flex; align-items:center; justify-content:center; font-size:1.1rem; box-shadow:0 4px 12px rgba(255, 91, 38, 0.35); cursor:pointer;">🎁</div></div></div></div>"""
    st.markdown(html, unsafe_allow_html=True)


def render_description_stepper(steps=None):
    if steps is None:
        steps = [
            ("Start point:", "Begin in a kneeling position, hands-on thighs and toes curled underneath the buttocks."),
            ("Actions:", "Move forward on the knees bringing the forearms to the floor, hands close together. Lift the legs and take a steady deep breath."),
        ]

    steps_html = ""
    for idx, (title, desc) in enumerate(steps, start=1):
        steps_html += f"""<div style="display:flex; gap: 16px; margin-bottom: 1.2rem;"><div style="width:32px; height:32px; min-width:32px; border-radius:50%; background:#0F172A; color:white; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.9rem;">{idx}</div><div><div style="font-weight:700; font-size:0.95rem; color:#111827; margin-bottom: 2px;">{title}</div><div style="font-size:0.9rem; color:#64748B; line-height:1.5;">{desc}</div></div></div>"""

    html = f"""<div style="background:#FFFFFF; border:1px solid #EEF2F6; border-radius:24px; padding: 1.6rem; box-shadow: 0 4px 20px rgba(0,0,0,0.03);"><div style="font-size:0.8rem; font-weight:800; color:#64748B; text-transform:uppercase; letter-spacing:0.08em; margin-bottom: 1.2rem;">DESCRIPTION</div>{steps_html}</div>"""
    st.markdown(html, unsafe_allow_html=True)

