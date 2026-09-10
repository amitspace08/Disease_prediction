import streamlit as st

def render_home():
    """Renders the dashboard home page."""
    # Custom Violet accent for Home page
    st.markdown("""
    <style>
    :root {
        --accent-color: #8B5CF6;
        --accent-gradient-end: #6366F1;
        --accent-glow: rgba(139, 92, 246, 0.15);
    }
    </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-eyebrow">⚡ CLINICAL ARTIFICIAL INTELLIGENCE</div>
            <div class="hero-title">Next-Generation AI<br>Disease Prediction</div>
            <div class="hero-desc">
                Leverage advanced, peer-reviewed clinical machine learning models to assess health risks and compute diagnostics in under 30 seconds.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 🔍 Select Diagnostics Module")
    st.markdown("<p style='color: var(--text-muted); margin-top: -0.5rem; margin-bottom: 1.5rem;'>Each prediction engine runs on a specialized, scaled ML classifier.</p>", unsafe_allow_html=True)

    # Grid for disease selection cards
    card_cols = st.columns(4)
    
    diseases = [
        {
            "emoji": "🫀", "title": "Heart Risk Analysis",
            "desc": "Predict coronary disease and arterial blockages using clinical metrics.",
            "target": "Heart", "color": "#EF4444"
        },
        {
            "emoji": "🧪", "title": "Hepatic Diagnostics",
            "desc": "Assess liver function, proteins, and bilrubin levels for liver diseases.",
            "target": "Liver", "color": "#22C55E"
        },
        {
            "emoji": "🫘", "title": "Chronic Kidney Disease",
            "desc": "Evaluate glomerular health and urine statistics for CKD risk.",
            "target": "Kidney", "color": "#3B82F6"
        },
        {
            "emoji": "🩸", "title": "Diabetes Screen",
            "desc": "Assess insulin levels and glucose tolerance indicators.",
            "target": "Diabetes", "color": "#3B82F6"
        }
    ]

    for idx, disease in enumerate(diseases):
        with card_cols[idx]:
            # Outer styled card container
            st.markdown(
                f"""
                <div class="premium-card" style="--accent-color: {disease['color']}; --accent-glow: {disease['color']}22; height: 320px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="font-size: 2.2rem; margin-bottom: 0.8rem;">{disease['emoji']}</div>
                        <h4 style="margin: 0 0 0.5rem 0; font-size: 1.15rem;">{disease['title']}</h4>
                        <p style="color: var(--text-muted); font-size: 0.86rem; line-height: 1.5; margin: 0;">{disease['desc']}</p>
                    </div>
                    <div style="margin-top: 1.5rem;">
                """,
                unsafe_allow_html=True
            )
            
            # We insert the native Streamlit button inside the container HTML
            if st.button(f"Analyze {disease['target']} →", key=f"btn_{disease['target']}", use_container_width=True):
                st.session_state.page = disease["target"]
                st.query_params["page"] = disease["target"]
                st.rerun()
                
            st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown("### 📊 Platform Metrics")

    # Platform Stats Bar
    stats_cols = st.columns(5)
    
    stats_data = [
        {"num": "15,000+", "lbl": "Analyses Processed"},
        {"num": "97.4%", "lbl": "Mean Heart Accuracy"},
        {"num": "30 Sec", "lbl": "Avg Diagnostics Latency"},
        {"num": "🔒 HIPAA", "lbl": "Compliant Security"},
        {"num": "4 Models", "lbl": "Active Classifiers"}
    ]

    for idx, stat in enumerate(stats_data):
        with stats_cols[idx]:
            st.markdown(
                f"""
                <div style="background: var(--bg-secondary); border: 1px solid var(--card-border); 
                            border-radius: 16px; padding: 1.2rem; text-align: center; height: 100%;">
                    <div style="font-size: 1.6rem; font-weight: 800; color: #8B5CF6;">{stat['num']}</div>
                    <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-top: 0.3rem;">{stat['lbl']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
