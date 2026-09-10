import streamlit as st

def render_navbar():
    """Renders a fixed premium top navigation bar aligned with the screenshot styling."""
    st.markdown("""
    <style>
    /* Fixed top navbar styling targeting the container with key "navbar" */
    div[data-testid="stVerticalBlock"] > div[key="navbar"] {
        position: fixed !important;
        top: 0;
        left: 0;
        right: 0;
        height: 4.5rem;
        background-color: #08080A !important;
        border-bottom: 1px solid #1A1A22 !important;
        z-index: 9999;
        padding: 1rem 2rem 0.5rem 2rem !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    /* Active navigation button capsule override */
    .nav-capsule-active button {
        background: rgba(239, 68, 68, 0.15) !important;
        color: #EF4444 !important;
        border: 1px solid rgba(239, 68, 68, 0.25) !important;
        border-radius: 20px !important;
        font-weight: 700 !important;
    }
    
    /* Ensure page content starts below navbar */
    .block-container {
        margin-top: 1.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container(key="navbar"):
        # Branding, Navigation links, and CTA
        cols = st.columns([2.5, 1, 1, 1, 1, 1, 1, 1.8])
        
        # Logo / Branding
        with cols[0]:
            st.markdown(
                """
                <div style="display: flex; align-items: center; gap: 0.6rem; height: 100%; margin-top: 3px;">
                    <span style="font-size: 1.5rem; line-height: 1; display: inline-block; color: #EF4444; animation: heartbeat 1.5s infinite;">❤️</span>
                    <div style="display: flex; flex-direction: column; justify-content: center;">
                        <span style="font-weight: 800; font-size: 1.15rem; line-height: 1.1; letter-spacing: -0.02em; color: white;">MediPredict</span>
                        <span style="font-size: 0.65rem; color: #8E8E93; letter-spacing: 0.05em; text-transform: uppercase; font-weight: 600;">AI Powered Health Prediction</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        pages = [
            ("Home", "🏠 Home"),
            ("Heart", "❤️ Heart"),
            ("Liver", "🧪 Liver"),
            ("Kidney", "🫘 Kidney"),
            ("Diabetes", "💧 Diabetes"),
            ("About", "ℹ️ About")
        ]
        
        # Navigation Tabs
        for i, (page_id, display_name) in enumerate(pages):
            with cols[i + 1]:
                is_active = st.session_state.page == page_id
                btn_class = "nav-capsule-active" if is_active else "nav-btn"
                
                # Active colors depending on disease
                if is_active:
                    accent_color = "#EF4444"
                    if page_id == "Liver":
                        accent_color = "#22C55E"
                    elif page_id in ["Kidney", "Diabetes"]:
                        accent_color = "#3B82F6"
                    elif page_id == "About":
                        accent_color = "#8B5CF6"
                        
                    st.markdown(f"""
                    <style>
                    div[key="navbar"] div[data-testid="stHorizontalBlock"] > div:nth-child({i+2}) button {{
                        background: {accent_color}1a !important;
                        color: {accent_color} !important;
                        border: 1px solid {accent_color}33 !important;
                        border-radius: 20px !important;
                        font-weight: 700 !important;
                    }}
                    </style>
                    """, unsafe_allow_html=True)
                
                st.markdown(f'<div class="{btn_class}" style="text-align: center; margin-top: 3px;">', unsafe_allow_html=True)
                if st.button(display_name, key=f"nav_{page_id}", use_container_width=True):
                    st.session_state.page = page_id
                    st.query_params["page"] = page_id
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
        # CTA Action Button (matches mockup)
        with cols[7]:
            st.markdown('<div class="stButton" style="margin-top: 1px;">', unsafe_allow_html=True)
            # Inject a red/accent color block for CTA
            st.markdown("""
            <style>
            div[key="navbar"] div[data-testid="stHorizontalBlock"] > div:nth-child(8) button {
                background: linear-gradient(135deg, #EF4444 0%, #C53030 100%) !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
                box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2) !important;
                font-weight: 700 !important;
                height: 38px !important;
                font-size: 0.88rem !important;
                padding: 0 1rem !important;
            }
            </style>
            """, unsafe_allow_html=True)
            if st.button("Get Started →", key="nav_cta", use_container_width=True):
                st.session_state.page = "Heart"
                st.query_params["page"] = "Heart"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
pre_active = None
