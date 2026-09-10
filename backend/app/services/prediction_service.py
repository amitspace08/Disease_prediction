import os
import joblib
import pandas as pd
import shap
from typing import Dict, Any

class PredictionService:
    def __init__(self):
        self.models = {}
        self.features = {}
        self.explainers = {}
        self._load_models()

    def _load_models(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        models_dir = os.path.join(base_dir, 'models')
        
        diseases = ['diabetes', 'heart', 'liver', 'kidney']
        for d in diseases:
            model_path = os.path.join(models_dir, d, 'model.pkl')
            features_path = os.path.join(models_dir, d, 'features.pkl')
            if os.path.exists(model_path) and os.path.exists(features_path):
                model = joblib.load(model_path)
                self.models[d] = model
                self.features[d] = joblib.load(features_path)
                
                # Initialize SHAP explainer
                # If it's a pipeline, get the classifier step
                if hasattr(model, 'named_steps'):
                    clf = model.named_steps.get('classifier', model)
                    try:
                        self.explainers[d] = shap.TreeExplainer(clf)
                    except Exception as e:
                        print(f"Warning: Could not create TreeExplainer for {d}: {e}")
                else:
                    self.explainers[d] = shap.TreeExplainer(model)
            else:
                print(f"Warning: Model for {d} not found at {model_path}")

    def predict(self, disease: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        if disease not in self.models:
            raise ValueError(f"Model for {disease} is not loaded.")
        
        model = self.models[disease]
        feature_names = self.features[disease]
        
        df = pd.DataFrame([input_data])
        
        for feat in feature_names:
            if feat not in df.columns:
                alt_feat = feat.replace('/', '_').replace(' ', '_')
                if alt_feat in df.columns:
                    df = df.rename(columns={alt_feat: feat})
                else:
                    df[feat] = None
        
        df = df[feature_names]
        
        probability = float(model.predict_proba(df)[0][1])
        prediction_class = int(model.predict(df)[0])
        
        if probability < 0.3:
            risk_level = "Low"
            prediction_label = "Low Risk"
        elif probability < 0.7:
            risk_level = "Moderate"
            prediction_label = "Moderate Risk"
        else:
            risk_level = "High"
            prediction_label = "High Risk"
            
        # SHAP Explanation
        explanation_list = []
        if disease in self.explainers:
            try:
                # Need to preprocess data if it's a pipeline before passing to TreeExplainer
                if hasattr(model, 'named_steps'):
                    preprocessor = None
                    if 'preprocessor' in model.named_steps:
                        preprocessor = model.named_steps['preprocessor']
                    elif 'scaler' in model.named_steps or 'imputer' in model.named_steps:
                        # Reconstruct basic pipeline
                        from sklearn.pipeline import Pipeline
                        steps = []
                        for name, step in model.named_steps.items():
                            if name != 'classifier':
                                steps.append((name, step))
                        if steps:
                            preprocessor = Pipeline(steps)
                            
                    if preprocessor:
                        X_transformed = preprocessor.transform(df)
                        if hasattr(X_transformed, 'toarray'):
                            X_transformed = X_transformed.toarray()
                    else:
                        X_transformed = df.values
                else:
                    X_transformed = df.values
                
                shap_values = self.explainers[disease].shap_values(X_transformed)
                
                # shap_values could be a list (multiclass) or array (binary)
                if isinstance(shap_values, list):
                    vals = shap_values[1][0]
                else:
                    vals = shap_values[0]
                    
                # Pair features with their SHAP values
                # Note: if ColumnTransformer changed the number of features (e.g. OneHotEncoder), 
                # feature names won't directly map.
                # For simplicity, if lengths match, we zip.
                if len(vals) == len(feature_names):
                    for i, feat in enumerate(feature_names):
                        explanation_list.append({
                            "feature": feat,
                            "contribution": float(vals[i]),
                            "value": float(df.iloc[0, i]) if pd.api.types.is_numeric_dtype(df.iloc[0, i]) else str(df.iloc[0, i])
                        })
                    
                    # Sort by absolute contribution
                    explanation_list.sort(key=lambda x: abs(x["contribution"]), reverse=True)
            except Exception as e:
                print(f"SHAP explanation failed for {disease}: {e}")
                
        return {
            "disease": disease,
            "prediction": prediction_label,
            "probability": round(probability, 4),
            "risk_level": risk_level,
            "model_version": f"{disease}_xgboost_v1",
            "explanation": explanation_list[:5] # Top 5 factors
        }

prediction_service = PredictionService()
