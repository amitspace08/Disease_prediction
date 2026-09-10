import joblib
import numpy as np
import pandas as pd
import streamlit as st
from components import styles

def app():
    # 1. Inject Blue Accent Theme
    st.markdown(styles.get_theme_css("#3B82F6", "#1D4ED8"), unsafe_allow_html=True)

    # 2. Load Model Artifacts
    @st.cache_resource
    def load_artifacts():
        try:
            model = joblib.load("models/diabetes/diabetes_model.pkl")
            scaler = joblib.load("models/diabetes/scaler.pkl")
            return model, scaler
        except FileNotFoundError:
            st.error("Model files not found. Make sure diabetes_model.pkl and scaler.pkl are available in models/diabetes/")
            st.stop()

    model, scaler = load_artifacts()

    # 3. Hero Section
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-eyebrow">🩸 ENDOCRINOLOGY & DIABETES SCREENING</div>
            <div class="hero-title">Diabetes Prediction System</div>
            <p class="hero-desc">
                Evaluate blood glucose tolerances, insulin indices, and demographic factors to predict diabetes mellitus.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 4. Two-Column Dashboard Layout
    col_left, col_right = st.columns([1.2, 1], gap="large")

    # ---- LEFT COLUMN: Input Form & Illustration ----
    with col_left:
        # Illustration card
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 0.5rem 0; font-size:1.05rem; display:flex; align-items:center; gap:0.5rem;">🧬 Anatomical Visual</h4>', unsafe_allow_html=True)
        st.markdown(styles.get_diabetes_svg(), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Form card
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 1.2rem 0; font-size:1.05rem; display:flex; align-items:center; gap:0.5rem;">🩸 Endocrine Vital Metrics</h4>', unsafe_allow_html=True)

        patient_name = st.text_input("Patient Name", value="John Doe", key="diab_patient_name")

        r1c1, r1c2 = st.columns(2)
        with r1c1:
            preg = st.number_input("Pregnancies", min_value=0, max_value=20, value=2, key="diab_preg")
            bp = st.number_input("Blood Pressure (mm Hg)", min_value=0, max_value=200, value=75, key="diab_bp")
        with r1c2:
            glucose = st.number_input("Plasma Glucose Concentration (2hr tolerance)", min_value=0, max_value=300, value=100, key="diab_glucose")
            skin = st.number_input("Triceps Skin Fold Thickness (mm)", min_value=0, max_value=100, value=20, key="diab_skin")

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            insulin = st.number_input("2-Hour Serum Insulin (mu U/ml)", min_value=0, max_value=900, value=85, key="diab_ins")
            dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=3.0, value=0.35, step=0.01, key="diab_dpf")
        with r2c2:
            bmi = st.number_input("Body Mass Index (weight in kg/(height in m)^2)", min_value=0, max_value=70, value=24, key="diab_bmi")
            age = st.number_input("Age (years)", min_value=1, max_value=110, value=30, key="diab_age")

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        predict_clicked = st.button("🔍 Run Diabetes Assessment", use_container_width=True, key="diab_predict")
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- RIGHT COLUMN: Diagnostic Results ----
    with col_right:
        st.markdown('<div class="premium-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 1.2rem 0; font-size:1.05rem; display:flex; align-items:center; gap:0.5rem;">🎯 Analysis Result</h4>', unsafe_allow_html=True)

        if predict_clicked:
            # Create sample input array
            sample = np.array([[
                preg,
                glucose,
                bp,
                skin,
                insulin,
                bmi,
                dpf,
                age
            ]])

            # Scale input
            sample_scaled = scaler.transform(sample)

            # Predict & Probability
            prediction = model.predict(sample_scaled)[0]
            probability = model.predict_proba(sample_scaled)[0][1] * 100
            
            high_risk = prediction == 1
            confidence = max(model.predict_proba(sample_scaled)[0]) * 100

            # Save to prediction history
            try:
                from components.history import read_history, write_history
                import time
                history_item = {
                    "id": str(int(time.time() * 1000)),
                    "patientName": patient_name if patient_name else "Unknown Patient",
                    "disease": "Diabetes",
                    "date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "prediction": int(prediction),
                    "probability": float(probability),
                    "confidence": float(confidence),
                    "vitals": {
                        "Age": f"{age} years",
                        "Pregnancies": preg,
                        "Glucose": f"{glucose} mg/dL",
                        "Blood Pressure": f"{bp} mm Hg",
                        "Skin Thickness": f"{skin} mm",
                        "Insulin": f"{insulin} mu U/ml",
                        "BMI": bmi,
                        "Diabetes Pedigree": dpf
                    }
                }
                history_list = read_history()
                history_list.insert(0, history_item)
                write_history(history_list)
            except Exception as history_err:
                print("Error saving Streamlit diabetes history:", history_err)

            # Result Header Card
            status_color = "#EF4444" if high_risk else "#22C55E"
            status_bg = "rgba(239, 68, 68, 0.08)" if high_risk else "rgba(34, 197, 94, 0.08)"
            status_border = "rgba(239, 68, 68, 0.2)" if high_risk else "rgba(34, 197, 94, 0.2)"
            status_text = "ELEVATED RISK" if high_risk else "LOW RISK DETECTED"
            status_desc = "Patient parameters correlate with diabetes mellitus" if high_risk else "Endocrine metrics are within normal bounds"

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
                        <div class="metric-val">{probability:.1f}%</div>
                        <div class="metric-lbl">Diabetes Risk</div>
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
                        <span>Diabetes Probability</span>
                        <span>{probability:.1f}%</span>
                    </div>
                    <div class="custom-progress-track">
                        <div class="custom-progress-bar" style="width: {probability}%;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Patient Summary Box
            st.markdown(
                f"""
                <div style="background: rgba(255,255,255,0.01); border: 1px solid var(--card-border); border-radius:14px; padding:1.2rem; margin-bottom:1.5rem;">
                    <span style="font-weight:700; color:white; display:block; margin-bottom:0.8rem; font-size:0.9rem;">📋 Clinical Inputs Summary</span>
                    <table style="width:100%; font-size:0.82rem; border-collapse:collapse; color:var(--text-muted);">
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Age / Pregnancies</td><td style="text-align:right; color:white; font-weight:500;">{age} yrs / {preg}</td></tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Glucose Tolerance (2hr)</td><td style="text-align:right; color:white; font-weight:500;">{glucose} mg/dL</td></tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Blood Pressure</td><td style="text-align:right; color:white; font-weight:500;">{bp} mmHg</td></tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Skin Thickness / Insulin</td><td style="text-align:right; color:white; font-weight:500;">{skin} mm / {insulin} mu U/ml</td></tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Body Mass Index (BMI)</td><td style="text-align:right; color:white; font-weight:500;">{bmi:.1f}</td></tr>
                        <tr><td style="padding:0.4rem 0;">Diabetes Pedigree Score</td><td style="text-align:right; color:white; font-weight:500;">{dpf:.3f}</td></tr>
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
                            <td style="padding:0.5rem 0.4rem;">Plasma Glucose (2h)</td>
                            <td>{glucose} mg/dL</td>
                            <td>70 - 140 mg/dL</td>
                            <td><span style="color:{'#EF4444' if glucose >= 140 else '#22C55E'}; font-weight:700;">{'⚠️ Elevated' if glucose >= 140 else '✓ Normal'}</span></td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:0.5rem 0.4rem;">Blood Pressure</td>
                            <td>{bp} mmHg</td>
                            <td>60 - 80 mmHg</td>
                            <td><span style="color:{'#EF4444' if bp >= 80 else '#22C55E'}; font-weight:700;">{'⚠️ Elevated' if bp >= 80 else '✓ Normal'}</span></td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:0.5rem 0.4rem;">Body Mass Index (BMI)</td>
                            <td>{bmi:.1f} kg/m²</td>
                            <td>18.5 - 25.0 kg/m²</td>
                            <td><span style="color:{'#EF4444' if bmi >= 25.0 else '#22C55E'}; font-weight:700;">{'⚠️ Overweight' if bmi >= 25.0 else '✓ Normal'}</span></td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:0.5rem 0.4rem;">Serum Insulin (2h)</td>
                            <td>{insulin} mu U/ml</td>
                            <td>15 - 160 mu U/ml</td>
                            <td><span style="color:{'#EF4444' if (insulin < 15 or insulin > 160) else '#22C55E'}; font-weight:700;">{'⚠️ Abnormal' if (insulin < 15 or insulin > 160) else '✓ Normal'}</span></td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:0.5rem 0.4rem;">Triceps Skin Thickness</td>
                            <td>{skin} mm</td>
                            <td>10 - 30 mm</td>
                            <td><span style="color:{'#EF4444' if (skin < 10 or skin > 30) else '#22C55E'}; font-weight:700;">{'⚠️ Abnormal' if (skin < 10 or skin > 30) else '✓ Normal'}</span></td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:0.5rem 0.4rem;">Diabetes Pedigree Function</td>
                            <td>{dpf:.3f}</td>
                            <td>0.0 - 0.8</td>
                            <td><span style="color:{'#EF4444' if dpf >= 0.8 else '#22C55E'}; font-weight:700;">{'⚠️ High Risk' if dpf >= 0.8 else '✓ Normal'}</span></td>
                        </tr>
                    </table>
                    """,
                    unsafe_allow_html=True
                )

            # Recommendations
            recos = []
            if high_risk:
                recos = [
                    "Consult an endocrinologist or primary care physician.",
                    "Engage in structured, low-impact exercise regularly.",
                    "Reduce sugar, carbohydrate, and high glycemic food intakes.",
                    "Monitor fasting and postprandial blood glucose levels daily."
                ]
            else:
                recos = [
                    "Maintain a balanced diet rich in fibers and complex carbs.",
                    "Engage in moderate physical exercise regularly.",
                    "Stay well hydrated throughout the day.",
                    "Maintain a healthy weight profile and check BMI semi-annually."
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
                    Please fill out the patient metrics in the left panel and click <b>Run Diabetes Assessment</b> to generate the report.
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Medical Disclaimer
        st.markdown(
            """
            <div class="disclaimer-text">
                <b>Medical Disclaimer:</b> This diagnostic assessment is generated dynamically using an artificial intelligence classification model. It is designed to act as an indicative screening utility and is <b>not a clinical diagnostic finding</b>. Always confirm these estimations with certified laboratory testing and professional endocrinological consultations.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)