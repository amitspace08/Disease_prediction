import joblib
import numpy as np
import pandas as pd
import streamlit as st
from components import styles

def app():
    # 1. Inject Blue Accent Theme
    st.markdown(styles.get_theme_css("#3B82F6", "#1D4ED8"), unsafe_allow_html=True)

    # 2. Config & Meta Definitions
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

    CLASS_LABELS = {0: "Chronic Kidney Disease (CKD)", 1: "No Kidney Disease (Healthy)"}

    DEFAULTS = {
        "age": 50.0, "bp": 80.0, "sg": 1.020, "al": 0.0, "su": 0.0,
        "bgr": 120.0, "bu": 40.0, "sc": 1.2, "sod": 138.0, "pot": 4.5,
        "hemo": 13.5, "pcv": 41.0, "wc": 8000.0, "rc": 5.0,
    }

    # 3. Load Model Artifacts
    @st.cache_resource
    def load_artifacts():
        try:
            model = joblib.load("models/kidney/kidney_model.pkl")
            scaler = joblib.load("models/kidney/scaler.pkl")
            return model, scaler
        except FileNotFoundError:
            st.error("Model files not found. Make sure kidney_model.pkl and scaler.pkl are available in models/kidney/")
            st.stop()

    model, scaler = load_artifacts()

    # 4. Hero Section
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-eyebrow">🫘 NEPHROLOGY & RENAL HEALTH</div>
            <div class="hero-title">Chronic Kidney Disease Predictor</div>
            <p class="hero-desc">
                Analyze clinical inputs and glomerular values to estimate the risk of Chronic Kidney Disease (CKD).
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 5. Two-Column Dashboard Layout
    col_left, col_right = st.columns([1.2, 1], gap="large")

    # ---- LEFT COLUMN: Grouped Inputs & Illustration ----
    with col_left:
        # Illustration card
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 0.5rem 0; font-size:1.05rem; display:flex; align-items:center; gap:0.5rem;">🧬 Anatomical Visual</h4>', unsafe_allow_html=True)
        st.markdown(styles.get_kidney_svg(), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Form card
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 1.2rem 0; font-size:1.05rem; display:flex; align-items:center; gap:0.5rem;">🫘 Comprehensive Nephrology Form</h4>', unsafe_allow_html=True)

        patient_name = st.text_input("Patient Name", value="John Doe", key="kidney_patient_name")

        # Group 1: Demographics & Vitals
        st.markdown("<span style='font-size: 0.88rem; font-weight:600; color:white; display:block; margin-bottom: 0.8rem;'>🩺 1. Demographics & Vitals</span>", unsafe_allow_html=True)
        g1c1, g1c2 = st.columns(2)
        with g1c1:
            age = st.number_input("Age (years)", min_value=0.0, max_value=120.0, value=DEFAULTS["age"], step=1.0, key="kidney_age")
            htn = st.radio("Hypertension?", ["no", "yes"], index=0, horizontal=True, key="kidney_htn")
            cad = st.radio("Coronary Artery Disease?", ["no", "yes"], horizontal=True, key="kidney_cad")
        with g1c2:
            bp = st.number_input("Blood Pressure (mm/Hg)", min_value=0.0, max_value=300.0, value=DEFAULTS["bp"], step=1.0, key="kidney_bp")
            dm = st.radio("Diabetes Mellitus?", ["no", "yes"], index=0, horizontal=True, key="kidney_dm")

        st.markdown("<hr style='border-color: var(--card-border); margin:1.2rem 0;'>", unsafe_allow_html=True)

        # Group 2: Urine Analysis
        st.markdown("<span style='font-size: 0.88rem; font-weight:600; color:white; display:block; margin-bottom: 0.8rem;'>🧪 2. Urine Observations</span>", unsafe_allow_html=True)
        g2c1, g2c2 = st.columns(2)
        with g2c1:
            sg = st.number_input("Specific Gravity", min_value=1.000, max_value=1.040, value=DEFAULTS["sg"], step=0.005, format="%.3f", key="kidney_sg")
            al = st.selectbox("Albumin (0–5 scale)", options=[0, 1, 2, 3, 4, 5], index=0, key="kidney_al")
            rbc = st.radio("Red Blood Cells in Urine", ["normal", "abnormal"], index=0, horizontal=True, key="kidney_rbc")
            pcc = st.radio("Pus Cell Clumps", ["notpresent", "present"], index=0, horizontal=True, key="kidney_pcc")
        with g2c2:
            su = st.selectbox("Sugar (0–5 scale)", options=[0, 1, 2, 3, 4, 5], index=0, key="kidney_su")
            pc = st.radio("Pus Cells in Urine", ["normal", "abnormal"], index=0, horizontal=True, key="kidney_pc")
            ba = st.radio("Bacteria in Urine", ["notpresent", "present"], horizontal=True, key="kidney_ba")

        st.markdown("<hr style='border-color: var(--card-border); margin:1.2rem 0;'>", unsafe_allow_html=True)

        # Group 3: Blood Chemistry & Metrics
        st.markdown("<span style='font-size: 0.88rem; font-weight:600; color:white; display:block; margin-bottom: 0.8rem;'>🩸 3. Blood Panel Chemistry</span>", unsafe_allow_html=True)
        g3c1, g3c2 = st.columns(2)
        with g3c1:
            bgr = st.number_input("Blood Glucose Random (mgs/dl)", min_value=0.0, value=DEFAULTS["bgr"], step=1.0, key="kidney_bgr")
            sc = st.number_input("Serum Creatinine (mgs/dl)", min_value=0.0, value=DEFAULTS["sc"], step=0.1, key="kidney_sc")
            pot = st.number_input("Potassium (mEq/L)", min_value=0.0, value=DEFAULTS["pot"], step=0.1, key="kidney_pot")
            pcv = st.number_input("Packed Cell Volume (%)", min_value=0.0, max_value=100.0, value=DEFAULTS["pcv"], step=1.0, key="kidney_pcv")
            rc = st.number_input("Red Blood Cell Count (m/cumm)", min_value=0.0, max_value=10.0, value=DEFAULTS["rc"], step=0.1, key="kidney_rc")
            appet = st.radio("Appetite", ["good", "poor"], index=0, horizontal=True, key="kidney_appet")
            ane = st.radio("Anemia?", ["no", "yes"], index=0, horizontal=True, key="kidney_ane")
        with g3c2:
            bu = st.number_input("Blood Urea (mgs/dl)", min_value=0.0, value=DEFAULTS["bu"], step=1.0, key="kidney_bu")
            sod = st.number_input("Sodium (mEq/L)", min_value=0.0, value=DEFAULTS["sod"], step=0.5, key="kidney_sod")
            hemo = st.number_input("Hemoglobin (gms)", min_value=0.0, max_value=20.0, value=DEFAULTS["hemo"], step=0.1, key="kidney_hemo")
            wc = st.number_input("WBC Count (cells/cumm)", min_value=0.0, value=DEFAULTS["wc"], step=100.0, key="kidney_wc")
            pe = st.radio("Pedal Edema?", ["no", "yes"], index=0, horizontal=True, key="kidney_pe")

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        predict_clicked = st.button("🔍 Run Renal Analysis", use_container_width=True, key="kidney_predict")
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- RIGHT COLUMN: Diagnostic Results ----
    with col_right:
        st.markdown('<div class="premium-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 1.2rem 0; font-size:1.05rem; display:flex; align-items:center; gap:0.5rem;">🎯 Analysis Result</h4>', unsafe_allow_html=True)

        if predict_clicked:
            raw_input = {
                "age": age, "bp": bp, "sg": sg, "al": al, "su": su,
                "rbc": rbc, "pc": pc, "pcc": pcc, "ba": ba,
                "bgr": bgr, "bu": bu, "sc": sc, "sod": sod, "pot": pot,
                "hemo": hemo, "pcv": pcv, "wc": wc, "rc": rc,
                "htn": htn, "dm": dm, "cad": cad, "appet": appet, "pe": pe, "ane": ane,
            }

            # Map categorical variables
            encoded_input = dict(raw_input)
            for col, mapping in BINARY_MAPS.items():
                encoded_input[col] = mapping[raw_input[col]]

            # Convert to DataFrame in exact feature order
            input_df = pd.DataFrame([encoded_input])[FEATURE_ORDER]

            try:
                # Scale and Predict
                scaled_input = scaler.transform(input_df)
                prediction = model.predict(scaled_input)[0]

                # Compute probability for CKD class (0)
                ckd_prob = None
                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(scaled_input)[0]
                    class_list = list(model.classes_)
                    ckd_idx = class_list.index(0)  # Class 0 is CKD
                    ckd_prob = proba[ckd_idx] * 100

                high_risk = prediction == 0  # 0 is CKD
                confidence = (ckd_prob if high_risk else (100.0 - ckd_prob)) if ckd_prob is not None else 98.0
                prob_pct = ckd_prob if ckd_prob is not None else (100.0 if high_risk else 0.0)

                # Save to prediction history
                try:
                    from components.history import read_history, write_history
                    import time
                    history_item = {
                        "id": str(int(time.time() * 1000)),
                        "patientName": patient_name if patient_name else "Unknown Patient",
                        "disease": "Kidney Disease",
                        "date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "prediction": int(prediction),
                        "probability": float(prob_pct),
                        "confidence": float(confidence),
                        "vitals": {
                            "Age": f"{age} years",
                            "Gender": gender,
                            "Blood Pressure": f"{bp} mm Hg",
                            "Specific Gravity": sg,
                            "Albumin": al,
                            "Sugar": su,
                            "Red Blood Cells": rbc,
                            "Pus Cell": pc,
                            "Pus Cell Clumps": pcc,
                            "Bacteria": ba,
                            "Blood Glucose Random": f"{bgr} mg/dL",
                            "Blood Urea": f"{bu} mg/dL",
                            "Serum Creatinine": f"{sc} mg/dL",
                            "Sodium": f"{sod} mEq/L",
                            "Potassium": f"{pot} mEq/L",
                            "Hemoglobin": f"{hemo} g/dL",
                            "Packed Cell Volume": pcv,
                            "White Blood Cell Count": f"{wc} cells/cumm",
                            "Red Blood Cell Count": f"{rc} millions/cmm",
                            "Hypertension": htn,
                            "Diabetes Mellitus": dm,
                            "Coronary Artery Disease": cad,
                            "Appetite": appet,
                            "Pedal Edema": pe,
                            "Anemia": ane
                        }
                    }
                    history_list = read_history()
                    history_list.insert(0, history_item)
                    write_history(history_list)
                except Exception as history_err:
                    print("Error saving Streamlit kidney history:", history_err)

                # Result Header Card
                status_color = "#EF4444" if high_risk else "#22C55E"
                status_bg = "rgba(239, 68, 68, 0.08)" if high_risk else "rgba(34, 197, 94, 0.08)"
                status_border = "rgba(239, 68, 68, 0.2)" if high_risk else "rgba(34, 197, 94, 0.2)"
                status_text = "ELEVATED RISK" if high_risk else "LOW RISK DETECTED"
                status_desc = "Patient parameters correlate with Chronic Kidney Disease" if high_risk else "Kidney biomarkers are within healthy ranges"

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
                            <div class="metric-val">{prob_pct:.1f}%</div>
                            <div class="metric-lbl">CKD Risk Score</div>
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
                            <span>Kidney Disease Probability</span>
                            <span>{prob_pct:.1f}%</span>
                        </div>
                        <div class="custom-progress-track">
                            <div class="custom-progress-bar" style="width: {prob_pct}%;"></div>
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
                            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Age / Blood Pressure</td><td style="text-align:right; color:white; font-weight:500;">{age:.0f} yrs / {bp:.0f} mmHg</td></tr>
                            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Specific Gravity</td><td style="text-align:right; color:white; font-weight:500;">{sg:.3f}</td></tr>
                            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Albumin / Sugar (0-5)</td><td style="text-align:right; color:white; font-weight:500;">{al} / {su}</td></tr>
                            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Serum Creatinine</td><td style="text-align:right; color:white; font-weight:500;">{sc:.1f} mgs/dl</td></tr>
                            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Hemoglobin / Packed Cell</td><td style="text-align:right; color:white; font-weight:500;">{hemo:.1f} gms / {pcv:.0f}%</td></tr>
                            <tr><td style="padding:0.4rem 0;">Hypertension / Diabetes</td><td style="text-align:right; color:white; font-weight:500;">{htn.upper()} / {dm.upper()}</td></tr>
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
                                <td style="padding:0.5rem 0.4rem;">Blood Pressure</td>
                                <td>{bp} mmHg</td>
                                <td>60 - 90 mmHg</td>
                                <td><span style="color:{'#EF4444' if bp > 90 else '#22C55E'}; font-weight:700;">{'⚠️ Elevated' if bp > 90 else '✓ Normal'}</span></td>
                            </tr>
                            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                                <td style="padding:0.5rem 0.4rem;">Specific Gravity</td>
                                <td>{sg:.3f}</td>
                                <td>1.010 - 1.025</td>
                                <td><span style="color:{'#EF4444' if (sg < 1.010 or sg > 1.025) else '#22C55E'}; font-weight:700;">{'⚠️ Out of Range' if (sg < 1.010 or sg > 1.025) else '✓ Normal'}</span></td>
                            </tr>
                            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                                <td style="padding:0.5rem 0.4rem;">Albumin (urine)</td>
                                <td>{al}</td>
                                <td>0</td>
                                <td><span style="color:{'#EF4444' if int(al) > 0 else '#22C55E'}; font-weight:700;">{'⚠️ Proteinuria' if int(al) > 0 else '✓ Normal'}</span></td>
                            </tr>
                            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                                <td style="padding:0.5rem 0.4rem;">Sugar (urine)</td>
                                <td>{su}</td>
                                <td>0</td>
                                <td><span style="color:{'#EF4444' if int(su) > 0 else '#22C55E'}; font-weight:700;">{'⚠️ Glycosuria' if int(su) > 0 else '✓ Normal'}</span></td>
                            </tr>
                            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                                <td style="padding:0.5rem 0.4rem;">Serum Creatinine</td>
                                <td>{sc:.1f} mg/dL</td>
                                <td>0.5 - 1.2 mg/dL</td>
                                <td><span style="color:{'#EF4444' if sc > 1.2 else '#22C55E'}; font-weight:700;">{'⚠️ Elevated' if sc > 1.2 else '✓ Normal'}</span></td>
                            </tr>
                            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                                <td style="padding:0.5rem 0.4rem;">Blood Urea</td>
                                <td>{bu:.1f} mg/dL</td>
                                <td>7 - 20 mg/dL</td>
                                <td><span style="color:{'#EF4444' if bu > 20 else '#22C55E'}; font-weight:700;">{'⚠️ Elevated' if bu > 20 else '✓ Normal'}</span></td>
                            </tr>
                            <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                                <td style="padding:0.5rem 0.4rem;">Hemoglobin</td>
                                <td>{hemo:.1f} g/dL</td>
                                <td>12.0 - 16.0 g/dL</td>
                                <td><span style="color:{'#EF4444' if hemo < 12.0 else '#22C55E'}; font-weight:700;">{'⚠️ Low (Anemia)' if hemo < 12.0 else '✓ Normal'}</span></td>
                            </tr>
                        </table>
                        """,
                        unsafe_allow_html=True
                    )

                # Recommendations
                recos = []
                if high_risk:
                    recos = [
                        "Arrange an urgent consultation with a nephrologist.",
                        "Obtain blood pressure and serum creatinine clearance diagnostic monitors.",
                        "Follow a kidney-healthy diet: restrict potassium, sodium, and heavy proteins.",
                        "Establish active blood glucose management protocols."
                    ]
                else:
                    recos = [
                        "Maintain adequate fluid intake (2-3 liters of water daily).",
                        "Avoid chronic over-use of NSAIDs (painkillers like ibuprofen).",
                        "Perform an annual renal panel checkup (Serum Creatinine and EGFR).",
                        "Support active cardiovascular and blood pressure control."
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

            except Exception as e:
                st.error(f"Renal Prediction System Error: {e}")

        else:
            # Placeholder before prediction
            st.markdown(
                """
                <div style="text-align:center; padding: 5rem 1rem; color:var(--text-muted);">
                    <div style="font-size:2.8rem; margin-bottom:1rem; opacity:0.6;">🩺</div>
                    <span style="font-weight:600; font-size:0.95rem; color:white; display:block; margin-bottom:0.3rem;">Awaiting Metrics</span>
                    Please fill out the patient metrics in the left panel and click <b>Run Renal Analysis</b> to generate the report.
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Medical Disclaimer
        st.markdown(
            """
            <div class="disclaimer-text">
                <b>Medical Disclaimer:</b> This diagnostic assessment is generated dynamically using an artificial intelligence classification model. It is designed to act as an indicative screening utility and is <b>not a clinical diagnostic finding</b>. Always confirm these estimations with certified laboratory testing and professional nephrological consultations.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)