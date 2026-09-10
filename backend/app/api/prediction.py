from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from app.schemas.prediction import (
    DiabetesPredictionInput, HeartPredictionInput, 
    LiverPredictionInput, KidneyPredictionInput, PredictionResponse
)
from app.services.prediction_service import prediction_service
from app.api.auth import get_current_user
from app.schemas.auth import UserInDB
from app.database.mongodb import get_database

router = APIRouter(prefix="/api/predict", tags=["predictions"])

async def save_prediction(user_id: str, disease: str, input_data: dict, result: dict):
    db = get_database()
    prediction_record = {
        "user_id": user_id,
        "disease": disease,
        "input_data": input_data,
        "result": result,
        "timestamp": datetime.utcnow()
    }
    await db.predictions.insert_one(prediction_record)

@router.post("/diabetes", response_model=PredictionResponse)
async def predict_diabetes(input_data: DiabetesPredictionInput, current_user: UserInDB = Depends(get_current_user)):
    try:
        data_dict = input_data.model_dump(by_alias=True)
        result = prediction_service.predict("diabetes", data_dict)
        await save_prediction(current_user.id, "diabetes", data_dict, result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/heart", response_model=PredictionResponse)
async def predict_heart(input_data: HeartPredictionInput, current_user: UserInDB = Depends(get_current_user)):
    try:
        data_dict = input_data.model_dump(by_alias=True)
        result = prediction_service.predict("heart", data_dict)
        await save_prediction(current_user.id, "heart", data_dict, result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/liver", response_model=PredictionResponse)
async def predict_liver(input_data: LiverPredictionInput, current_user: UserInDB = Depends(get_current_user)):
    try:
        data_dict = input_data.model_dump(by_alias=True)
        result = prediction_service.predict("liver", data_dict)
        await save_prediction(current_user.id, "liver", data_dict, result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/kidney", response_model=PredictionResponse)
async def predict_kidney(input_data: KidneyPredictionInput, current_user: UserInDB = Depends(get_current_user)):
    try:
        data_dict = input_data.model_dump(by_alias=True)
        result = prediction_service.predict("kidney", data_dict)
        await save_prediction(current_user.id, "kidney", data_dict, result)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_prediction_history(current_user: UserInDB = Depends(get_current_user)):
    db = get_database()
    cursor = db.predictions.find({"user_id": current_user.id}).sort("timestamp", -1)
    history = await cursor.to_list(length=100)
    
    # Convert ObjectId to string for JSON serialization
    for record in history:
        record["_id"] = str(record["_id"])
        
    return {"history": history}
