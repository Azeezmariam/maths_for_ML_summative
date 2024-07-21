from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle as pk

# Define the FastAPI app
app = FastAPI()

# Load the model
with open('model.pkl', 'rb') as file:
    model = pk.load(file)

# Define the request model
class PredictionRequest(BaseModel):
    Research_And_Development: float
    Administration: float
    Marketing_Spend: float
    State: str

@app.post('/predict')
def predict(request: PredictionRequest):
    try:
        # DataFrame from the input data
        input_data = pd.DataFrame([{
            'Research_And_Development': request.Research_And_Development,
            'Administration': request.Administration,
            'Marketing_Spend': request.Marketing_Spend,
            'State': request.State
        }])
        
        # Expected columns
        expected_columns = [
            'Research_And_Development', 'Administration', 'Marketing_Spend',
            'State_California', 'State_Florida'  
        ]
        
        # Preprocessing
        x = input_data.copy()
        categorical_features = ['State']

        # One-hot encode categorical features
        x_encoded = pd.get_dummies(x[categorical_features], drop_first=True)
        x_numeric = x.drop(columns=categorical_features)
        x_preprocessed = pd.concat([x_numeric, x_encoded], axis=1)
        
        # Ensure DataFrame has all expected columns, fill missing columns with 0
        for col in expected_columns:
            if col not in x_preprocessed.columns:
                x_preprocessed[col] = 0
        
        # Reorder columns to match model's expectation
        x_preprocessed = x_preprocessed[expected_columns]

        # Make prediction
        prediction = model.predict(x_preprocessed)
        return {"business profit": prediction[0]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
