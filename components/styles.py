import streamlit as st

def get_base_css():
    """Returns the persistent base CSS styling for global elements (navbar, sidebar)."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --font-sans: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }

    /* Core Page Layout */
    .stApp {
        font-family: var(--font-sans);
    }
    
    .block-container {
        padding-top: 5.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px !important;
    }

    /* Hide Streamlit elements */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    div[data-testid="stToolbar"] {
        display: none !important;
    }
    div[data-testid="stDecoration"] {
        display: none !important;
    }
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Fixed top navbar styling - ALWAYS DARK */
    div[data-testid="stVerticalBlock"] > div[key="navbar"] {
        position: fixed !important;
        top: 0;
        left: 0;
        right: 0;
        height: 4.5rem;
        background-color: #0A0A0C !important;
        border-bottom: 1px solid #1A1A22 !important;
        z-index: 9999;
        padding: 1rem 2rem 0.5rem 2rem !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    /* Fixed left sidebar styling - ALWAYS DARK */
    section[data-testid="stSidebar"] {
        background-color: #0B0B0E !important;
        border-right: 1px solid #1A1A22 !important;
        padding-top: 1.5rem !important;
    }

    /* Navigation button styles inside top navbar */
    .nav-btn button {
        background: transparent !important;
        border: none !important;
        color: #8E8E93 !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        border-radius: 20px !important;
        transition: all 0.2s ease !important;
        height: auto !important;
        width: auto !important;
    }
    .nav-btn button:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
    }
    .nav-btn-active button {
        background: rgba(255, 255, 255, 0.08) !important;
        color: var(--accent-color, #EF4444) !important;
        border-bottom: 2px solid var(--accent-color, #EF4444) !important;
        border-radius: 0px !important;
        font-weight: 700 !important;
        height: auto !important;
        width: auto !important;
    }

    /* Sidebar Navigation buttons styling */
    .sidebar-btn button {
        background: transparent !important;
        border: none !important;
        color: #8E8E93 !important;
        text-align: left !important;
        font-size: 0.9rem !important;
        padding: 0.6rem 1rem !important;
        width: 100% !important;
        justify-content: flex-start !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
        font-weight: 500 !important;
    }
    .sidebar-btn button:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        transform: translateX(3px);
    }
    .sidebar-btn-active button {
        background: rgba(239, 68, 68, 0.1) !important;
        color: var(--accent-color, #EF4444) !important;
        border-left: 3px solid var(--accent-color, #EF4444) !important;
        border-radius: 0 10px 10px 0 !important;
        font-weight: 700 !important;
        justify-content: flex-start !important;
        width: 100% !important;
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: #2C2C35;
        border-radius: 99px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-color, #EF4444);
    }
    </style>
    """

