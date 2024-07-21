## Public API Endpoint for Predictions

This project provides a publicly accessible API endpoint that returns predictions based on input values. The API is built using FastAPI and is deployed on Render.

### API Endpoint

- **Base URL**: `https://maths-for-ml-summative.onrender.com`
- **Endpoint for Predictions**: `/predict`

### Request Format

**Method**: POST  
**Content-Type**: application/json

**Request Body**:
```json
{
  "Research_And_Development": 100000,
  "Administration": 200000,
  "Marketing_Spend": 300000,
  "State": "California"
}
Response format
{
  "business profit": 123456.78
}
