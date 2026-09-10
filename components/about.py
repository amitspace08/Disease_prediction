import streamlit as st

def render_about():
    """Renders the About page content."""
    # Violet accent for About page
    st.markdown("""
    <style>
    :root {
        --accent-color: #8B5CF6;
        --accent-gradient-end: #6366F1;
        --accent-glow: rgba(139, 92, 246, 0.15);
    }
    </style>
    """, unsafe_allow_html=True)

    # Hero Banner
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-eyebrow">📖 METHODOLOGY & DOCUMENTATION</div>
            <div class="hero-title">About MediPredict</div>
            <div class="hero-desc">
                MediPredict is a final-year research initiative combining clinical data records with supervised machine learning classifiers to produce instant, indicative risk profiles.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            """
            <div class="premium-card" style="height: 100%;">
                <h3 style="margin-top: 0; color: #8B5CF6;">🔬 Clinical Classifiers</h3>
                <p style="color: var(--text-muted); font-size: 0.92rem; line-height: 1.6;">
                    The prediction systems employ specialized machine learning models trained on standardized, anonymized hospital datasets:
                </p>
                <div style="margin-top: 1rem;">
                    <div style="padding: 0.8rem; background: rgba(255, 255, 255, 0.02); border: 1px solid var(--card-border); border-radius: 12px; margin-bottom: 0.6rem;">
                        <span style="font-weight: 700; color: white;">💓 Heart Disease Model</span>
                        <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">Random Forest (97.4% accuracy)</div>
                    </div>
                    <div style="padding: 0.8rem; background: rgba(255, 255, 255, 0.02); border: 1px solid var(--card-border); border-radius: 12px; margin-bottom: 0.6rem;">
                        <span style="font-weight: 700; color: white;">🧪 Hepatic Diagnostics Model</span>
                        <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">Calibrated Logistic Regression (66.7% accuracy)</div>
                    </div>
                    <div style="padding: 0.8rem; background: rgba(255, 255, 255, 0.02); border: 1px solid var(--card-border); border-radius: 12px; margin-bottom: 0.6rem;">
                        <span style="font-weight: 700; color: white;">🫘 Chronic Kidney Disease Model</span>
                        <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">Random Forest Classifier (98.3% accuracy)</div>
                    </div>
                    <div style="padding: 0.8rem; background: rgba(255, 255, 255, 0.02); border: 1px solid var(--card-border); border-radius: 12px;">
                        <span style="font-weight: 700; color: white;">🩸 Diabetes Prediction Model</span>
                        <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.2rem;">Random Forest Classifier (84.8% accuracy)</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="premium-card" style="height: 100%;">
                <h3 style="margin-top: 0; color: #8B5CF6;">👨‍💻 Development & Engineering</h3>
                <p style="color: var(--text-muted); font-size: 0.92rem; line-height: 1.6;">
                    Developed as a final year academic project, the system showcases the integration of scikit-learn models within a modern web interface.
                </p>
                <div style="margin-top: 1.5rem;">
                    <h4 style="margin-bottom: 0.4rem; color: white;">Lead Developer</h4>
                    <p style="margin: 0; font-size: 1rem; font-weight: 600; color: #8B5CF6;">Amit Kumar</p>
                    <p style="margin: 0.1rem 0 0 0; font-size: 0.82rem; color: var(--text-muted);">Department of Computer Science & Engineering</p>
                    <p style="margin: 0.1rem 0 0 0; font-size: 0.82rem; color: var(--text-muted);">National Institute of Technology (NIT) Delhi</p>
                </div>
                <div style="margin-top: 1.5rem; padding: 1rem; border-radius: 14px; background: rgba(139, 92, 246, 0.05); border: 1px solid rgba(139, 92, 246, 0.15);">
                    <span style="font-weight: 700; color: white; display: block; margin-bottom: 0.3rem;">⚠️ Important Notice</span>
                    <span style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.5; display: block;">
                        The model predictions are probabilistic and generated using public clinical datasets. These results are <b>indicative only</b> and are not a substitute for clinical diagnostics or professional medical consultations.
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
