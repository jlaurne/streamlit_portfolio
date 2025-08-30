import streamlit as st

def apply_custom_styles():
    """
    Apply custom CSS styling with dark green palette and Montserrat font:
    - Primary Background: #02281e (deepest shade)
    - Secondary Background: #003e2c (evergreen panels)
    - Accent/Headers: #87ad7a (sage highlight)
    - Borders/Dividers: #325326 (natural deep green)
    - Hover/Active States: #02381b (forest green)
    - Font: Montserrat (all elements)
    """
    st.markdown("""
    <style>
        /* ==== FONT IMPORT ==== */
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&display=swap');
        
        /* ==== GLOBAL TYPOGRAPHY ==== */
        html, body, [class*="st-"], .stApp, div, p, h1, h2, h3, h4, h5, h6, span, button, table, .stMarkdown {
            font-family: 'Montserrat', sans-serif !important;
            color: #e4e8e6 !important;
        }

        /* ==== APP BACKGROUND ==== */
        .stApp {
            background-color: #02281e !important;
        }
        .main .block-container {
            background-color: #02281e !important;
            padding: 2rem 1rem !important;
        }

        /* ==== HEADINGS ==== */
        h1 {
            color: #87ad7a !important; 
            font-weight: 600 !important;
            font-size: 2.2rem !important;
            line-height: 1.3 !important;
            margin-bottom: 1.2rem !important;
        }
        h2 {
            color: #87ad7a !important; 
            font-weight: 500 !important;
            font-size: 1.6rem !important;
            margin-bottom: 1rem !important;
        }
        h3 {
            color: #325326 !important; 
            font-weight: 500 !important;
            font-size: 1.3rem !important;
            margin-bottom: 0.8rem !important;
        }

        /* ==== BODY TEXT ==== */
        p, li, span, div {
            font-weight: 400 !important;
            font-size: 1rem !important;
            line-height: 1.6 !important;
        }
        strong, b {
            color: #87ad7a !important;
            font-weight: 600 !important;
        }

        /* ==== SIDEBAR ==== */
        section[data-testid="stSidebar"] {
            background-color: #003e2c !important;
            border-right: 1px solid #325326 !important;
        }
        .stSidebar p, .stSidebar span, .stSidebar div {
            color: #e4e8e6 !important;
            font-size: 0.95rem !important;
        }

        /* ==== BUTTONS ==== */
        .stButton>button {
            background-color: #003e2c !important;
            color: #e4e8e6 !important;
            border: 1px solid #325326 !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.2rem !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #02381b !important;
            color: #87ad7a !important;
            transform: translateY(-2px);
        }

        /* ==== TABLES ==== */
        table {
            border-collapse: collapse !important;
            width: 100% !important;
            font-size: 0.95rem !important;
        }
        th {
            background-color: #003e2c !important;
            color: #87ad7a !important;
            font-weight: 600 !important;
            border-bottom: 2px solid #325326 !important;
            padding: 0.75rem !important;
        }
        td {
            background-color: #02281e !important;
            color: #e4e8e6 !important;
            border-bottom: 1px solid #325326 !important;
            padding: 0.75rem !important;
        }
        tr:hover td {
            background-color: #02381b !important;
        }
    </style>
    """, unsafe_allow_html=True)


def apply_page_config():
    """
    Apply common page configuration for Streamlit apps.
    
    IMPORTANT: This must be called FIRST, before any other Streamlit commands!
    """
    st.set_page_config(
        page_title="Laurné Jones | Portfolio", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )
