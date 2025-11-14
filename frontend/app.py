import streamlit as st
import requests

# Load custom CSS
with open("frontend/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Page config
st.set_page_config(page_title="AI Fitness Coach", layout="centered")

# Title
st.title("AI Fitness Coach App")

API_URL = "http://127.0.0.1:8000"

# ---------------- USER INPUT CARD ---------------- #
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🧍 User Information")

gender_option = st.selectbox("Gender", ["Male", "Female"])
gender = 1 if gender_option == "Male" else 0

age = st.number_input("Age", min_value=10, max_value=100, value=25)
height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
exercise = st.selectbox("Physical Exercise Level", [1, 2, 3, 4, 5])

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ACTION BUTTONS ---------------- #
st.markdown("<div class='btn-row'>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# Placeholder for results
result_placeholder = st.empty()

# Placeholder for full-screen glass loader
overlay = st.empty()

# Reusable glassmorphism loader (HTML block)
GLASS_LOADER_HTML = """
<div class='overlay'>
    <div class='glass-card'>
        <div class='glass-loader'></div>
        <div class='loader-text'>Loading...</div>
    </div>
</div>
"""


# ---------------- CALORIES BUTTON ---------------- #
with col1:
    if st.button("🔥Calculate Calories"):

        # Show glass loader
        overlay.markdown(GLASS_LOADER_HTML, unsafe_allow_html=True)

        payload = {
            "gender": gender,
            "age": age,
            "height": height,
            "weight": weight,
            "exercise": exercise,
        }

        response = requests.post(f"{API_URL}/predict_calories", json=payload)

        # Hide overlay
        overlay.empty()

        if response.status_code == 200:
            calories = response.json()["daily_calories_needed"]
            result_placeholder.success(f"Daily Calories: **{calories} kcal**")
        else:
            result_placeholder.error("Failed to get calorie prediction.")

# ---------------- WORKOUT BUTTON ---------------- #
with col2:
    if st.button("💪 Workout Plan"):

        overlay.markdown(GLASS_LOADER_HTML, unsafe_allow_html=True)

        payload = {
            "gender": gender,
            "age": age,
            "height": height,
            "weight": weight,
            "exercise": exercise,
        }

        response = requests.post(f"{API_URL}/generate_workout_plan", json=payload)
        data = response.json()

        overlay.empty()

        if "plan" in data:
            result_placeholder.info(data["plan"])
        else:
            result_placeholder.error(data.get("error", "Unknown error occurred"))

# ---------------- DIET BUTTON ---------------- #
with col3:
    if st.button("🥗 Diet Plan"):

        overlay.markdown(GLASS_LOADER_HTML, unsafe_allow_html=True)

        payload = {
            "gender": gender,
            "age": age,
            "height": height,
            "weight": weight,
            "exercise": exercise,
        }

        response = requests.post(f"{API_URL}/generate_diet_plan", json=payload)
        data = response.json()

        overlay.empty()

        if "diet" in data:
            result_placeholder.info(data["diet"])
        else:
            result_placeholder.error("Failed to generate diet plan.")

st.markdown("</div>", unsafe_allow_html=True)
