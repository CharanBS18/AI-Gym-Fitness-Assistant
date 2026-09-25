import streamlit as st
from utils import api_client
from utils.theme import render_top_day_bar, render_hero_banner

render_top_day_bar(active_day="Day 1")

render_hero_banner(
    title="AI Dietician & Macro Coach",
    subtitle="Personalized BMR calculations, target calorie deficit/surplus, tailored meal breakdowns, and shopping list.",
    exercise_num="Nutrition Hub",
    target="Calorie & Macro Optimization",
)

with st.container(border=True):
    st.markdown("<div style='font-size:1.1rem; font-weight:800; color:#111827; margin-bottom:1rem;'>🥗 Configure Your Nutrition Profile</div>", unsafe_allow_html=True)
    with st.form("diet_form"):
        c1, c2, c3 = st.columns(3)
        weight_kg = c1.number_input("Weight (kg)", min_value=1.0, value=70.0)
        height_cm = c2.number_input("Height (cm)", min_value=1.0, value=170.0)
        age = c3.number_input("Age", min_value=1, max_value=120, value=25)

        c4, c5, c6 = st.columns(3)
        sex = c4.selectbox("Sex", ["male", "female"])
        activity_level = c5.selectbox(
            "Activity level", ["sedentary", "light", "moderate", "active", "very_active"], index=2,
        )
        goal = c6.selectbox("Goal", ["lose", "maintain", "gain"], index=1)

        dietary_preference = st.selectbox("Dietary preference", ["veg", "non_veg", "vegan"])
        submitted = st.form_submit_button("Generate Nutrition Plan", use_container_width=True, type="primary")

if submitted:
    try:
        plan = api_client.generate_diet_plan({
            "weight_kg": weight_kg, "height_cm": height_cm, "age": int(age),
            "sex": sex, "activity_level": activity_level, "goal": goal,
            "dietary_preference": dietary_preference,
        })
        st.session_state["diet_plan"] = plan
    except RuntimeError as e:
        st.error(str(e))

plan = st.session_state.get("diet_plan")
if plan:
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # 3 Stat metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Body Mass Index", f"{plan['bmi']} ({plan['bmi_category']})")
    c2.metric("Basal Metabolic Rate", f"{plan['bmr']} kcal")
    c3.metric("Target Calories", f"{plan['target_calories']} kcal/day")

    st.markdown(
        f"""<div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:1rem; margin: 1.5rem 0;"><div style="background:#FEF3C7; border-radius:18px; padding:1.1rem 1.4rem; border:1px solid #FDE68A;"><div style="font-size:0.75rem; font-weight:800; color:#B45309; text-transform:uppercase;">PROTEIN</div><div style="font-size:1.6rem; font-weight:800; color:#92400E; font-family:'Outfit',sans-serif;">{plan['macros']['protein_g']}g</div></div><div style="background:#EDE9FE; border-radius:18px; padding:1.1rem 1.4rem; border:1px solid #DDD6FE;"><div style="font-size:0.75rem; font-weight:800; color:#6D28D9; text-transform:uppercase;">CARBOHYDRATES</div><div style="font-size:1.6rem; font-weight:800; color:#5B21B6; font-family:'Outfit',sans-serif;">{plan['macros']['carbs_g']}g</div></div><div style="background:#FCE7F3; border-radius:18px; padding:1.1rem 1.4rem; border:1px solid #FBCFE8;"><div style="font-size:0.75rem; font-weight:800; color:#BE185D; text-transform:uppercase;">HEALTHY FATS</div><div style="font-size:1.6rem; font-weight:800; color:#9D174D; font-family:'Outfit',sans-serif;">{plan['macros']['fat_g']}g</div></div></div>""",
        unsafe_allow_html=True,
    )

    col_meals, col_grocery = st.columns([1.2, 1], gap="large")

    with col_meals:
        with st.container(border=True):
            st.markdown("<div style='font-size:1.1rem; font-weight:800; color:#111827; margin-bottom:1rem;'>🍽️ Daily Meal Blueprint</div>", unsafe_allow_html=True)
            meal_icons = {"breakfast": "🥣", "lunch": "🥗", "dinner": "🍲", "snacks": "🍎"}
            for meal, items in plan["meal_plan"].items():
                icon = meal_icons.get(meal.lower(), "🍴")
                st.markdown(
                    f"""<div style="padding:0.75rem 0; border-bottom:1px solid #F1F5F9;"><div style="font-weight:800; font-size:0.95rem; color:#111827;">{icon} {meal.capitalize()}</div><div style="color:#64748B; font-size:0.9rem; margin-top:2px;">{', '.join(items)}</div></div>""",
                    unsafe_allow_html=True,
                )

    with col_grocery:
        with st.container(border=True):
            st.markdown("<div style='font-size:1.1rem; font-weight:800; color:#111827; margin-bottom:1rem;'>🛒 Smart Grocery List</div>", unsafe_allow_html=True)
            for item in plan["grocery_list"]:
                st.markdown(
                    f"""<div style="display:flex; align-items:center; gap:8px; padding:0.4rem 0;"><span style="color:#FF5B26; font-weight:bold;">✓</span><span style="color:#334155; font-size:0.9rem; font-weight:500;">{item}</span></div>""",
                    unsafe_allow_html=True,
                )


