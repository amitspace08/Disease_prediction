import streamlit as st
import json
import os
import pandas as pd

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
        st.error(f"Error writing history file: {e}")

def render_history():
    """Renders the prediction history page in Streamlit."""
    st.markdown("""
    <style>
    :root {
        --accent-color: #6366F1;
        --accent-gradient-end: #4F46E5;
        --accent-glow: rgba(99, 102, 241, 0.15);
    }
    </style>
    """, unsafe_allow_html=True)

    # Hero Banner
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-eyebrow">📁 PATIENT RECORDS</div>
            <div class="hero-title">Prediction History Logs</div>
            <div class="hero-desc">
                Access past diagnostic assessments, clinical parameter logs, and prediction details for registered patients.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    history_list = read_history()

    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"##### 📁 Archived Predictions ({len(history_list)})")
    with col2:
        if len(history_list) > 0:
            if st.button("🗑️ Clear All History", type="secondary", use_container_width=True):
                write_history([])
                st.success("History cleared successfully!")
                st.rerun()

    if not history_list:
        st.markdown(
            """
            <div class="premium-card text-center" style="padding: 3rem; text-align: center;">
                <h4 style="color: var(--text-muted); margin-bottom: 0.5rem;">No Records Found</h4>
                <p style="color: var(--text-muted); font-size: 0.85rem; margin: 0;">
                    Run prediction diagnostics inside any of the disease assessment tabs to save diagnostic histories.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    # Render each record
    for record in history_list:
        is_ckd = record.get("disease") == "Kidney Disease"
        is_high = record.get("prediction") == 0 if is_ckd else record.get("prediction") == 1
        status_text = "🔴 High Risk / Disease" if is_high else "🟢 Low Risk / Healthy"
        accent_color = "#EF4444" if is_high else "#22C55E"

        with st.container():
            st.markdown(
                f"""
                <div class="premium-card" style="border-left: 5px solid {accent_color}; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                        <div>
                            <span style="font-weight: 700; font-size: 1.1rem; color: white;">{record.get('patientName')}</span>
                            <span style="margin-left: 0.8rem; font-size: 0.75rem; background: rgba(255,255,255,0.08); padding: 0.2rem 0.5rem; border-radius: 4px; color: var(--text-muted);">{record.get('disease')}</span>
                        </div>
                        <span style="font-size: 0.8rem; color: var(--text-muted);">{record.get('date')}</span>
                    </div>
                    <div style="display: flex; gap: 2rem; font-size: 0.9rem;">
                        <div>Status: <span style="font-weight: 700; color: {accent_color};">{status_text}</span></div>
                        <div>Probability: <span style="font-weight: 700; color: white;">{record.get('probability'):.1f}%</span></div>
                        <div>Confidence: <span style="font-weight: 700; color: white;">{record.get('confidence'):.1f}%</span></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Use expander to view detailed analysis parameters
            with st.expander("🔍 View Detailed Analysis Details"):
                vitals = record.get("vitals", {})
                if vitals:
                    df = pd.DataFrame(list(vitals.items()), columns=["Clinical Parameter", "Recorded Value"])
                    st.dataframe(df, hide_index=True, use_container_width=True)
                else:
                    st.write("No clinical vital parameters recorded.")
