import os
import pandas as pd
from ucimlrepo import fetch_ucirepo

def download_diabetes(data_dir):
    print("Fetching Diabetes dataset (openml/scikit-learn is easier but let's try fetch_openml)...")
    from sklearn.datasets import fetch_openml
    # Pima Indians Diabetes is id 37
    diabetes = fetch_openml(data_id=37, as_frame=True, parser='auto')
    df = diabetes.frame
    df.to_csv(os.path.join(data_dir, "diabetes.csv"), index=False)
    print("Diabetes dataset saved.")

def download_heart(data_dir):
    print("Fetching Heart Disease dataset...")
    # fetch dataset 
    heart_disease = fetch_ucirepo(id=45) 
    X = heart_disease.data.features 
    y = heart_disease.data.targets 
    df = pd.concat([X, y], axis=1)
    df.to_csv(os.path.join(data_dir, "heart.csv"), index=False)
    print("Heart dataset saved.")

def download_liver(data_dir):
    print("Fetching Liver Disease dataset...")
    # fetch dataset 
    ilpd = fetch_ucirepo(id=225) 
    X = ilpd.data.features 
    y = ilpd.data.targets 
    df = pd.concat([X, y], axis=1)
    df.to_csv(os.path.join(data_dir, "liver.csv"), index=False)
    print("Liver dataset saved.")

def download_kidney(data_dir):
    print("Fetching Kidney Disease dataset...")
    # fetch dataset 
    chronic_kidney_disease = fetch_ucirepo(id=336) 
    X = chronic_kidney_disease.data.features 
    y = chronic_kidney_disease.data.targets 
    df = pd.concat([X, y], axis=1)
    df.to_csv(os.path.join(data_dir, "kidney.csv"), index=False)
    print("Kidney dataset saved.")

if __name__ == "__main__":
    data_dir = os.path.join("..", "data")
    os.makedirs(data_dir, exist_ok=True)
    
    download_diabetes(data_dir)
    download_heart(data_dir)
    download_liver(data_dir)
    download_kidney(data_dir)
    print("All datasets downloaded successfully.")
