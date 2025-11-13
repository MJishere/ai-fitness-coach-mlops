import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# Loading the dataset

df = pd.read_csv("backend/model/calories.csv")

#Select Features
X = df[["Gender", "Age", "Height", "Weight", "Physical exercise"]]

#Select target
y = df["Calories"]

# Ensure physical exercise is numeric
X = X.apply(pd.to_numeric, errors="coerce")
y = pd.to_numeric(y,errors="coerce")

# Train / test splitting
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, "backend/model/calorie_model.pkl")

print("Model Trained and Saved As calorie_model.pkl")
