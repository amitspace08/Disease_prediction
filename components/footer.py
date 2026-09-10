import streamlit as st

def render_footer():
    """Renders the global application footer."""
    st.markdown("<hr style='border-color: var(--card-border); margin: 3rem 0 1.5rem 0;'>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; padding-bottom: 2rem; text-align: center;">
            <div style="font-size: 0.8rem; color: var(--text-muted);">
                MediPredict &copy; 2026 | Built for academic research and demonstration purposes.
            </div>
            <div style="font-size: 0.75rem; color: #8E8E93; max-width: 800px; line-height: 1.4;">
                <b>Disclaimer:</b> All analysis outputs are generated from statistical probabilities of clinical training sets and are completely advisory. Please seek official clinical testing and professional medical advice for definitive healthcare assessments.
            </div>
            <div style="font-size: 0.8rem; font-weight: 500; color: var(--accent-color, #8B5CF6); margin-top: 0.2rem;">
                Developed by Amit Kumar | National Institute of Technology Delhi
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
