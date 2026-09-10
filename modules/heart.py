import joblib
import numpy as np
import pandas as pd
import streamlit as st
from components import styles

def app():
    # 1. Inject Red Accent Theme
    st.markdown(styles.get_theme_css("#EF4444", "#991B1B"), unsafe_allow_html=True)

    # 2. Load Model Artifacts
    @st.cache_resource
    def load_model():
        model = joblib.load("models/heart/heart_model.pkl")
        columns = joblib.load("models/heart/model_columns.pkl")
        return model, columns

    try:
        model, model_columns = load_model()
    except FileNotFoundError:
        st.error("Model files not found. Make sure `heart_model.pkl` and `model_columns.pkl` are in the models/heart/ directory.")
        st.stop()

    # 3. Hero Section
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-eyebrow">💓 CARDIOVASCULAR DIAGNOSTICS</div>
            <div class="hero-title">Heart Disease Risk Analysis</div>
            <p class="hero-desc">
                Evaluate cardiovascular health parameters using a Random Forest classifier trained on clinical patient cohorts.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 4. Two-Column Dashboard Layout
    col_left, col_right = st.columns([1.2, 1], gap="large")

    # ---- LEFT COLUMN: Input Form & Illustration ----
    with col_left:
        # Medical Illustration
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 0.5rem 0; font-size:1.05rem; display:flex; align-items:center; gap:0.5rem;">🧬 Anatomical Visual</h4>', unsafe_allow_html=True)
        st.markdown(styles.get_heart_svg(), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Form card
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 1.2rem 0; font-size:1.05rem; display:flex; align-items:center; gap:0.5rem;">🫀 Patient Vital Metrics</h4>', unsafe_allow_html=True)

        patient_name = st.text_input("Patient Name", value="John Doe", key="heart_patient_name")

        r1c1, r1c2 = st.columns(2)
        with r1c1:
            age = st.number_input("Age (years)", min_value=20, max_value=100, value=54, key="heart_age")
        with r1c2:
            sex = st.radio("Gender", ["Male", "Female"], horizontal=True, key="heart_sex")

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            chest_pain = st.selectbox(
                "Chest Pain Type",
                ["ASY - Asymptomatic", "TA - Typical Angina", "ATA - Atypical Angina", "NAP - Non-Anginal Pain"],
                index=2, # ATA
                key="heart_cp"
            )
        with r2c2:
            resting_bp = st.number_input("Resting Blood Pressure (mm Hg)", min_value=80, max_value=220, value=120, key="heart_rbp")

        r3c1, r3c2 = st.columns(2)
        with r3c1:
            cholesterol = st.number_input("Cholesterol (mg/dL)", min_value=80, max_value=600, value=200, key="heart_chol")
        with r3c2:
            fasting_bs = st.radio("Fasting Blood Sugar > 120 mg/dl?", ["No", "Yes"], index=0, horizontal=True, key="heart_fbs")

        r4c1, r4c2 = st.columns(2)
        with r4c1:
            resting_ecg = st.selectbox(
                "Resting ECG",
                ["Normal", "ST - ST-T abnormality", "LVH - Left Ventricular Hypertrophy"],
                index=0,
                key="heart_ecg"
            )
        with r4c2:
            max_hr = st.number_input("Max Heart Rate Achieved (bpm)", min_value=60, max_value=220, value=150, key="heart_mhr")

        r5c1, r5c2 = st.columns(2)
        with r5c1:
            exercise_angina = st.radio("Exercise Induced Angina?", ["No", "Yes"], index=0, horizontal=True, key="heart_exang")
        with r5c2:
            oldpeak = st.number_input("Oldpeak (ST Depression)", min_value=-3.0, max_value=8.0, value=0.0, step=0.1, key="heart_oldpeak")

        st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"], index=0, key="heart_slope")

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        predict_clicked = st.button("🔍 Run Cardiovascular Diagnostic", use_container_width=True, key="heart_predict")
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- RIGHT COLUMN: Diagnostic Results ----
    with col_right:
        st.markdown('<div class="premium-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 1.2rem 0; font-size:1.05rem; display:flex; align-items:center; gap:0.5rem;">🎯 Analysis Result</h4>', unsafe_allow_html=True)

        if predict_clicked:
            # Build input row matching training columns exactly
            chest_pain_code = chest_pain.split(" - ")[0]
            resting_ecg_code = resting_ecg.split(" - ")[0]

            raw_input = {
                "Age": age,
                "RestingBP": resting_bp,
                "Cholesterol": cholesterol,
                "FastingBS": 1 if fasting_bs == "Yes" else 0,
                "MaxHR": max_hr,
                "Oldpeak": oldpeak,
                "Sex_M": 1 if sex == "Male" else 0,
                "ChestPainType_ATA": 1 if chest_pain_code == "ATA" else 0,
                "ChestPainType_NAP": 1 if chest_pain_code == "NAP" else 0,
                "ChestPainType_TA": 1 if chest_pain_code == "TA" else 0,
                "RestingECG_Normal": 1 if resting_ecg_code == "Normal" else 0,
                "RestingECG_ST": 1 if resting_ecg_code == "ST" else 0,
                "ExerciseAngina_Y": 1 if exercise_angina == "Yes" else 0,
                "ST_Slope_Flat": 1 if st_slope == "Flat" else 0,
                "ST_Slope_Up": 1 if st_slope == "Up" else 0,
            }
            input_df = pd.DataFrame([raw_input])

            # Ensure column order matches pickled list
            input_df = input_df[model_columns]

            # Run prediction
            proba = model.predict_proba(input_df)[0]
            prob_disease = proba[1] * 100
            prediction = model.predict(input_df)[0]
            high_risk = prediction == 1
            confidence = max(proba) * 100

            # Save to prediction history
            try:
                from components.history import read_history, write_history
                import time
                history_item = {
                    "id": str(int(time.time() * 1000)),
                    "patientName": patient_name if patient_name else "Unknown Patient",
                    "disease": "Heart Disease",
                    "date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "prediction": int(prediction),
                    "probability": float(prob_disease),
                    "confidence": float(confidence),
                    "vitals": {
                        "Age": f"{age} years",
                        "Gender": sex,
                        "Chest Pain Type": chest_pain,
                        "Resting BP": f"{resting_bp} mm Hg",
                        "Cholesterol": f"{cholesterol} mg/dL",
                        "Fasting BS": fasting_bs,
                        "Resting ECG": resting_ecg,
                        "Max HR": f"{max_hr} bpm",
                        "Exercise Angina": exercise_angina,
                        "Oldpeak": oldpeak,
                        "ST Slope": st_slope
                    }
                }
                history_list = read_history()
                history_list.insert(0, history_item)
                write_history(history_list)
            except Exception as history_err:
                print("Error saving Streamlit heart history:", history_err)

            # Result Header Card
            status_color = "#EF4444" if high_risk else "#22C55E"
            status_bg = "rgba(239, 68, 68, 0.08)" if high_risk else "rgba(34, 197, 94, 0.08)"
            status_border = "rgba(239, 68, 68, 0.2)" if high_risk else "rgba(34, 197, 94, 0.2)"
            status_text = "ELEVATED RISK" if high_risk else "LOW RISK DETECTED"
            status_desc = "Patient exhibits indicators of cardiovascular disease" if high_risk else "Cardiovascular metrics are within normal bounds"

            st.markdown(
                f"""
                <div class="result-status-card" style="background: {status_bg}; border: 1px solid {status_border};">
                    <div style="font-size: 2.5rem;">{'💔' if high_risk else '💚'}</div>
                    <div class="result-status-title" style="color: {status_color};">{status_text}</div>
                    <div class="result-status-desc">{status_desc}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Metrics Grid
            st.markdown(
                f"""
                <div class="metric-grid">
                    <div class="metric-box">
                        <div class="metric-val">{prob_disease:.1f}%</div>
                        <div class="metric-lbl">Risk Score</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-val">{confidence:.1f}%</div>
                        <div class="metric-lbl">Confidence</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Custom Probability Bar
            st.markdown(
                f"""
                <div class="custom-progress-container">
                    <div class="custom-progress-label-row">
                        <span>Cardiovascular Disease Probability</span>
                        <span>{prob_disease:.1f}%</span>
                    </div>
                    <div class="custom-progress-track">
                        <div class="custom-progress-bar" style="width: {prob_disease}%;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Patient Summary Tab/Box
            st.markdown(
                f"""
                <div style="background: rgba(255,255,255,0.01); border: 1px solid var(--card-border); border-radius:14px; padding:1.2rem; margin-bottom:1.5rem;">
                    <span style="font-weight:700; color:white; display:block; margin-bottom:0.8rem; font-size:0.9rem;">📋 Clinical Inputs Summary</span>
                    <table style="width:100%; font-size:0.82rem; border-collapse:collapse; color:var(--text-muted);">
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Age / Gender</td><td style="text-align:right; color:white; font-weight:500;">{age} yrs / {sex}</td></tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Chest Pain</td><td style="text-align:right; color:white; font-weight:500;">{chest_pain}</td></tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Resting Blood Pressure</td><td style="text-align:right; color:white; font-weight:500;">{resting_bp} mmHg</td></tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Cholesterol</td><td style="text-align:right; color:white; font-weight:500;">{cholesterol} mg/dL</td></tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Max Heart Rate</td><td style="text-align:right; color:white; font-weight:500;">{max_hr} bpm</td></tr>
                        <tr><td style="padding:0.4rem 0;">Oldpeak / ST Slope</td><td style="text-align:right; color:white; font-weight:500;">{oldpeak} / {st_slope}</td></tr>
                    </table>
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.expander("🔍 View Detailed Clinical Analysis"):
                st.markdown(
                    f"""
                    <table style="width:100%; font-size:0.85rem; border-collapse:collapse; color:white;">
                        <tr style="background:#131317; color:white; font-weight:700; border-bottom:1px solid #222227;">
                            <th style="padding:0.5rem; text-align:left;">Parameter</th>
                            <th style="padding:0.5rem; text-align:left;">Entered</th>
                            <th style="padding:0.5rem; text-align:left;">Ref Range</th>
                            <th style="padding:0.5rem; text-align:left;">Status</th>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:0.5rem 0.4rem;">Resting Blood Pressure</td>
                            <td>{resting_bp} mmHg</td>
                            <td>90 - 120 mmHg</td>
                            <td><span style="color:{'#EF4444' if resting_bp > 120 else '#22C55E'}; font-weight:700;">{'⚠️ Elevated' if resting_bp > 120 else '✓ Normal'}</span></td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:0.5rem 0.4rem;">Serum Cholesterol</td>
                            <td>{cholesterol} mg/dL</td>
                            <td>120 - 200 mg/dL</td>
                            <td><span style="color:{'#EF4444' if cholesterol > 200 else '#22C55E'}; font-weight:700;">{'⚠️ Elevated' if cholesterol > 200 else '✓ Normal'}</span></td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:0.5rem 0.4rem;">Max Heart Rate</td>
                            <td>{max_hr} bpm</td>
                            <td>60 - 220 bpm</td>
                            <td><span style="color:#22C55E; font-weight:700;">✓ Normal</span></td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:0.5rem 0.4rem;">Oldpeak (ST depression)</td>
                            <td>{oldpeak}</td>
                            <td>0.0 - 1.0</td>
                            <td><span style="color:{'#EF4444' if oldpeak > 1.0 else '#22C55E'}; font-weight:700;">{'⚠️ Abnormal' if oldpeak > 1.0 else '✓ Normal'}</span></td>
                        </tr>
                    </table>
                    """,
                    unsafe_allow_html=True
                )

            # Recommendations
            recos = []
            if high_risk:
                recos = [
                    "Arrange a diagnostic consultation with a cardiologist promptly.",
                    "Obtain a formal ECG/Echocardiogram diagnostic checkup.",
                    "Restrict intake of sodium, saturated fats, and high-cholesterol foods.",
                    "Monitor blood pressure daily and record spikes."
                ]
            else:
                recos = [
                    "Maintain healthy exercise levels (minimum 150 mins aerobic weekly).",
                    "Keep sodium levels under 2000mg per day.",
                    "Get blood pressure checked semi-annually.",
                    "Support a fiber-rich diet with heart-healthy omega fats."
                ]

            reco_list_html = "".join([f'<div class="reco-item"><span>•</span><span>{r}</span></div>' for r in recos])
            st.markdown(
                f"""
                <div class="reco-container">
                    <div class="reco-title">💡 Recommendations</div>
                    {reco_list_html}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            # Placeholder before prediction
            st.markdown(
                """
                <div style="text-align:center; padding: 5rem 1rem; color:var(--text-muted);">
                    <div style="font-size:2.8rem; margin-bottom:1rem; opacity:0.6;">🩺</div>
                    <span style="font-weight:600; font-size:0.95rem; color:white; display:block; margin-bottom:0.3rem;">Awaiting Metrics</span>
                    Please fill out the patient metrics in the left panel and click <b>Run Cardiovascular Diagnostic</b> to generate the report.
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Medical Disclaimer
        st.markdown(
            """
            <div class="disclaimer-text">
                <b>Medical Disclaimer:</b> This diagnostic assessment is generated dynamically using an artificial intelligence classification model. It is designed to act as an indicative screening utility and is <b>not a clinical diagnostic finding</b>. Always confirm these estimations with certified laboratory testing and professional cardiological consultations.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)