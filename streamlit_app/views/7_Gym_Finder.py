import streamlit as st
from utils import api_client
from utils.theme import render_top_day_bar, render_hero_banner

render_top_day_bar(active_day="Day 1")

render_hero_banner(
    title="Gym Recommender & Locator",
    subtitle="Discover top-rated fitness centers matched with your training targets, programs, and geographic radius.",
    exercise_num="Location Hub",
    target="Smart Facility Finder",
)

with st.container(border=True):
    st.markdown("<div style='font-size:1.1rem; font-weight:800; color:#111827; margin-bottom:1rem;'>🔍 Search Nearby Fitness Studios & Gyms</div>", unsafe_allow_html=True)
    with st.form("location_form"):
        place = st.text_input(
            "Target Location / Neighborhood", placeholder="e.g. Indiranagar, Bengaluru or Brooklyn, NY",
            help="Any place name works - a neighborhood, city, or landmark.",
        )
        col1, col2 = st.columns(2)
        goal = col1.selectbox("Fitness Focus", ["", "lose", "gain", "maintain", "strength", "cardio"], format_func=lambda x: "All Goals" if not x else x.capitalize())
        max_distance_km = col2.slider("Search Radius (km)", min_value=1, max_value=50, value=10)
        search_submitted = st.form_submit_button("🔍 Find Matching Gyms", use_container_width=True, type="primary")

if search_submitted:
    if not place.strip():
        st.warning("Please enter a location or landmark name.")
    else:
        try:
            with st.spinner(f"Locating '{place}'..."):
                location = api_client.geocode_place(place)
            st.session_state["gym_location"] = location

            with st.spinner("Finding nearby gyms..."):
                gyms = api_client.recommend_gyms({
                    "latitude": location["latitude"],
                    "longitude": location["longitude"],
                    "goal": goal or None,
                    "max_distance_km": max_distance_km,
                })
            st.session_state["gym_results"] = gyms
        except RuntimeError as e:
            st.error(str(e))
            st.session_state.pop("gym_results", None)

location = st.session_state.get("gym_location")
if location:
    st.markdown(
        f"""<div style="background:#DCFCE7; border:1px solid #BBF7D0; border-radius:16px; padding:0.8rem 1.2rem; margin:1.2rem 0; color:#166534; font-weight:600; font-size:0.95rem;">📍 Showing gyms near <b>{location['display_name']}</b></div>""",
        unsafe_allow_html=True,
    )

results = st.session_state.get("gym_results")
if results:
    for gym in results:
        with st.container(border=True):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"<div style='font-size:1.2rem; font-weight:800; color:#111827; margin-bottom:4px;'>{gym['name']}</div>", unsafe_allow_html=True)
                programs_chips = "".join([f"<span style='display:inline-block; background:#F1F5F9; color:#475569; font-weight:600; font-size:0.8rem; padding:3px 10px; border-radius:12px; margin-right:6px; margin-top:4px;'>{p}</span>" for p in gym['programs']])
                st.markdown(f"<div style='margin-top:6px;'>{programs_chips}</div>", unsafe_allow_html=True)
            with c2:
                st.metric("Distance", f"{gym['distance_km']} km")
                st.markdown(f"<div style='margin-top:6px; font-weight:800; color:#D97706; font-size:0.95rem;'>⭐ {gym['rating']} / 5.0</div>", unsafe_allow_html=True)
elif search_submitted:
    st.info("No gyms found within that distance - try increasing the max search radius.")

