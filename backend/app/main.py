from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import prediction, auth

from contextlib import asynccontextmanager
from app.database.mongodb import connect_to_mongo, close_mongo_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title="Explainable AI-Based Multi-Disease Prediction API",
    description="Backend for Healthcare Decision Support System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Multi-Disease Prediction API"}

@app.get("/api/diseases")
def get_diseases():
    return {
        "diseases": [
            {"id": "diabetes", "name": "Diabetes"},
            {"id": "heart", "name": "Heart Disease"},
            {"id": "liver", "name": "Liver Disease"},
            {"id": "kidney", "name": "Kidney Disease"}
        ]
    }
