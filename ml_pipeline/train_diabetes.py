import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def train_diabetes():
    print("Training Diabetes Model...")
    data_path = os.path.join("data", "diabetes.csv")
    df = pd.read_csv(data_path)
    
    # Target column for Pima is usually 'class'
    target_col = 'class'
    if target_col not in df.columns:
        # Check if it's named something else
        target_col = df.columns[-1]
    
    # Map target values to 0/1
    if df[target_col].dtype in ['object', 'category', 'string'] or isinstance(df[target_col].iloc[0], str):
        df[target_col] = df[target_col].map({'tested_negative': 0, 'tested_positive': 1})
        
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Some features have 0 as missing value. E.g., Glucose, BloodPressure, SkinThickness, Insulin, BMI
    # Let's replace 0 with NaN for these columns so imputer can handle them.
    cols_with_zeros = ['plas', 'pres', 'skin', 'insu', 'mass']
    for col in cols_with_zeros:
        if col in X.columns:
            X[col] = X[col].replace(0, np.nan)
            
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('classifier', XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss'))
    ])
    
    # Hyperparameter tuning
    param_grid = {
        'classifier__n_estimators': [50, 100],
        'classifier__max_depth': [3, 5],
        'classifier__learning_rate': [0.01, 0.1]
    }
    
    grid = GridSearchCV(pipeline, param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
    grid.fit(X_train, y_train)
    
    best_model = grid.best_estimator_
    
    # Evaluation
    y_pred = best_model.predict(X_test)
    y_prob = best_model.predict_proba(X_test)[:, 1]
    
    print("Diabetes Model Metrics:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall: {recall_score(y_test, y_pred):.4f}")
    print(f"F1-score: {f1_score(y_test, y_pred):.4f}")
    print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")
    
    # Save model
    model_dir = os.path.join("models", "diabetes")
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(best_model, os.path.join(model_dir, "model.pkl"))
    # Save feature names for SHAP
    joblib.dump(list(X.columns), os.path.join(model_dir, "features.pkl"))
    print("Diabetes model saved.")

if __name__ == "__main__":
    train_diabetes()
