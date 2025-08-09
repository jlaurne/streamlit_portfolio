import streamlit as st
import pandas as pd
import numpy as np

# Page configuration (keep this as is)
st.set_page_config(
    page_title="Laurné Jones - Data Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling with Montserrat font and your color palette

st.markdown("""

<style>

@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');


/* Force Montserrat on ALL text elements */

html, body, [class*="css"], .stSelectbox, .stSlider, .stMetric, .stMarkdown,

.stText, h1, h2, h3, h4, h5, h6, p, div, span, label, .stButton > button {

font-family: 'Montserrat', sans-serif !important;

}


/* Override Streamlit's default fonts */

.css-10trblm, .css-16idsys, .css-1kyxreq, .css-1adrfps {

font-family: 'Montserrat', sans-serif !important;

}


.main-header {

font-family: 'Montserrat', sans-serif !important;

font-size: 3.2rem;

font-weight: 700;

color: #8B4513;

text-align: center;

margin-bottom: 1rem;

text-shadow: 2px 2px 4px rgba(139, 69, 19, 0.1);

}


.section-header {

font-family: 'Montserrat', sans-serif !important;

font-size: 2.2rem;

font-weight: 600;

color: #2F4F4F;

margin-top: 2rem;

margin-bottom: 1rem;

border-bottom: 3px solid #8FBC8F;

padding-bottom: 0.5rem;

}


.highlight-box {

background: linear-gradient(135deg, #F5F5DC 0%, #FAEBD7 100%);

padding: 1.8rem;

border-radius: 15px;

border-left: 5px solid #8FBC8F;

box-shadow: 0 6px 15px rgba(143, 188, 143, 0.2);

margin-bottom: 1.5rem;

font-family: 'Montserrat', sans-serif !important;

}


.highlight-box h3 {

color: #8B4513 !important;

font-family: 'Montserrat', sans-serif !important;

font-weight: 600;

margin-bottom: 1rem;

}


.metric-card {

background: linear-gradient(135deg, #ffffff 0%, #F5F5DC 100%);

padding: 1.8rem;

border-radius: 15px;

box-shadow: 0 6px 20px rgba(143, 188, 143, 0.25);

border: 2px solid #8FBC8F;

font-family: 'Montserrat', sans-serif !important;

}


.work-in-progress {

background: linear-gradient(135deg, #FFF8DC 0%, #FFFACD 100%);

padding: 1rem;

border-radius: 10px;

border-left: 4px solid #DAA520;

margin: 1rem 0;

font-style: italic;

color: #B8860B;

font-family: 'Montserrat', sans-serif !important;

font-weight: 500;

}


.about-text {

font-family: 'Montserrat', sans-serif !important;

font-size: 1.1rem;

line-height: 1.7;

color: #2F4F4F;

text-align: justify;

font-weight: 400;

}


.profile-image {

border-radius: 50%;

border: 4px solid #8FBC8F;

box-shadow: 0 6px 20px rgba(143, 188, 143, 0.4);

}


/* Subtitle styling */

.subtitle {

text-align: center;

font-size: 1.3rem;

color: #2F4F4F;

margin-bottom: 2rem;

font-weight: 500;

font-family: 'Montserrat', sans-serif !important;

}


/* Link styling */

a, .stMarkdown a {

color: #8B4513 !important;

font-family: 'Montserrat', sans-serif !important;

font-weight: 500;

text-decoration: none;

}


a:hover, .stMarkdown a:hover {

color: #2F4F4F !important;

text-decoration: underline;

}


/* Sidebar styling */

.css-1d391kg {

background: linear-gradient(180deg, #F5F5DC 0%, #FAEBD7 100%);

}


/* Selectbox and other inputs */

.stSelectbox label, .stSlider label, .stFileUploader label {

font-family: 'Montserrat', sans-serif !important;

color: #2F4F4F !important;

font-weight: 500;

}


/* Metrics styling */

.css-1xarl3l {

font-family: 'Montserrat', sans-serif !important;

}


/* Button styling */

.stButton > button {

background: linear-gradient(135deg, #8FBC8F 0%, #9ACD32 100%);

color: white;

font-family: 'Montserrat', sans-serif !important;

font-weight: 600;

border: none;

border-radius: 8px;

padding: 0.5rem 1rem;

}


.stButton > button:hover {

background: linear-gradient(135deg, #2F4F4F 0%, #8B4513 100%);

transform: translateY(-2px);

box-shadow: 0 4px 8px rgba(47, 79, 79, 0.3);

}

</style>

""", unsafe_allow_html=True)




# --- START: HOME PAGE CONTENT ---
# This is the content that will always display for your main page.

st.sidebar.success("Select a project above to get started.")

st.markdown('<div class="main-header">Laurné Jones</div>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Data Strategy Professional | Analytics Engineer | Insights Architect</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.markdown("### 🚀 Data Solutioning")
    st.write("Building end-to-end data tools and dashboards.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.markdown("### 📊 Metric Exploration")
    st.write("Creating tools for defining and exploring key metrics.")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
    st.markdown("### 🏙️ Urban Analytics")
    st.write("Profiling cities and communities through data.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Professional background summary
st.markdown('<div class="section-header">Professional Background</div>', unsafe_allow_html=True)

col1_bg, col2_bg = st.columns([2, 1])
with col1_bg:
    st.markdown("""
    <div class="about-text">
    My career journey has spanned various industries, from consulting at Deloitte and IBM to spearheading data initiatives in immersive commerce at Walmart's Store No. 8. My current role is Sr. Analytics Engineer at The Walt Disney Company, where I lead the design and development of unified data solutions for Organizational Management and broader HR initiatives.
    <br><br>
    This multi-page application showcases a collection of my data projects. Each project is a self-contained Streamlit app, demonstrating different facets of my technical and analytical skills. Use the navigation panel on the left to explore each one.
    </div>
    """, unsafe_allow_html=True)

with col2_bg:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Years Experience", "6+")
    st.metric("Industries", "5+")
    st.metric("Advanced Degrees", "2")
    st.markdown('</div>', unsafe_allow_html=True)


# Footer (keep this as is)
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #2F4F4F; font-family: Montserrat, sans-serif;">Built with Streamlit | '
    '<a href="https://www.linkedin.com/in/laurnejones/" style="color: #8B4513; font-weight: 500;">LinkedIn</a> | '
    '<a href="mailto:laurne3@gmail.com" style="color: #8B4513; font-weight: 500;">laurne3@gmail.com</a></div>', 
    unsafe_allow_html=True
)
# --- END: HOME PAGE CONTENT ---