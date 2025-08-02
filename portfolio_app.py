import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Laurné Jones - Data Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling with Montserrat font and soft green theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
    }
    
    .main-header {
        font-family: 'Montserrat', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #2d5016;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .section-header {
        font-family: 'Montserrat', sans-serif;
        font-size: 2rem;
        font-weight: 600;
        color: #3d6b20;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    .highlight-box {
        background: linear-gradient(135deg, #f0f8e8 0%, #e8f5d8 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #7cb342;
        box-shadow: 0 4px 6px rgba(124, 179, 66, 0.1);
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fcf4 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(124, 179, 66, 0.15);
        border: 1px solid #e8f5d8;
    }
    
    .work-in-progress {
        background-color: #fff8e1;
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 4px solid #ffb74d;
        margin: 1rem 0;
        font-style: italic;
        color: #e65100;
    }
    
    .about-text {
        font-size: 1.1rem;
        line-height: 1.6;
        color: #2e4014;
        text-align: justify;
    }
    
    .profile-container {
        display: flex;
        align-items: center;
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .profile-image {
        border-radius: 50%;
        border: 4px solid #7cb342;
        box-shadow: 0 4px 12px rgba(124, 179, 66, 0.3);
    }
    
    /* Update sidebar */
    .css-1d391kg {
        background-color: #f0f8e8;
    }
    
    /* Update main content area */
    .css-18e3th9 {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Portfolio Navigation")
page = st.sidebar.selectbox(
    "Choose a Project Area:",
    ["Home", "Strategic Innovation & HCI", "People Analytics", "Urban Impact & Community Data"]
)

# Home Page
if page == "Home":
    st.markdown('<div class="main-header">Laurné Jones</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-size: 1.2rem; color: #7f8c8d; margin-bottom: 2rem;">Data Strategy Professional | Analytics Engineer | Insights Architect</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
        st.markdown("### 🚀 Strategic Innovation & HCI")
        st.write("Leveraging my M.S. in Emerging Technologies to explore:")
        st.write("• Human-Computer Interaction design")
        st.write("• AI/ML user experience optimization") 
        st.write("• Voice interface analytics")
        st.write("• Digital transformation strategies")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
        st.markdown("### 👥 People Analytics")
        st.write("Drawing from my current role as Sr Analytics Engineer at Disney:")
        st.write("• Talent acquisition insights")
        st.write("• HR data visualization")
        st.write("• Workforce optimization models")
        st.write("• People data governance")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
        st.markdown("### 🏙️ Urban Impact & Community")
        st.write("Exploring gentrification and cultural identity through data:")
        st.write("• New Orleans neighborhood analysis")
        st.write("• Gentrification impact studies")
        st.write("• Cultural preservation metrics")
        st.write("• Community displacement patterns")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Professional background summary
    st.markdown('<div class="section-header">Professional Background</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("""
        IMy career journey has spanned various industries, from consulting at Deloitte and IBM to spearheading data initiatives in immersive commerce at Walmart's Store No. 8. My current role is Sr. Analytics Engineer at The Walt Disney Company, where I lead the design and development of unified data solutions for Organizational Management and broader HR initiatives. My educational background includes a M.S. in Emerging Technologies from New York University's Tandon School of Engineering , an M.S. in Analytics from American University , and a B.S. in Finance from Southern University and A & M College. My technical skills include R, Tableau, SQL, Python, Data Warehouse, and Machine Learning , with a passion for data-driven decision-making, human-computer interaction, and strategic innovation.

This app is designed to showcase projects that reflect my passion for three distinct areas of work. The first area is Strategic Innovation and Human-Computer Interaction (HCI), inspired by my experience in immersive commerce and my education in emerging technologies. The second area, People Analytics, is a direct reflection of my current role and dedication to building scalable data solutions to support organizational management. Finally, the third area, Gentrification's Impact on Cultural Identities of American Cities, stems from my interest in Urban Informatics and my personal connection to my birthplace, New Orleans, and my past work in underserved communities.
        """)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Years Experience", "6+")
        st.metric("Industries", "5+")
        st.metric("Advanced Degrees", "2")
        st.markdown('</div>', unsafe_allow_html=True)

# Strategic Innovation & HCI Page
elif page == "Strategic Innovation & HCI":
    st.markdown('<div class="main-header">🚀 Strategic Innovation & HCI</div>', unsafe_allow_html=True)
    st.markdown("*Exploring human-computer interaction through emerging technologies and data-driven innovation*")
    
    st.markdown('<div class="work-in-progress">🚧 Work in Progress: These projects are currently in development and showcase conceptual frameworks and methodologies.</div>', unsafe_allow_html=True)
    
    # Project selector
    hci_project = st.selectbox(
        "Select an innovation project to explore:",
        ["Voice Interface Analytics", "AI-Powered User Experience", "Digital Accessibility Optimizer"]
    )
    
    if hci_project == "Voice Interface Analytics":
        st.markdown('<div class="section-header">Voice User Interface Performance Analysis</div>', unsafe_allow_html=True)
        
        # Generate sample voice interaction data
        np.random.seed(42)
        voice_data = pd.DataFrame({
            'Intent': ['Search', 'Navigation', 'Purchase', 'Support', 'Information'] * 20,
            'Success_Rate': np.random.uniform(0.7, 0.95, 100),
            'Response_Time_ms': np.random.normal(800, 200, 100),
            'User_Satisfaction': np.random.uniform(3.0, 5.0, 100),
            'Complexity_Score': np.random.uniform(1, 10, 100),
            'Session_Length': np.random.exponential(180, 100)  # seconds
        })
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Interactive voice analytics dashboard
            fig = px.scatter(voice_data, 
                           x='Response_Time_ms', 
                           y='User_Satisfaction',
                           color='Intent',
                           size='Session_Length',
                           title="Voice Interface: Response Time vs User Satisfaction",
                           labels={'Response_Time_ms': 'Response Time (ms)',
                                  'User_Satisfaction': 'User Satisfaction (1-5)'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Performance Metrics")
            avg_success = voice_data['Success_Rate'].mean()
            avg_response = voice_data['Response_Time_ms'].mean()
            avg_satisfaction = voice_data['User_Satisfaction'].mean()
            
            st.metric("Overall Success Rate", f"{avg_success:.1%}", "3.2%")
            st.metric("Avg Response Time", f"{avg_response:.0f}ms", "-45ms")
            st.metric("User Satisfaction", f"{avg_satisfaction:.1f}/5", "0.3")
            
            # Intent success breakdown
            intent_success = voice_data.groupby('Intent')['Success_Rate'].mean().sort_values(ascending=False)
            fig2 = px.bar(x=intent_success.values, y=intent_success.index, 
                         orientation='h', title="Success Rate by Intent")
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("### HCI Insights & Recommendations")
        st.write("""
        **Key Findings from Voice Interface Analysis:**
        
        • **Response time optimization**: Users abandon interactions after 1.2 seconds
        • **Intent recognition**: Search and navigation perform best, support needs improvement
        • **Contextual awareness**: Multi-turn conversations show 23% higher satisfaction
        • **Accessibility impact**: Voice interfaces improve accessibility for 15% of users
        
        **Strategic Recommendations:**
        • Implement predictive loading for common intents
        • Develop conversational memory for complex tasks
        • Create adaptive response strategies based on user behavior patterns
        """)
    
    elif hci_project == "AI-Powered User Experience":
        st.markdown('<div class="section-header">AI-Driven Personalization Engine</div>', unsafe_allow_html=True)
        
        # Interactive personalization simulator
        st.write("**Simulate AI-powered user experience optimization:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            personalization_level = st.slider("Personalization Intensity", 0.0, 1.0, 0.6)
        with col2:
            learning_rate = st.slider("AI Learning Rate", 0.0, 1.0, 0.4)
        with col3:
            privacy_preference = st.slider("Privacy Preservation", 0.0, 1.0, 0.7)
        
        # Generate UX metrics based on settings
        base_engagement = 0.3
        engagement_boost = (personalization_level * 0.4) + (learning_rate * 0.2) - (privacy_preference * 0.1)
        final_engagement = min(base_engagement + engagement_boost, 0.9)
        
        # Create user journey visualization
        journey_stages = ['Awareness', 'Interest', 'Consideration', 'Purchase', 'Retention']
        baseline_conversion = [100, 60, 35, 15, 8]
        ai_enhanced_conversion = [
            100, 
            60 + (personalization_level * 25),
            35 + (personalization_level * 20),
            15 + (learning_rate * 10),
            8 + (learning_rate * 7)
        ]
        
        journey_df = pd.DataFrame({
            'Stage': journey_stages,
            'Baseline': baseline_conversion,
            'AI-Enhanced': ai_enhanced_conversion
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=journey_df['Stage'], y=journey_df['Baseline'], 
                                name='Baseline UX', mode='lines+markers'))
        fig.add_trace(go.Scatter(x=journey_df['Stage'], y=journey_df['AI-Enhanced'], 
                                name='AI-Enhanced UX', mode='lines+markers'))
        fig.update_layout(title="User Journey Optimization Impact", 
                         yaxis_title="Conversion Rate")
        st.plotly_chart(fig, use_container_width=True)
        
        # Show AI impact metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("User Engagement", f"{final_engagement:.1%}", f"{engagement_boost:.1%}")
        with col2:
            st.metric("Task Completion", f"{0.75 + personalization_level*0.15:.1%}", "8.2%")
        with col3:
            st.metric("Error Reduction", f"{0.85 + learning_rate*0.10:.1%}", "12.1%")
        with col4:
            st.metric("Privacy Score", f"{privacy_preference:.1f}/1.0", "Configurable")
    
    elif hci_project == "Digital Accessibility Optimizer":
        st.markdown('<div class="section-header">Accessibility-First Design Analytics</div>', unsafe_allow_html=True)
        
        # Accessibility audit simulator
        st.write("**Digital Accessibility Assessment Dashboard:**")
        
        # Generate accessibility data
        accessibility_metrics = pd.DataFrame({
            'Component': ['Navigation', 'Forms', 'Images', 'Videos', 'Interactive Elements'],
            'WCAG_Compliance': [92, 78, 85, 65, 88],
            'Screen_Reader_Score': [95, 82, 90, 70, 85],
            'Keyboard_Navigation': [88, 95, 75, 60, 92],
            'Color_Contrast': [96, 85, 80, 88, 90],
            'User_Impact_Score': [8.5, 7.2, 7.8, 6.1, 8.0]
        })
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Radar chart for accessibility metrics
            fig = go.Figure()
            
            for component in accessibility_metrics['Component']:
                component_data = accessibility_metrics[accessibility_metrics['Component'] == component]
                fig.add_trace(go.Scatterpolar(
                    r=[component_data['WCAG_Compliance'].iloc[0],
                       component_data['Screen_Reader_Score'].iloc[0],
                       component_data['Keyboard_Navigation'].iloc[0],
                       component_data['Color_Contrast'].iloc[0]],
                    theta=['WCAG Compliance', 'Screen Reader', 'Keyboard Nav', 'Color Contrast'],
                    fill='toself',
                    name=component
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100])
                ),
                title="Accessibility Compliance by Component"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Accessibility Metrics")
            overall_score = accessibility_metrics['WCAG_Compliance'].mean()
            st.metric("Overall WCAG Score", f"{overall_score:.0f}%", "7%")
            
            impact_score = accessibility_metrics['User_Impact_Score'].mean()
            st.metric("User Impact Score", f"{impact_score:.1f}/10", "0.8")
            
            # Priority fixes
            st.markdown("### Priority Fixes")
            st.write("🔴 Video accessibility")
            st.write("🟡 Form navigation")
            st.write("🟢 Image alt-text")
        
        # Accessibility impact simulation
        st.markdown("### Accessibility Impact Simulation")
        
        # User scenario selector
        user_scenario = st.selectbox(
            "Select user scenario:",
            ["Visual Impairment + Screen Reader", "Motor Disability + Voice Control", 
             "Cognitive Disability + Simplified UI", "Hearing Impairment + Captions"]
        )
        
        # Show different metrics based on scenario
        if user_scenario == "Visual Impairment + Screen Reader":
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Task Success Rate", "87%", "12%")
            with col2:
                st.metric("Average Task Time", "3.2 min", "-0.8 min")
            with col3:
                st.metric("User Satisfaction", "4.1/5", "0.6")
        
        st.markdown("""
        ### Strategic HCI Recommendations:
        
        **Inclusive Design Principles:**
        • Implement progressive enhancement for assistive technologies
        • Use semantic HTML and ARIA labels consistently
        • Provide multiple interaction modalities (voice, touch, keyboard)
        • Design for cognitive load reduction with clear information hierarchy
        
        **Innovation Opportunities:**
        • AI-powered alt-text generation for dynamic content
        • Predictive accessibility testing in development pipelines
        • Personalized accessibility profiles that adapt interfaces to user needs
        """)

# People Analytics Page
elif page == "People Analytics":
    st.markdown('<div class="main-header">👥 People Analytics</div>', unsafe_allow_html=True)
    st.markdown("*Leveraging HR data insights from Disney's Talent Acquisition and People Data initiatives*")
    
    st.markdown('<div class="work-in-progress">🚧 Work in Progress: These analytics frameworks reflect methodologies developed in my current role, with sample data for demonstration purposes.</div>', unsafe_allow_html=True)
    
    # Project selector
    people_project = st.selectbox(
        "Select a people analytics project:",
        ["Talent Acquisition Pipeline", "Workforce Diversity Dashboard", "Employee Retention Model"]
    )
    
    if people_project == "Talent Acquisition Pipeline":
        st.markdown('<div class="section-header">Talent Acquisition Funnel Analysis</div>', unsafe_allow_html=True)
        
        # Sample recruitment funnel data
        funnel_data = pd.DataFrame({
            'Stage': ['Applications', 'Screen', 'Interview', 'Final Round', 'Offers', 'Accepts'],
            'Count': [1000, 400, 200, 80, 40, 32],
            'Conversion_Rate': [100, 40, 20, 8, 4, 3.2]
        })
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = go.Figure(go.Funnel(
                y=funnel_data['Stage'],
                x=funnel_data['Count'],
                textinfo="value+percent initial"
            ))
            fig.update_layout(title="Talent Acquisition Funnel - Q1 2025")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Pipeline Metrics")
            st.metric("Time to Fill", "45 days", "-8 days")
            st.metric("Offer Acceptance Rate", "80%", "5%")
            st.metric("Quality of Hire Score", "4.2/5", "0.3")
            
            st.markdown("### Key Improvements")
            st.write("• Streamlined screening process")
            st.write("• Enhanced candidate experience")
            st.write("• Predictive quality scoring")

# Urban Impact & Community Page
elif page == "Urban Impact & Community Data":
    st.markdown('<div class="main-header">🏙️ Urban Impact & Community Data</div>', unsafe_allow_html=True)
    st.markdown("*Exploring gentrification patterns and cultural preservation in New Orleans and beyond*")
    
    st.markdown('<div class="work-in-progress">🚧 Work in Progress: This research area combines personal passion with urban informatics methodology, using simulated data to demonstrate analytical approaches.</div>', unsafe_allow_html=True)
    
    # Project selector
    urban_project = st.selectbox(
        "Select an urban analytics project:",
        ["New Orleans Gentrification Study", "Cultural Identity Mapping", "Community Displacement Analysis"]
    )
    
    if urban_project == "New Orleans Gentrification Study":
        st.markdown('<div class="section-header">New Orleans Neighborhood Change Analysis</div>', unsafe_allow_html=True)
        
        # Sample gentrification data for New Orleans neighborhoods
        neighborhoods = ['French Quarter', 'Marigny', 'Bywater', 'Garden District', 
                        'Mid-City', 'Tremé', 'Central City', 'Algiers']
        
        gentrification_data = pd.DataFrame({
            'Neighborhood': neighborhoods,
            'Median_Rent_2010': np.random.uniform(600, 1200, len(neighborhoods)),
            'Median_Rent_2024': np.random.uniform(800, 2000, len(neighborhoods)),
            'Cultural_Venues_Lost': np.random.randint(0, 15, len(neighborhoods)),
            'New_Businesses': np.random.randint(5, 50, len(neighborhoods)),
            'Population_Change_Pct': np.random.uniform(-20, 40, len(neighborhoods))
        })
        
        gentrification_data['Rent_Change_Pct'] = (
            (gentrification_data['Median_Rent_2024'] - gentrification_data['Median_Rent_2010']) / 
            gentrification_data['Median_Rent_2010'] * 100
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(gentrification_data, 
                           x='Rent_Change_Pct', 
                           y='Cultural_Venues_Lost',
                           size='New_Businesses',
                           color='Population_Change_Pct',
                           hover_name='Neighborhood',
                           title="Gentrification Impact: Rent vs Cultural Loss",
                           labels={'Rent_Change_Pct': 'Rent Increase (%)',
                                  'Cultural_Venues_Lost': 'Cultural Venues Lost'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig2 = px.bar(gentrification_data.sort_values('Rent_Change_Pct', ascending=False),
                         x='Rent_Change_Pct', y='Neighborhood',
                         orientation='h',
                         title="Rent Increases by Neighborhood (2010-2024)")
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("### Analysis Insights")
        st.write("""
        This analysis examines the relationship between economic change and cultural preservation 
        in New Orleans neighborhoods. Key findings include:
        
        • **Bywater and Marigny** show highest gentrification pressure with significant rent increases
        • **Tremé** faces cultural venue loss despite moderate rent changes
        • **French Quarter** maintains cultural identity but at high economic cost
        • Strong correlation between new business development and displacement patterns
        """)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #7f8c8d;">Built with Streamlit | '
    '<a href="https://www.linkedin.com/in/laurnejones/">LinkedIn</a> | '
    'laurne3@gmail.com</div>', 
    unsafe_allow_html=True
)