def get_theme_css(theme_mode, accent_color, accent_end=None):
    """Generates variables and overrides for dynamic Light/Dark mode content panels."""
    if not accent_end:
        accent_end = accent_color
    
    if theme_mode == "light":
        return f"""
        <style>
        :root {{
            --bg-primary: #F8FAFC;
            --bg-secondary: #F1F5F9;
            --card-bg: #FFFFFF;
            --card-border: #E2E8F0;
            --text-primary: #0F172A;
            --text-muted: #64748B;
            --input-bg: #FFFFFF;
            --input-border: #E2E8F0;
            --input-text: #0F172A;
            --accent-color: {accent_color};
            --accent-gradient-end: {accent_end};
            --accent-glow: {accent_color}1a;
        }}
        
        .stApp {{
            background-color: var(--bg-primary);
        }}
        
        /* Clinical cards */
        .premium-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 1.8rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .premium-card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent-color);
            box-shadow: 0 8px 24px var(--accent-glow);
        }}
        
        /* Input tile styling */
        .param-tile {{
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 0.8rem 1rem;
            margin-bottom: 0.8rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            transition: border-color 0.2s ease;
        }}
        .param-tile:hover {{
            border-color: var(--accent-color);
        }}
        .param-label-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.25rem;
        }}
        .param-unit {{
            font-size: 0.72rem;
            color: var(--text-muted);
            font-family: var(--font-sans);
        }}
        .param-range {{
            font-size: 0.72rem;
            font-weight: 500;
            color: #22C55E;
            margin-top: 0.25rem;
            display: block;
        }}

        /* Streamlit Input Overrides */
        div[data-testid="stNumberInput"] input, 
        div[data-testid="stTextInput"] input,
        div[data-testid="stSelectbox"] > div > div {{
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
            color: #0F172A !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
            height: 38px !important;
            transition: all 0.2s ease !important;
        }}
        div[data-testid="stNumberInput"] input:focus, 
        div[data-testid="stTextInput"] input:focus,
        div[data-testid="stSelectbox"] > div > div:focus-within {{
            border-color: var(--accent-color) !important;
            box-shadow: 0 0 0 1px var(--accent-color) !important;
        }}
        
        /* Segmented buttons/radio override */
        div[data-testid="stRadio"] div[role="radiogroup"] {{
            background-color: #F1F5F9;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 0.25rem;
            gap: 0.25rem;
        }}
        div[data-testid="stRadio"] label[data-testid="stWidgetLabel"] {{
            color: var(--text-muted) !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.3rem !important;
        }}
        
        /* Primary Submit Action Buttons */
        .stButton > button {{
            background: linear-gradient(135deg, var(--accent-color) 0%, var(--accent-gradient-end) 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.65rem 1.5rem !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            width: 100% !important;
            box-shadow: 0 4px 12px var(--accent-glow) !important;
            height: 48px !important;
            transition: all 0.2s ease !important;
        }}
        .stButton > button:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 18px var(--accent-glow) !important;
            opacity: 0.95 !important;
        }}
        
        /* Prediction Result Alert Boxes */
        .alert-card-high {{
            background-color: #FFF5F5 !important;
            border: 1.5px solid #FEB2B2 !important;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        .alert-card-low {{
            background-color: #F0FDF4 !important;
            border: 1.5px solid #BBF7D0 !important;
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        .alert-title-high {{
            color: #C53030 !important;
            font-weight: 800;
            font-size: 1.3rem;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .alert-title-low {{
            color: #15803D !important;
            font-weight: 800;
            font-size: 1.3rem;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .alert-desc {{
            color: #4A5568;
            font-size: 0.88rem;
            margin-top: 0.4rem;
            line-height: 1.5;
        }}
        
        /* Recommendation Items with Green Checkmarks */
        .check-item {{
            display: flex;
            align-items: flex-start;
            gap: 0.6rem;
            font-size: 0.88rem;
            color: #334155;
            margin-bottom: 0.5rem;
            line-height: 1.5;
        }}
        .check-icon {{
            color: #22C55E;
            font-weight: bold;
            font-size: 1.05rem;
        }}
        </style>
        """
    else:  # Dark theme (Home page only)
        return f"""
        <style>
        :root {{
            --bg-primary: #08080A;
            --bg-secondary: #0F0F12;
            --card-bg: #131317;
            --card-border: #222227;
            --text-primary: #FFFFFF;
            --text-muted: #8E8E93;
            --accent-color: {accent_color};
            --accent-gradient-end: {accent_end};
            --accent-glow: {accent_color}1a;
        }}
        
        .stApp {{
            background-color: var(--bg-primary);
        }}
        
        .premium-card {{
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 1.8rem;
            margin-bottom: 1.5rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .premium-card:hover {{
            transform: translateY(-4px);
            border-color: var(--accent-color);
            box-shadow: 0 12px 30px var(--accent-glow);
        }}
        
        .stButton > button {{
            background: linear-gradient(135deg, var(--accent-color) 0%, var(--accent-gradient-end) 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.65rem 1.5rem !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            width: 100% !important;
            box-shadow: 0 4px 12px var(--accent-glow) !important;
            height: 48px !important;
            transition: all 0.2s ease !important;
        }}
        .stButton > button:hover {{
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 18px var(--accent-glow) !important;
            opacity: 0.95 !important;
        }}
        </style>
        """

