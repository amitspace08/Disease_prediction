import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from components import styles

def app():
    # 1. Inject Green Accent Theme
    st.markdown(styles.get_theme_css("#22C55E", "#15803D"), unsafe_allow_html=True)

    # 2. Config & Meta Definitions
    LOG_COLS = ["tot_bilirubin", "direct_bilirubin", "tot_proteins", "albumin", "ag_ratio"]

    FIELD_META = {
        "tot_bilirubin": dict(label="Total Bilirubin", unit="mg/dL", low=0.1, high=1.2, absmin=0.1, absmax=8.0, default=0.8, step=0.1),
        "direct_bilirubin": dict(label="Direct Bilirubin", unit="mg/dL", low=0.0, high=0.3, absmin=0.0, absmax=4.0, default=0.2, step=0.1),
        "tot_proteins": dict(label="Alkaline Phosphotase", unit="IU/L", low=44, high=147, absmin=20, absmax=500, default=80, step=1),
        "albumin": dict(label="SGPT (ALT)", unit="IU/L", low=7, high=56, absmin=0, absmax=300, default=30, step=1),
        "ag_ratio": dict(label="SGOT (AST)", unit="IU/L", low=8, high=48, absmin=0, absmax=300, default=25, step=1),
        "sgpt": dict(label="Total Proteins", unit="g/dL", low=6.0, high=8.3, absmin=2.0, absmax=10.0, default=7.0, step=0.1),
        "sgot": dict(label="Albumin", unit="g/dL", low=3.5, high=5.5, absmin=1.0, absmax=7.0, default=4.2, step=0.1),
        "alkphos": dict(label="A/G Ratio", unit="", low=1.1, high=2.5, absmin=0.3, absmax=3.0, default=1.5, step=0.05),
    }

    FRIENDLY_FEATURE_NAMES = {
        "age": "Age",
        "gender": "Gender",
        **{k: v["label"] for k, v in FIELD_META.items()},
        **{f"{k}_log": f"{v['label']} (log-scaled)" for k, v in FIELD_META.items()},
    }

    # Helper function to render a premium range strip
    def range_strip(value, meta):
        absmin, absmax = meta["absmin"], meta["absmax"]
        low, high = meta["low"], meta["high"]
        span = absmax - absmin
        zone_left = max(0, min(100, (low - absmin) / span * 100))
        zone_width = max(0, min(100 - zone_left, (high - low) / span * 100))
        marker_pos = max(0, min(100, (value - absmin) / span * 100))
        marker_color = "var(--accent-color)" if low <= value <= high else "#E2B82B"

        return f"""
        <div class="lab-range-container">
            <div class="lab-range-track">
                <div class="lab-range-zone" style="left:{zone_left:.1f}%; width:{zone_width:.1f}%;"></div>
                <div class="lab-range-marker" style="left:{marker_pos:.1f}%; background:{marker_color}; box-shadow: 0 0 6px {marker_color};"></div>
            </div>
            <div class="lab-range-legend">
                <span>{absmin:g}</span>
                <span>ref {low:g}–{high:g}</span>
                <span>{absmax:g}</span>
            </div>
        </div>
        """

    def build_feature_row(raw: dict) -> pd.DataFrame:
        row = dict(raw)
        for col in LOG_COLS:
            row[f"{col}_log"] = np.log1p(row[col])
        return pd.DataFrame([row])

    # 3. Load Model Artifacts
    @st.cache_resource
    def load_artifacts():
        model = joblib.load("models/liver/liver_model.pkl")
        scaler = joblib.load("models/liver/liver_scaler.pkl")
        return model, scaler

    try:
        model, scaler = load_artifacts()
    except FileNotFoundError:
        st.error("Model files not found. Make sure `liver_model.pkl` and `liver_scaler.pkl` are in models/liver/ directory.")
        st.stop()

    # Get feature columns from scaler (or fallback to manual list if attribute missing)
    try:
        feature_columns = list(scaler.feature_names_in_)
    except AttributeError:
        feature_columns = ["age", "gender", "tot_bilirubin", "direct_bilirubin", "tot_proteins", "albumin", "ag_ratio", "sgpt", "sgot", "alkphos", "tot_bilirubin_log", "direct_bilirubin_log", "tot_proteins_log", "albumin_log", "ag_ratio_log"]

    # 4. Hero Section
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-eyebrow">🧪 HEPATOLOGY & LIVER FUNCTION</div>
            <div class="hero-title">Hepatic Diagnostics Panel</div>
            <p class="hero-desc">
                Evaluate metabolic risk scores and compute liver pathology probabilities based on the Indian Liver Patient Dataset (ILPD).
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 5. Two-Column Dashboard Layout
    col_left, col_right = st.columns([1.2, 1], gap="large")

    # ---- LEFT COLUMN: Inputs & Illustration ----
    with col_left:
        # Illustration card
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 0.5rem 0; font-size:1.05rem; display:flex; align-items:center; gap:0.5rem;">🧬 Anatomical Visual</h4>', unsafe_allow_html=True)
        st.markdown(styles.get_liver_svg(), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Form card
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 1.2rem 0; font-size:1.05rem; display:flex; align-items:center; gap:0.5rem;">🧪 Patient Lab Records</h4>', unsafe_allow_html=True)

        patient_name = st.text_input("Patient Name", value="John Doe", key="liver_patient_name")

        # Patient basic details
        c1, c2 = st.columns(2)
        with c1:
            age = st.number_input("Age (years)", min_value=1, max_value=100, value=45, key="liver_age")
        with c2:
            gender = st.selectbox("Gender", ["Male", "Female"], key="liver_gender")

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        st.markdown("<span style='font-size: 0.88rem; font-weight:600; color:white; display:block; margin-bottom: 0.8rem;'>🔬 Laboratory Measurements</span>", unsafe_allow_html=True)

        # Lab values layout
        values = {}
        lab_cols = st.columns(2)
        for i, (key, meta) in enumerate(FIELD_META.items()):
            col = lab_cols[i % 2]
            with col:
                st.markdown(
                    f"""
                    <div style="background: rgba(255,255,255,0.01); border: 1px solid var(--card-border); 
                                border-radius: 12px; padding: 0.8rem 1rem 0.8rem 1rem; margin-bottom: 0.8rem;">
                        <div style="display:flex; justify-content:space-between; font-size:0.8rem; font-weight:600; color:var(--text-muted); margin-bottom:0.3rem;">
                            <span>{meta['label']}</span>
                            <span style="font-family:var(--font-mono); font-size:0.7rem; color:var(--accent-color);">{meta['unit']}</span>
                        </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Input
                val = st.number_input(
                    meta["label"], min_value=0.0, value=float(meta["default"]), step=float(meta["step"]),
                    key=f"val_{key}", label_visibility="collapsed"
                )
                
                # Range strip
                st.markdown(range_strip(val, meta), unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
                values[key] = val

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        run_clicked = st.button("🔍 Run Hepatic Assessment", use_container_width=True, key="liver_predict")
        st.markdown('</div>', unsafe_allow_html=True)

    # ---- RIGHT COLUMN: Diagnostic Results ----
    with col_right:
        st.markdown('<div class="premium-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown('<h4 style="margin:0 0 1.2rem 0; font-size:1.05rem; display:flex; align-items:center; gap:0.5rem;">🎯 Analysis Result</h4>', unsafe_allow_html=True)

        if run_clicked:
            raw = {"age": age, "gender": 1 if gender == "Male" else 0, **values}
            X_row = build_feature_row(raw)
            
            # Reorder columns to match expected scaler structure
            X_row = X_row[feature_columns]
            
            # Scale & Predict
            X_scaled = scaler.transform(X_row)
            pred = model.predict(X_scaled)[0]
            proba = model.predict_proba(X_scaled)[0][1]
            prob_pct = proba * 100
            
            high_risk = pred == 1
            confidence = max(model.predict_proba(X_scaled)[0]) * 100

            # Save to prediction history
            try:
                from components.history import read_history, write_history
                import time
                history_item = {
                    "id": str(int(time.time() * 1000)),
                    "patientName": patient_name if patient_name else "Unknown Patient",
                    "disease": "Liver Disease",
                    "date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "prediction": int(pred),
                    "probability": float(prob_pct),
                    "confidence": float(confidence),
                    "vitals": {
                        "Age": f"{age} years",
                        "Gender": gender,
                        "Total Bilirubin": f"{values['tot_bilirubin']} mg/dL",
                        "Direct Bilirubin": f"{values['direct_bilirubin']} mg/dL",
                        "Alkaline Phosphatase": f"{values['tot_proteins']} IU/L",
                        "SGPT (ALT)": f"{values['albumin']} IU/L",
                        "SGOT (AST)": f"{values['ag_ratio']} IU/L",
                        "Total Proteins": f"{values['sgpt']} g/dL",
                        "Albumin": f"{values['sgot']} g/dL",
                        "A/G Ratio": values['alkphos']
                    }
                }
                history_list = read_history()
                history_list.insert(0, history_item)
                write_history(history_list)
            except Exception as history_err:
                print("Error saving Streamlit liver history:", history_err)

            # Result Header Card
            status_color = "#22C55E" if not high_risk else "#EF4444"
            status_bg = "rgba(34, 197, 94, 0.08)" if not high_risk else "rgba(239, 68, 68, 0.08)"
            status_border = "rgba(34, 197, 94, 0.2)" if not high_risk else "rgba(239, 68, 68, 0.2)"
            status_text = "ELEVATED RISK" if high_risk else "LOW RISK DETECTED"
            status_desc = "Patient exhibits indicators of chronic liver disease" if high_risk else "Hepatic biomarkers are within reference intervals"

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
                        <span>Liver Disease Probability</span>
                        <span>{prob_pct:.1f}%</span>
                    </div>
                    <div class="custom-progress-track">
                        <div class="custom-progress-bar" style="width: {prob_pct}%;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Feature contributions analysis supporting calibrated classifiers and tree models
            protective_features = {"sgpt", "sgot", "alkphos"}
            contributions_list = []
            for idx, feat_name in enumerate(feature_columns):
                if hasattr(model, "calibrated_classifiers_"):
                    # Calibrated Classifier (ensemble over cv folds)
                    if hasattr(model.calibrated_classifiers_[0].estimator, "feature_importances_"):
                        importance = np.mean([clf.estimator.feature_importances_ for clf in model.calibrated_classifiers_], axis=0)[idx]
                    else:
                        importance = np.mean([abs(clf.estimator.coef_[0][idx]) for clf in model.calibrated_classifiers_], axis=0)
                else:
                    # Standard Classifier
                    if hasattr(model, "feature_importances_"):
                        importance = model.feature_importances_[idx]
                    elif hasattr(model, "coef_"):
                        importance = abs(model.coef_[0][idx])
                    else:
                        importance = 1.0
                
                val_scaled = X_scaled[0][idx]
                base_name = feat_name.replace("_log", "")
                direction = -1.0 if base_name in protective_features else 1.0
                contributions_list.append(val_scaled * importance * direction)
                
            contributions = np.array(contributions_list)
            order = np.argsort(-np.abs(contributions))[:3]
            
            st.markdown("<div style='font-family:var(--font-mono); font-size:0.75rem; letter-spacing:0.05em; margin-bottom:0.6rem; color:var(--text-muted); text-transform:uppercase;'>🔥 Top Contributing Risk Factors</div>", unsafe_allow_html=True)
            
            rows_html = ""
            for idx in order:
                feat_name = feature_columns[idx]
                name = FRIENDLY_FEATURE_NAMES.get(feat_name, feat_name)
                direction = "Raises Risk (↑)" if contributions[idx] > 0 else "Lowers Risk (↓)"
                color = "#EF4444" if contributions[idx] > 0 else "#22C55E"
                rows_html += f"""
                <div style="display:flex; justify-content:space-between; font-size:0.8rem; padding:0.4rem 0.6rem; 
                            background:rgba(255,255,255,0.01); border:1px solid var(--card-border); border-radius:8px; margin-bottom:0.4rem;">
                    <span style="color:white; font-weight:500;">{name}</span>
                    <span style="color:{color}; font-weight:600; font-family:var(--font-mono); font-size:0.75rem;">{direction}</span>
                </div>
                """
            st.markdown(rows_html, unsafe_allow_html=True)
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

            # Patient Summary Box
            st.markdown(
                f"""
                <div style="background: rgba(255,255,255,0.01); border: 1px solid var(--card-border); border-radius:14px; padding:1.2rem; margin-bottom:1.5rem;">
                    <span style="font-weight:700; color:white; display:block; margin-bottom:0.8rem; font-size:0.9rem;">📋 Clinical Inputs Summary</span>
                    <table style="width:100%; font-size:0.82rem; border-collapse:collapse; color:var(--text-muted);">
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Age / Gender</td><td style="text-align:right; color:white; font-weight:500;">{age} yrs / {gender}</td></tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Total Bilirubin</td><td style="text-align:right; color:white; font-weight:500;">{values['tot_bilirubin']} mg/dL</td></tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">Alkaline Phosphotase</td><td style="text-align:right; color:white; font-weight:500;">{values['tot_proteins']} IU/L</td></tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);"><td style="padding:0.4rem 0;">SGPT (ALT) / SGOT (AST)</td><td style="text-align:right; color:white; font-weight:500;">{values['albumin']} / {values['ag_ratio']} IU/L</td></tr>
                        <tr><td style="padding:0.4rem 0;">Albumin / Total Proteins</td><td style="text-align:right; color:white; font-weight:500;">{values['sgot']} / {values['sgpt']} g/dL</td></tr>
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
                            <td style="padding:0.5rem 0.4rem;">Total Bilirubin</td>
                            <td>{values['tot_bilirubin']} mg/dL</td>
                            <td>{FIELD_META['tot_bilirubin']['low']} - {FIELD_META['tot_bilirubin']['high']} mg/dL</td>
                            <td><span style="color:{'#EF4444' if values['tot_bilirubin'] > FIELD_META['tot_bilirubin']['high'] else '#22C55E'}; font-weight:700;">{'⚠️ Elevated' if values['tot_bilirubin'] > FIELD_META['tot_bilirubin']['high'] else '✓ Normal'}</span></td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:0.5rem 0.4rem;">Direct Bilirubin</td>
                            <td>{values['direct_bilirubin']} mg/dL</td>
                            <td>{FIELD_META['direct_bilirubin']['low']} - {FIELD_META['direct_bilirubin']['high']} mg/dL</td>
                            <td><span style="color:{'#EF4444' if values['direct_bilirubin'] > FIELD_META['direct_bilirubin']['high'] else '#22C55E'}; font-weight:700;">{'⚠️ Elevated' if values['direct_bilirubin'] > FIELD_META['direct_bilirubin']['high'] else '✓ Normal'}</span></td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:0.5rem 0.4rem;">Alkaline Phosphatase (ALP)</td>
                            <td>{values['tot_proteins']} IU/L</td>
                            <td>{FIELD_META['tot_proteins']['low']} - {FIELD_META['tot_proteins']['high']} IU/L</td>
                            <td><span style="color:{'#EF4444' if values['tot_proteins'] > FIELD_META['tot_proteins']['high'] else '#22C55E'}; font-weight:700;">{'⚠️ Elevated' if values['tot_proteins'] > FIELD_META['tot_proteins']['high'] else '✓ Normal'}</span></td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:0.5rem 0.4rem;">SGPT (ALT)</td>
                            <td>{values['albumin']} IU/L</td>
                            <td>{FIELD_META['albumin']['low']} - {FIELD_META['albumin']['high']} IU/L</td>
                            <td><span style="color:{'#EF4444' if values['albumin'] > FIELD_META['albumin']['high'] else '#22C55E'}; font-weight:700;">{'⚠️ Elevated' if values['albumin'] > FIELD_META['albumin']['high'] else '✓ Normal'}</span></td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:0.5rem 0.4rem;">SGOT (AST)</td>
                            <td>{values['ag_ratio']} IU/L</td>
                            <td>{FIELD_META['ag_ratio']['low']} - {FIELD_META['ag_ratio']['high']} IU/L</td>
                            <td><span style="color:{'#EF4444' if values['ag_ratio'] > FIELD_META['ag_ratio']['high'] else '#22C55E'}; font-weight:700;">{'⚠️ Elevated' if values['ag_ratio'] > FIELD_META['ag_ratio']['high'] else '✓ Normal'}</span></td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:0.5rem 0.4rem;">Total Proteins</td>
                            <td>{values['sgpt']} g/dL</td>
                            <td>{FIELD_META['sgpt']['low']} - {FIELD_META['sgpt']['high']} g/dL</td>
                            <td><span style="color:{'#EF4444' if (values['sgpt'] < FIELD_META['sgpt']['low'] or values['sgpt'] > FIELD_META['sgpt']['high']) else '#22C55E'}; font-weight:700;">{'⚠️ Abnormal' if (values['sgpt'] < FIELD_META['sgpt']['low'] or values['sgpt'] > FIELD_META['sgpt']['high']) else '✓ Normal'}</span></td>
                        </tr>
                        <tr style="border-bottom:1px solid rgba(255,255,255,0.05);">
                            <td style="padding:0.5rem 0.4rem;">Albumin</td>
                            <td>{values['sgot']} g/dL</td>
                            <td>{FIELD_META['sgot']['low']} - {FIELD_META['sgot']['high']} g/dL</td>
                            <td><span style="color:{'#EF4444' if (values['sgot'] < FIELD_META['sgot']['low'] or values['sgot'] > FIELD_META['sgot']['high']) else '#22C55E'}; font-weight:700;">{'⚠️ Abnormal' if (values['sgot'] < FIELD_META['sgot']['low'] or values['sgot'] > FIELD_META['sgot']['high']) else '✓ Normal'}</span></td>
                        </tr>
                    </table>
                    """,
                    unsafe_allow_html=True
                )

            # Recommendations
            recos = []
            if high_risk:
                recos = [
                    "Consult a gastroenterologist or hepatologist for a diagnostic liver panel.",
                    "Discontinue alcohol intake completely.",
                    "Reduce intake of fat-soluble vitamins unless prescribed.",
                    "Avoid self-prescribed medications to prevent drug-induced liver injury."
                ]
            else:
                recos = [
                    "Maintain a balanced diet rich in leafy greens and lean proteins.",
                    "Stay well hydrated and limit high-fructose corn syrup.",
                    "Get regular exercise and check BMI indices.",
                    "Support a regular liver health assessment annually."
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
                    Please fill out the patient metrics in the left panel and click <b>Run Hepatic Assessment</b> to generate the report.
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Medical Disclaimer
        st.markdown(
            """
            <div class="disclaimer-text">
                <b>Medical Disclaimer:</b> This diagnostic assessment is generated dynamically using an artificial intelligence classification model. It is designed to act as an indicative screening utility and is <b>not a clinical diagnostic finding</b>. Always confirm these estimations with certified laboratory testing and professional hepatology consultations.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)