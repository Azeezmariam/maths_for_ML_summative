from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import numpy as np
import pandas as pd
import pickle as pk
import uvicorn

# Load the model
with open('model.pkl', 'rb') as file:
    model = pk.load(file)

app = FastAPI()

class StartupData(BaseModel):
    Research_And_Development: float
    Administration: float
    Marketing_Spend: float
    State: str

@app.get('/', status_code=status.HTTP_200_OK)
async def home():
    return 'Hello LOLA'

@app.post('/predict', status_code=status.HTTP_200_OK)
async def predict(data: StartupData):
    try:
        # Convert input data to DataFrame
        input_data = pd.DataFrame([data.dict()])
        
        # Prepare features
        categorical_features = ['State']
        features = input_data.copy()

        # One-hot encode categorical features
        categorical_encoded = pd.get_dummies(features[categorical_features], drop_first=True)
        features = features.drop(columns=categorical_features)
        features = pd.concat([features, categorical_encoded], axis=1)

        # Ensure features have the correct columns for the model
        missing_cols = set(model.feature_names_in_) - set(features.columns)
        for col in missing_cols:
            features[col] = 0

        # Order columns as expected by the model
        features = features[model.feature_names_in_]
        
        # Make prediction
        prediction = model.predict(features)
        return {'prediction': prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)