def draw_gauge(level, text):
    """Generates a premium semi-circular HTML/CSS gauge indicator."""
    color = "#22C55E" if level == "Low" else ("#F97316" if level == "Medium" else "#EF4444")
    dash = 95 if level == "Low" else (190 if level == "Medium" else 285)
    return f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin: 1rem 0;">
        <svg width="180" height="100" viewBox="0 0 180 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <!-- Gauge track -->
            <path d="M20 90 C20 45, 160 45, 160 90" stroke="#E2E8F0" stroke-width="14" stroke-linecap="round" fill="none"/>
            <!-- Gauge level -->
            <path d="M20 90 C20 45, 160 45, 160 90" stroke="{color}" stroke-width="14" stroke-linecap="round" fill="none"
                  stroke-dasharray="285" stroke-dashoffset="{285 - dash}" style="transition: stroke-dashoffset 1s ease-in-out;"/>
        </svg>
        <div style="font-size: 1.15rem; font-weight: 800; color: {color}; margin-top: -1.2rem;">{text}</div>
        <div style="font-size: 0.72rem; color: #64748B; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em; margin-top: 0.2rem;">Risk Level</div>
    </div>
    """

def draw_donut_chart(normal_cnt, borderline_cnt, abnormal_cnt, total=8):
    """Draws a clean parameter summary donut dial indicating standard normal status."""
    normal_color = "#22C55E"
    total_metrics = normal_cnt + borderline_cnt + abnormal_cnt
    normal_pct = (normal_cnt / total_metrics) * 100 if total_metrics > 0 else 100
    return f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 1.5rem; margin: 1rem 0;">
        <div style="position: relative; width: 90px; height: 90px;">
            <svg width="90" height="90" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" stroke="#F1F5F9" stroke-width="10" fill="none"/>
                <circle cx="50" cy="50" r="40" stroke="{normal_color}" stroke-width="10" fill="none"
                        stroke-dasharray="251.2" stroke-dashoffset="{251.2 - (251.2 * normal_pct / 100)}"
                        transform="rotate(-90 50 50)" style="transition: stroke-dashoffset 1s ease;"/>
            </svg>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                <div style="font-size: 1.5rem; font-weight: 800; color: #0F172A; line-height: 1;">{normal_cnt}</div>
                <div style="font-size: 0.62rem; color: #64748B; font-weight: 600; margin-top: 0.15rem;">/{total_metrics}</div>
            </div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 0.35rem; font-size: 0.78rem;">
            <div style="display: flex; align-items: center; gap: 0.4rem;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #22C55E; display: inline-block;"></span>
                <span style="color: #22C55E; font-weight: 700;">{normal_cnt}</span> <span style="color: #64748B;">Normal</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.4rem;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #F97316; display: inline-block;"></span>
                <span style="color: #F97316; font-weight: 700;">{borderline_cnt}</span> <span style="color: #64748B;">Borderline</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.4rem;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #EF4444; display: inline-block;"></span>
                <span style="color: #EF4444; font-weight: 700;">{abnormal_cnt}</span> <span style="color: #64748B;">High</span>
            </div>
        </div>
    </div>
    """

# Beautiful high-end medical illustrations drawn via vector SVG
def get_heart_svg():
    return """
    <div style="display:flex; justify-content:center; align-items:center; padding:0.5rem;">
    <svg width="90" height="90" viewBox="0 0 150 150" fill="none" xmlns="http://www.w3.org/2000/svg" class="animate-pulse">
        <path d="M75 125C75 125 20 85 20 45C20 22.5 37.5 10 60 10C75 10 75 25 75 25C75 25 75 10 90 10C112.5 10 130 22.5 130 45C130 85 75 125 75 125Z" fill="url(#heartGrad)" stroke="var(--accent-color)" stroke-width="2"/>
        <path d="M45 40C45 40 40 45 40 55" stroke="white" stroke-width="3" stroke-linecap="round" opacity="0.6"/>
        <path d="M25 75 H50 M100 75 H125" stroke="var(--accent-color)" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.4"/>
        <defs>
            <radialGradient id="heartGrad" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(75 45) rotate(90) scale(80)">
                <stop offset="0%" stop-color="#FF5252"/>
                <stop offset="100%" stop-color="#B71C1C"/>
            </radialGradient>
        </defs>
    </svg>
    </div>
    """

