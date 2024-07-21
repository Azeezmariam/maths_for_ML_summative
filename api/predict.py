from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
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
    return {'message': 'Hello LOLA'}

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

        # Define expected columns
        expected_columns = ['Research_And_Development', 'Administration', 'Marketing_Spend', 'State', 'Profit']

        # Add missing columns with default value 0
        missing_cols = set(expected_columns) - set(features.columns)
        for col in missing_cols:
            features[col] = 0

        # Order columns as expected by the model
        features = features[expected_columns]

        # Make prediction
        prediction = model.predict(features)
        return {'prediction': prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")

if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)