from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from openai import OpenAI
import os
import pandas as pd

# Load the ML model
model = joblib.load("/app/backend/model/calorie_model.pkl")

app = FastAPI(title="AI Fitness Coach Backend")

class UserInput(BaseModel):
    gender: int
    age: int
    height: float
    weight: float
    exercise: float


# ---------- Helper Function (Avoid code duplication) ----------
def predict_calories_internal(data: UserInput):
    """Predict calories using DataFrame with correct feature names."""
    X = pd.DataFrame([{
        "Gender": data.gender,
        "Age": data.age,
        "Height": data.height,
        "Weight": data.weight,
        "Physical exercise": data.exercise
    }])

    prediction = model.predict(X)[0]
    return round(prediction, 2)


# ------------------- API ENDPOINT: Predict Calories ------------------- #
@app.post("/predict_calories")
def predict_calories(data: UserInput) -> dict:
    calories = predict_calories_internal(data)
    return {"daily_calories_needed": calories}


# -------------------- OpenAI Client -------------------- #
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ------------------- API ENDPOINT: Workout Plan ------------------- #
@app.post("/generate_workout_plan")
def generate_workout_plan(data: UserInput):
    try:
        calories = predict_calories_internal(data)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            timeout=30,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert certified fitness trainer. "
                        "You create safe, personalized, beginner-friendly workout plans "
                        "that are structured, effective, and easy to follow."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Create a personalized workout plan based on:\n"
                        f"- Gender: {'Male' if data.gender == 1 else 'Female'}\n"
                        f"- Age: {data.age}\n"
                        f"- Height: {data.height} cm\n"
                        f"- Weight: {data.weight} kg\n"
                        f"- Exercise Level (1-5): {data.exercise}\n"
                        f"- Estimated Daily Calories: {calories} kcal\n\n"
                        "Include:\n"
                        "- Warm-up (time + exercises)\n"
                        "- Main workout (sets, reps, rest)\n"
                        "- Cardio recommendations\n"
                        "- Cool-down\n"
                        "- Weekly progression tips\n"
                        "Keep it simple and beginner-friendly."
                    )
                }
            ]
        )

        plan = response.choices[0].message.content
        return {"calories": calories, "plan": plan}     

    except Exception as e:
        return {"error": str(e)}


# ------------------- API ENDPOINT: Diet Plan ------------------- #
@app.post("/generate_diet_plan")
def generate_diet_plan(data: UserInput):
    try:
        calories = predict_calories_internal(data)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            timeout=30,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a certified nutritionist. You create detailed, realistic, "
                        "and highly personalized diet plans."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Create a personalized diet plan based on:\n"
                        f"- Gender: {'Male' if data.gender == 1 else 'Female'}\n"
                        f"- Age: {data.age}\n"
                        f"- Height: {data.height} cm\n"
                        f"- Weight: {data.weight} kg\n"
                        f"- Exercise Level (1-5): {data.exercise}\n"
                        f"- Estimated Daily Calories: {calories} kcal\n\n"
                        "Include:\n"
                        "- Macronutrient targets (protein, carbs, fats)\n"
                        "- Breakfast, lunch, dinner + 2 snacks\n"
                        "- Portion sizes\n"
                        "- Hydration goals\n"
                        "- Foods to avoid\n"
                        "- Weekly improvement tips\n"
                        "Make it simple, practical, and tasty."
                    )
                }
            ]
        )

        diet = response.choices[0].message.content
        return {"calories": calories, "diet": diet}
        
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/health")
def health():
    return {"status": "ok"}

