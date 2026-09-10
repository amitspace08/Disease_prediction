from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class DiabetesPredictionInput(BaseModel):
    preg: float
    plas: float
    pres: float
    skin: float
    insu: float
    mass: float
    pedi: float
    age: float

class HeartPredictionInput(BaseModel):
    age: float
    sex: float
    cp: float
    trestbps: float
    chol: float
    fbs: float
    restecg: float
    thalach: float
    exang: float
    oldpeak: float
    slope: float
    ca: float
    thal: float

class LiverPredictionInput(BaseModel):
    Age: float
    Gender: str
    TB: float
    DB: float
    Alkphos: float
    Sgpt: float
    Sgot: float
    TP: float
    ALB: float
    A_G_Ratio: float = Field(alias='A/G Ratio')
    
class KidneyPredictionInput(BaseModel):
    age: Optional[float] = None
    bp: Optional[float] = None
    sg: Optional[float] = None
    al: Optional[float] = None
    su: Optional[float] = None
    rbc: Optional[str] = None
    pc: Optional[str] = None
    pcc: Optional[str] = None
    ba: Optional[str] = None
    bgr: Optional[float] = None
    bu: Optional[float] = None
    sc: Optional[float] = None
    sod: Optional[float] = None
    pot: Optional[float] = None
    hemo: Optional[float] = None
    pcv: Optional[float] = None
    wbcc: Optional[float] = None
    rbcc: Optional[float] = None
    htn: Optional[str] = None
    dm: Optional[str] = None
    cad: Optional[str] = None
    appet: Optional[str] = None
    pe: Optional[str] = None
    ane: Optional[str] = None

class PredictionResponse(BaseModel):
    disease: str
    prediction: str
    probability: float
    risk_level: str
    model_version: str
    explanation: List[Dict[str, Any]]
