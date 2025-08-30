import streamlit as st

def apply_styling(theme="dark", primary_color="#673DC9"):
    """
    Applies custom CSS styling to a Streamlit app with a focus on a dark, vibrant theme.

    Parameters:
    - theme (str): The theme to apply. Can be 'dark' or 'light'. Defaults to 'dark'.
    - primary_color (str): The primary accent color for the theme. Defaults to a vibrant purple.
    """
    
    # 🎨 Define color palettes for dark and light themes
    dark_theme_colors = {
        "background": "#1b061c",  # Dark background for the page
        "sidebar_bg": "#4f0a4b",  # Slightly lighter dark background for the sidebar
        "secondary": "#262B34",   # A subtle secondary dark color
        "accent": "#FFD633",      # A bright accent color
        "text_color": "#E0E0E0",  # Light text for contrast
        "caption_color": "#A0A0A0", # Muted light text for captions
    }

    light_theme_colors = {
        "background": "#F0F2F6",  
        "sidebar_bg": "#FFFFFF",  
        "secondary": "#E0E5EC",   
        "accent": "#FF4B4B",      
        "text_color": "#262626",  
        "caption_color": "#7A7A7A", 
    }
    
    # 🖼️ Set colors based on the selected theme
    colors = dark_theme_colors if theme == "dark" else light_theme_colors
    
    # Apply primary_color dynamically
    colors["primary"] = primary_color

    # 📝 Define font families
    font_family = "'Century Gothic', 'Futura', sans-serif"
    
    # 💻 Inject custom CSS using st.markdown with an unsafe_allow_html flag
    st.markdown(f"""
    <style>
    
    /* -------------------- 🎨 Global Styles -------------------- */
    
    @import url('https://fonts.googleapis.com/css2?family=Century+Gothic:wght@300;400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {{
        font-family: {font_family};
        background-color: {colors["background"]};
        color: {colors["text_color"]};
    }}

    /* -------------------- ⚙️ Sidebar Styling -------------------- */
    
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #4f0a4b 0%, #2a0526 50%, #1b061c 100%);
        border-right: 2px solid rgba(250, 181, 21, 0.2);
    }}

    .st-emotion-cache-16txtv3 {{ /* Sidebar widget labels */
        color: {colors["text_color"]};
    }}

    /* Sidebar content padding adjustment */
    [data-testid="stSidebar"] .st-emotion-cache-1d391kg {{
        padding-top: 2rem;
    }}

    /* -------------------- ✍️ Text and Header Styling -------------------- */
    
    h1, h2, h3, h4, h5, h6 {{
        color: {colors["primary"]};
        font-family: {font_family};
    }}
    
    p, label, .st-emotion-cache-16txtv3, .st-emotion-cache-1y4y1q, .st-emotion-cache-1b6p98 {{
        color: {colors["text_color"]};
    }}

    .st-emotion-cache-1jm98wq {{ /* Caption text */
        color: {colors["caption_color"]};
    }}

    /* -------------------- 🔘 Button and Widget Styling -------------------- */
    
    div.stButton > button {{
        background-color: {colors["primary"]};
        color: white;
        border-radius: 5px;
        border: none;
        transition: background-color 0.3s;
    }}
    
    div.stButton > button:hover {{
        background-color: {colors["primary"]}E0;
    }}
    
    div.stButton > button:active {{
        background-color: {colors["primary"]}C0;
    }}
    
    div.stButton > button:disabled {{
        background-color: {colors["secondary"]};
        color: {colors["caption_color"]};
        cursor: not-allowed;
    }}


    /* -------------------- 📦 Card/Container Styling -------------------- */
    
    .st-emotion-cache-1c99r31, .st-emotion-cache-1oe5f0g {{ /* Containers (st.container) */
        background-color: {colors["sidebar_bg"]};
        border: 1px solid {colors["secondary"]};
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.1);
        transition: box-shadow 0.3s;
    }}

    .st-emotion-cache-1c99r31:hover, .st-emotion-cache-1oe5f0g:hover {{
        box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
    }}

    </style>
    """, unsafe_allow_html=True)