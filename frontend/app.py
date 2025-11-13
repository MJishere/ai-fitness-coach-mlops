import streamlit  as st
import requests

st.set_page_config(page_title="AI Fitness Coach", layout="centered")

st.title("AI Fitness Coach App")
st.subheader("Smart Workout 🥗Diet 🧮Calorie Prediction")

#FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

st.write("---")
st.header("📊 Daily Calorie Prediction")

gender_option = st.selectbox("Gender", ["Male", "Female"])
gender = 1 if gender_option == "Male" else 0
age = st.number_input("Age", min_value=10, max_value=100, value=25)
height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
exercise = st.selectbox("Physical Exercise Level", [1,2,3,4,5])

if st.button("Predict Daily Calories"):
    payload = {
        "gender": gender,
        "age": age,
        "height": height,
        "weight": weight,
        "exercise": exercise,
    }

    response = requests.post(f"{API_URL}/predict_calories", json=payload)

    if response.status_code == 200:
        calories = response.json()["daily_calories_needed"]
        st.success(f"Daily Calories Needed: **{calories} kcal**")
    else:
        st.error("Error predicting calories, Check back later!")

st.write("---")
st.header("Generate Workout Plan")

if st.button("Generate Workout Plan"):
    response = requests.get(f"{API_URL}/generate_workout_plan")
    st.info(response.json()["plan"])