def get_liver_svg():
    return """
    <div style="display:flex; justify-content:center; align-items:center; padding:0.5rem;">
    <svg width="95" height="90" viewBox="0 0 150 150" fill="none" xmlns="http://www.w3.org/2000/svg" class="animate-pulse">
        <path d="M20 70C20 40 60 20 100 30C130 38 135 65 130 85C125 105 90 120 75 120C60 120 40 115 30 100C20 85 20 80 20 70Z" fill="url(#liverGrad)" stroke="var(--accent-color)" stroke-width="2"/>
        <path d="M75 30C75 30 80 60 70 120" stroke="var(--accent-color)" stroke-width="1.5" stroke-dasharray="2 2" opacity="0.5"/>
        <circle cx="50" cy="60" r="4" fill="#00C853" opacity="0.8"/>
        <circle cx="95" cy="75" r="5" fill="#00C853" opacity="0.8"/>
        <defs>
            <radialGradient id="liverGrad" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(75 70) rotate(90) scale(70)">
                <stop offset="0%" stop-color="#00E676"/>
                <stop offset="100%" stop-color="#004D40"/>
            </radialGradient>
        </defs>
    </svg>
    </div>
    """

def get_kidney_svg():
    return """
    <div style="display:flex; justify-content:center; align-items:center; padding:0.5rem;">
    <svg width="90" height="90" viewBox="0 0 160 150" fill="none" xmlns="http://www.w3.org/2000/svg" class="animate-pulse">
        <path d="M45 25C25 35 25 85 45 115C55 125 65 115 65 95C60 85 60 55 65 45C65 25 55 15 45 25Z" fill="url(#kidneyGrad)" stroke="var(--accent-color)" stroke-width="2"/>
        <path d="M115 25C135 35 135 85 115 115C105 125 95 115 95 95C100 85 100 55 95 45C95 25 105 15 115 25Z" fill="url(#kidneyGrad)" stroke="var(--accent-color)" stroke-width="2"/>
        <path d="M57 70 C70 75 75 80 80 120 M103 70 C90 75 85 80 80 120" stroke="#1E88E5" stroke-width="2" opacity="0.6"/>
        <defs>
            <linearGradient id="kidneyGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#2979FF"/>
                <stop offset="100%" stop-color="#0D47A1"/>
            </linearGradient>
        </defs>
    </svg>
    </div>
    """

def get_diabetes_svg():
    return """
    <div style="display:flex; justify-content:center; align-items:center; padding:0.5rem;">
    <svg width="90" height="90" viewBox="0 0 150 150" fill="none" xmlns="http://www.w3.org/2000/svg" class="animate-pulse">
        <path d="M75 15C75 15 115 65 115 95C115 117.1 97.1 135 75 135C52.9 135 35 117.1 35 95C35 65 75 15 75 15Z" fill="url(#diabGrad)" stroke="var(--accent-color)" stroke-width="2"/>
        <circle cx="75" cy="95" r="45" stroke="var(--accent-color)" stroke-width="1" stroke-dasharray="5 5" opacity="0.4"/>
        <circle cx="75" cy="50" r="6" fill="white" opacity="0.3"/>
        <circle cx="120" cy="95" r="4" fill="var(--accent-color)" opacity="0.7"/>
        <defs>
            <radialGradient id="diabGrad" cx="0" cy="0" r="1" gradientUnits="userSpaceOnUse" gradientTransform="translate(75 95) rotate(90) scale(55)">
                <stop offset="0%" stop-color="#2979FF"/>
                <stop offset="100%" stop-color="#1A237E"/>
            </radialGradient>
        </defs>
    </svg>
    </div>
    """
