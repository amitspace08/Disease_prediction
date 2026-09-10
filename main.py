from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
import os

app = FastAPI(title="Disease Prediction System API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to the specific frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Model Loaders
# ----------------------------
MODELS_DIR = "models"

# Heart Model
try:
    heart_model = joblib.load(os.path.join(MODELS_DIR, "heart", "heart_model.pkl"))
    heart_columns = joblib.load(os.path.join(MODELS_DIR, "heart", "model_columns.pkl"))
except Exception as e:
    print(f"Error loading Heart Model: {e}")
    heart_model, heart_columns = None, None

# Liver Model
try:
    liver_model = joblib.load(os.path.join(MODELS_DIR, "liver", "liver_model.pkl"))
    liver_scaler = joblib.load(os.path.join(MODELS_DIR, "liver", "liver_scaler.pkl"))
    try:
        liver_columns = list(liver_scaler.feature_names_in_)
    except AttributeError:
        liver_columns = [
            "age", "gender", "tot_bilirubin", "direct_bilirubin", "tot_proteins", 
            "albumin", "ag_ratio", "sgpt", "sgot", "alkphos", 
            "tot_bilirubin_log", "direct_bilirubin_log", "tot_proteins_log", "albumin_log", "ag_ratio_log"
        ]
except Exception as e:
    print(f"Error loading Liver Model: {e}")
    liver_model, liver_scaler, liver_columns = None, None, None

# Kidney Model
try:
    kidney_model = joblib.load(os.path.join(MODELS_DIR, "kidney", "kidney_model.pkl"))
    kidney_scaler = joblib.load(os.path.join(MODELS_DIR, "kidney", "scaler.pkl"))
except Exception as e:
    print(f"Error loading Kidney Model: {e}")
    kidney_model, kidney_scaler = None, None

# Diabetes Model
try:
    diabetes_model = joblib.load(os.path.join(MODELS_DIR, "diabetes", "diabetes_model.pkl"))
    diabetes_scaler = joblib.load(os.path.join(MODELS_DIR, "diabetes", "scaler.pkl"))
except Exception as e:
    print(f"Error loading Diabetes Model: {e}")
    diabetes_model, diabetes_scaler = None, None


# ----------------------------
# Request Schemas
# ----------------------------
class HeartRequest(BaseModel):
    age: float
    sex: str  # "Male" or "Female"
    chest_pain: str  # "TA", "ATA", "NAP", "ASY"
    resting_bp: float
    cholesterol: float
    fasting_bs: str  # "Yes" or "No"
    resting_ecg: str  # "Normal", "ST", "LVH"
    max_hr: float
    exercise_angina: str  # "Yes" or "No"
    oldpeak: float
    st_slope: str  # "Up", "Flat", "Down"

class LiverRequest(BaseModel):
    age: float
    gender: str  # "Male" or "Female"
    tot_bilirubin: float
    direct_bilirubin: float
    tot_proteins: float  # Alkaline Phosphotase
    albumin: float  # SGPT (ALT)
    ag_ratio: float  # SGOT (AST)
    sgpt: float  # Total Proteins
    sgot: float  # Albumin
    alkphos: float  # A/G Ratio

class KidneyRequest(BaseModel):
    age: float
    bp: float
    sg: float
    al: float
    su: float
    rbc: str  # "normal" or "abnormal"
    pc: str  # "normal" or "abnormal"
    pcc: str  # "present" or "notpresent"
    ba: str  # "present" or "notpresent"
    bgr: float
    bu: float
    sc: float
    sod: float
    pot: float
    hemo: float
    pcv: float
    wc: float
    rc: float
    htn: str  # "yes" or "no"
    dm: str  # "yes" or "no"
    cad: str  # "yes" or "no"
    appet: str  # "good" or "poor"
    pe: str  # "yes" or "no"
    ane: str  # "yes" or "no"

class DiabetesRequest(BaseModel):
    preg: float
    glucose: float
    bp: float
    skin: float
    insulin: float
    bmi: float
    dpf: float
    age: float


# ----------------------------
# API Endpoints
# ----------------------------
@app.get("/api/health")
def health_check():
    return {"status": "ok", "models_loaded": {
        "heart": heart_model is not None,
        "liver": liver_model is not None,
        "kidney": kidney_model is not None,
        "diabetes": diabetes_model is not None
    }}

@app.post("/api/predict/heart")
def predict_heart(req: HeartRequest):
    if not heart_model:
        raise HTTPException(status_code=500, detail="Heart model not loaded")
    
    # Process inputs
    chest_pain_code = req.chest_pain
    resting_ecg_code = req.resting_ecg

    raw_input = {
        "Age": req.age,
        "RestingBP": req.resting_bp,
        "Cholesterol": req.cholesterol,
        "FastingBS": 1 if req.fasting_bs == "Yes" else 0,
        "MaxHR": req.max_hr,
        "Oldpeak": req.oldpeak,
        "Sex_M": 1 if req.sex == "Male" else 0,
        "ChestPainType_ATA": 1 if chest_pain_code == "ATA" else 0,
        "ChestPainType_NAP": 1 if chest_pain_code == "NAP" else 0,
        "ChestPainType_TA": 1 if chest_pain_code == "TA" else 0,
        "RestingECG_Normal": 1 if resting_ecg_code == "Normal" else 0,
        "RestingECG_ST": 1 if resting_ecg_code == "ST" else 0,
        "ExerciseAngina_Y": 1 if req.exercise_angina == "Yes" else 0,
        "ST_Slope_Flat": 1 if req.st_slope == "Flat" else 0,
        "ST_Slope_Up": 1 if req.st_slope == "Up" else 0,
    }
    
    input_df = pd.DataFrame([raw_input])
    input_df = input_df[heart_columns]
    
    proba = heart_model.predict_proba(input_df)[0]
    prob_disease = proba[1] * 100
    prediction = heart_model.predict(input_df)[0]
    
    return {
        "prediction": int(prediction),
        "probability": float(prob_disease),
        "confidence": float(abs(prob_disease - 50.0) * 2)
    }

@app.post("/api/predict/liver")
def predict_liver(req: LiverRequest):
    if not liver_model or not liver_scaler:
        raise HTTPException(status_code=500, detail="Liver model not loaded")
        
    raw = {
        "age": req.age,
        "gender": 1 if req.gender == "Male" else 0,
        "tot_bilirubin": req.tot_bilirubin,
        "direct_bilirubin": req.direct_bilirubin,
        "tot_proteins": req.tot_proteins,
        "albumin": req.albumin,
        "ag_ratio": req.ag_ratio,
        "sgpt": req.sgpt,
        "sgot": req.sgot,
        "alkphos": req.alkphos
    }
    
    # Log scaling matching liver.py exactly
    LOG_COLS = ["tot_bilirubin", "direct_bilirubin", "tot_proteins", "albumin", "ag_ratio"]
    for col in LOG_COLS:
        raw[f"{col}_log"] = np.log1p(raw[col])
        
    input_df = pd.DataFrame([raw])
    input_df = input_df[liver_columns]
    
    X_scaled = liver_scaler.transform(input_df)
    pred = liver_model.predict(X_scaled)[0]
    proba = liver_model.predict_proba(X_scaled)[0]
    prob_disease = proba[1] * 100
    
    # Feature contributions analysis supporting calibrated classifiers and tree models
    protective_features = {"sgpt", "sgot", "alkphos"}
    contributions_list = []
    for idx, feat_name in enumerate(liver_columns):
        if hasattr(liver_model, "calibrated_classifiers_"):
            # Calibrated Classifier (ensemble over cv folds)
            if hasattr(liver_model.calibrated_classifiers_[0].estimator, "feature_importances_"):
                importance = np.mean([clf.estimator.feature_importances_ for clf in liver_model.calibrated_classifiers_], axis=0)[idx]
            else:
                importance = np.mean([abs(clf.estimator.coef_[0][idx]) for clf in liver_model.calibrated_classifiers_], axis=0)
        else:
            # Standard Classifier
            if hasattr(liver_model, "feature_importances_"):
                importance = liver_model.feature_importances_[idx]
            elif hasattr(liver_model, "coef_"):
                importance = abs(liver_model.coef_[0][idx])
            else:
                importance = 1.0
        
        val_scaled = X_scaled[0][idx]
        base_name = feat_name.replace("_log", "")
        direction = -1.0 if base_name in protective_features else 1.0
        contributions_list.append(val_scaled * importance * direction)
        
    contributions = np.array(contributions_list)
    order = np.argsort(-np.abs(contributions))[:3]
    
    friendly_names = {
        "age": "Age",
        "gender": "Gender",
        "tot_bilirubin": "Total Bilirubin",
        "direct_bilirubin": "Direct Bilirubin",
        "tot_proteins": "Alkaline Phosphotase",
        "albumin": "SGPT (ALT)",
        "ag_ratio": "SGOT (AST)",
        "sgpt": "Total Proteins",
        "sgot": "Albumin",
        "alkphos": "A/G Ratio",
        "tot_bilirubin_log": "Total Bilirubin (log)",
        "direct_bilirubin_log": "Direct Bilirubin (log)",
        "tot_proteins_log": "Alkaline Phosphotase (log)",
        "albumin_log": "SGPT (ALT) (log)",
        "ag_ratio_log": "SGOT (AST) (log)"
    }
    
    insights = []
    for idx in order:
        feat_name = liver_columns[idx]
        friendly_name = friendly_names.get(feat_name, feat_name)
        direction = "raises" if contributions[idx] > 0 else "lowers"
        insights.append({"factor": friendly_name, "effect": direction})

    return {
        "prediction": int(pred),
        "probability": float(prob_disease),
        "confidence": float(abs(prob_disease - 50.0) * 2),
        "insights": insights
    }

@app.post("/api/predict/kidney")
def predict_kidney(req: KidneyRequest):
    if not kidney_model or not kidney_scaler:
        raise HTTPException(status_code=500, detail="Kidney model not loaded")
        
    FEATURE_ORDER = [
        "age", "bp", "sg", "al", "su", "rbc", "pc", "pcc", "ba", "bgr",
        "bu", "sc", "sod", "pot", "hemo", "pcv", "wc", "rc", "htn", "dm",
        "cad", "appet", "pe", "ane",
    ]

    BINARY_MAPS = {
        "rbc":   {"normal": 1, "abnormal": 0},
        "pc":    {"normal": 1, "abnormal": 0},
        "pcc":   {"present": 1, "notpresent": 0},
        "ba":    {"present": 1, "notpresent": 0},
        "htn":   {"yes": 1, "no": 0},
        "dm":    {"yes": 1, "no": 0},
        "cad":   {"yes": 1, "no": 0},
        "appet": {"good": 0, "poor": 1},
        "pe":    {"yes": 1, "no": 0},
        "ane":   {"yes": 1, "no": 0},
    }
    
    raw = req.model_dump()
    encoded = dict(raw)
    for col, mapping in BINARY_MAPS.items():
        encoded[col] = mapping[raw[col]]
        
    input_df = pd.DataFrame([encoded])[FEATURE_ORDER]
    
    scaled_input = kidney_scaler.transform(input_df)
    prediction = kidney_model.predict(scaled_input)[0]
    
    proba = kidney_model.predict_proba(scaled_input)[0]
    class_list = list(kidney_model.classes_)
    ckd_idx = class_list.index(0)  # Class 0 is CKD
    ckd_prob = proba[ckd_idx] * 100
    
    # 0 = CKD (high risk), 1 = healthy
    return {
        "prediction": int(prediction),  # 0 or 1
        "probability": float(ckd_prob),
        "confidence": float(abs(ckd_prob - 50.0) * 2)
    }

@app.post("/api/predict/diabetes")
def predict_diabetes(req: DiabetesRequest):
    if not diabetes_model or not diabetes_scaler:
        raise HTTPException(status_code=500, detail="Diabetes model not loaded")
        
    sample = np.array([[
        req.preg,
        req.glucose,
        req.bp,
        req.skin,
        req.insulin,
        req.bmi,
        req.dpf,
        req.age
    ]])
    
    sample_scaled = diabetes_scaler.transform(sample)
    prediction = diabetes_model.predict(sample_scaled)[0]
    proba = diabetes_model.predict_proba(sample_scaled)[0]
    prob_disease = proba[1] * 100
    
    return {
        "prediction": int(prediction),
        "probability": float(prob_disease),
        "confidence": float(abs(prob_disease - 50.0) * 2)
    }

# ----------------------------
# Prediction History APIs
# ----------------------------
import json

class HistoryRecord(BaseModel):
    id: str
    patientName: str
    disease: str
    date: str
    prediction: int
    probability: float
    confidence: float
    vitals: dict

HISTORY_FILE = "history.json"

def read_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def write_history(data):
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error writing history file: {e}")

@app.get("/api/history")
def get_history():
    return read_history()

@app.post("/api/history")
def add_history(record: HistoryRecord):
    history = read_history()
    # Insert at the beginning to show newest first
    history.insert(0, record.dict())
    write_history(history)
    return {"status": "success"}

@app.delete("/api/history/{record_id}")
def delete_history_record(record_id: str):
    history = read_history()
    history = [r for r in history if r["id"] != record_id]
    write_history(history)
    return {"status": "success"}

@app.delete("/api/history")
def clear_history():
    write_history([])
    return {"status": "success"}
