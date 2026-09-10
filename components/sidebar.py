import streamlit as st

def render_sidebar():
    """Renders the left informational sidebar aligned with the visual mockups."""
    # Persistent dark sidebar background and button highlights
    st.markdown(
        """
        <style>
        /* Specific highlights for active states */
        .sidebar-active-heart button {
            background-color: #EF4444 !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
        }
        .sidebar-active-liver button {
            background-color: #22C55E !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
        }
        .sidebar-active-kidney button {
            background-color: #3B82F6 !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
        }
        .sidebar-active-diabetes button {
            background-color: #3B82F6 !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
        }
        .sidebar-active-dash button {
            background-color: rgba(255, 255, 255, 0.08) !important;
            color: #EF4444 !important;
            border-left: 3px solid #EF4444 !important;
            border-radius: 0 8px 8px 0 !important;
            font-weight: 700 !important;
        }
        .sidebar-active-history button {
            background-color: #6366F1 !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 700 !important;
        }
        
        /* Help card styling */
        .help-card {
            background: linear-gradient(135deg, #131317 0%, #0F0F12 100%);
            border: 1px solid #222227;
            border-radius: 12px;
            padding: 0.9rem;
            margin-top: 1.5rem;
        }
        .help-card h6 {
            color: #EF4444 !important;
            font-size: 0.85rem !important;
            margin: 0 0 0.3rem 0 !important;
        }
        .help-card p {
            font-size: 0.75rem;
            color: #8E8E93;
            line-height: 1.4;
            margin: 0 0 0.8rem 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        # Title Branding
        st.markdown(
            """
            <div style="padding-bottom: 0.8rem; border-bottom: 1px solid #222227; margin-bottom: 1.2rem;">
                <span style="font-weight: 800; font-size: 1.15rem; color: #EF4444; display: flex; align-items: center; gap: 0.4rem;">
                    <span style="animation: heartbeat 1.5s infinite;">🩺</span> Smart Health Assistant
                </span>
                <div style="font-size: 0.78rem; color: #8E8E93; margin-top: 0.2rem;">Your health, predicted by AI</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        current_page = st.session_state.page

        # Section 1: MAIN MENU
        st.markdown('<div style="font-size: 0.7rem; font-weight: 700; color: #52525B; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.5rem;">MAIN MENU</div>', unsafe_allow_html=True)
        is_dash_active = current_page == "Home"
        btn_class = "sidebar-active-dash" if is_dash_active else "sidebar-btn"
        st.markdown(f'<div class="{btn_class}">', unsafe_allow_html=True)
        if st.button("🏠  Dashboard", use_container_width=True, key="side_dash"):
            st.session_state.page = "Home"
            st.query_params["page"] = "Home"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Section 2: DISEASE PREDICTIONS
        st.markdown('<div style="font-size: 0.7rem; font-weight: 700; color: #52525B; letter-spacing: 0.08em; text-transform: uppercase; margin: 1.2rem 0 0.5rem 0;">DISEASE PREDICTIONS</div>', unsafe_allow_html=True)
        
        # Heart Disease Button
        is_heart_active = current_page == "Heart"
        h_btn_class = "sidebar-active-heart" if is_heart_active else "sidebar-btn"
        st.markdown(f'<div class="{h_btn_class}">', unsafe_allow_html=True)
        if st.button("❤️  Heart Disease", use_container_width=True, key="side_heart"):
            st.session_state.page = "Heart"
            st.query_params["page"] = "Heart"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Liver Disease Button
        is_liver_active = current_page == "Liver"
        l_btn_class = "sidebar-active-liver" if is_liver_active else "sidebar-btn"
        st.markdown(f'<div class="{l_btn_class}">', unsafe_allow_html=True)
        if st.button("🧪  Liver Disease", use_container_width=True, key="side_liver"):
            st.session_state.page = "Liver"
            st.query_params["page"] = "Liver"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Kidney Disease Button
        is_kidney_active = current_page == "Kidney"
        k_btn_class = "sidebar-active-kidney" if is_kidney_active else "sidebar-btn"
        st.markdown(f'<div class="{k_btn_class}">', unsafe_allow_html=True)
        if st.button("🫘  Kidney Disease", use_container_width=True, key="side_kidney"):
            st.session_state.page = "Kidney"
            st.query_params["page"] = "Kidney"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Diabetes Button
        is_diabetes_active = current_page == "Diabetes"
        d_btn_class = "sidebar-active-diabetes" if is_diabetes_active else "sidebar-btn"
        st.markdown(f'<div class="{d_btn_class}">', unsafe_allow_html=True)
        if st.button("💧  Diabetes", use_container_width=True, key="side_diab"):
            st.session_state.page = "Diabetes"
            st.query_params["page"] = "Diabetes"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Section 3: TOOLS & HISTORY
        st.markdown('<div style="font-size: 0.7rem; font-weight: 700; color: #52525B; letter-spacing: 0.08em; text-transform: uppercase; margin: 1.2rem 0 0.5rem 0;">TOOLS & HISTORY</div>', unsafe_allow_html=True)
        
        is_history_active = current_page == "History"
        hist_btn_class = "sidebar-active-history" if is_history_active else "sidebar-btn"
        st.markdown(f'<div class="{hist_btn_class}">', unsafe_allow_html=True)
        if st.button("📄  Health Records", use_container_width=True, key="side_rec"):
            st.session_state.page = "History"
            st.query_params["page"] = "History"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Need Help? Card
        st.markdown(
            """
            <div class="help-card">
                <h6>Need Help?</h6>
                <p>Talk to our AI assistant for personalized health insights.</p>
            """,
            unsafe_allow_html=True
        )
        if st.button("💬 Ask AI Assistant", key="side_ai_btn", use_container_width=True):
            st.toast("AI Medical Bot is coming soon! 🤖", icon="💬")
        st.markdown('</div>', unsafe_allow_html=True)

        # Bottom Secure Indicator
        st.markdown(
            """
            <div style="display: flex; align-items: center; justify-content: center; gap: 0.4rem; margin-top: 1.5rem; font-size: 0.72rem; color: #71717A;">
                <span>🛡️</span> Your data is secure and 100% confidential.
            </div>
            """,
            unsafe_allow_html=True
        )
pre_active_sidebar = None
