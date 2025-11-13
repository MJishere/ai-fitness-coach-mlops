from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# load the model
model = joblib.load("backend/model/calorie_model.pkl")

app = FastAPI(title="AI Fitness Coach Backend")

class UserInput(BaseModel):
    gender: int
    age: int
    height: float
    weight: float
    exercise: float

@app.post("/predict_calories")
def predict_calories(data: UserInput) -> dict:
    X = [[data.gender, data.age, data.height, data.weight, data.exercise]]
    prediction = model.predict(X)[0]
    return {"daily_calories_needed": round(prediction,2)}

# Dummy endpoint - later update open ai
@app.get("/generate_workout_plan")
def generate_workout_plan():
    return {"plan": "Workout plan will be generated using OpenAI soon"}

@app.get("/generate_diet_plan")
def generate_diet_plan():
    return {"diet": "Diet plan will be generated using Open AI soon"}