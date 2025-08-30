import streamlit as st
import pandas as pd
import numpy as np

# Import modules
from hr_data_module import hr_data_module
from hr_visualizations_module import hr_visualizations_module
from hr_filters_module import hr_filters_module
from hr_forms_module import hr_forms_module
from hr_data_connections import hr_data_connections_module
from hr_capstone_module import hr_capstone_module
from deployment_module import deployment_module
from utils.styling import apply_styling

apply_styling()

def main():
    st.set_page_config(
        page_title="Streamlit App Showcase",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for branding
    #st.markdown("""
    #<style>
    #.main-header {
    #    font-family: 'Trebuchet MS', sans-serif;
    #    color: #6C5CE7;
    #}
    #.subheader {
    #    font-family: 'Trebuchet MS', sans-serif;
    #    color: #A29BFE;
    #}
    #.sidebar-content {
    #    background-color: #F8F9FA;
    #    padding: 10px;
    #    border-radius: 5px;
    #}
    #.metric-card {
    #    background-color: #F8F9FA;
    #    padding: 15px;
    #    border-radius: 5px;
    #    box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    #}
    #</style>
    #""", unsafe_allow_html=True)

    # Sidebar navigation
    with st.sidebar:
        st.title("People Insights Streamlit Showcase")
        st.markdown("**[Image Placeholder: Company Logo]**")

        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.markdown("## Showcase Navigation")

        # Navigation options with emoji icons
        pages = {
            "🏠 Introduction": intro_page,
            "📝 HR Data Fundamentals": hr_data_module,
            "📊 HR Data Visualization": hr_visualizations_module,
            "🔍 Interactive HR Filters": hr_filters_module,
            "📋 HR Forms & Data Collection": hr_forms_module,
            "🔌 HR Data Connections": hr_data_connections_module,
            "🏆 PI analytics Dashboard": hr_capstone_module,
            "🚀 Snowflake Deployment": deployment_module,
        }

        # Create a selection box for navigation
        selection = st.radio("Explore Features:", list(pages.keys()))
        st.markdown('</div>', unsafe_allow_html=True)

        # Additional resources
        st.markdown("---")
        st.markdown("## Resources")

        with st.expander("Internal Resources"):
            st.markdown("""
            - Product Engineering Teams: #product-engineering
            - HR Data Catalog: [Link to catalog]
            - Snowflake Access Request: [Link to form]
            """)

        with st.expander("Streamlit Resources"):
            st.markdown("""
            - [Streamlit Documentation](https://docs.streamlit.io/)
            - [Streamlit in Snowflake](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
            - [Streamlit Community](https://discuss.streamlit.io/)
            """)

        # Version information
        st.caption("v2.0.0 | Created by Laurné Jones for demo purposes only")

    # Display the selected page
    pages[selection]()

def intro_page():
    st.markdown('<h1 class="main-header">People Insights Streamlit Showcase</h1>', unsafe_allow_html=True)

    # Introduction banner
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        # ✨ Welcome to the People Insights Streamlit Showcase!

        This interactive demo showcases what's possible with Streamlit for PI analytics applications.
        Explore different modules to discover capabilities that can be integrated into your own custom solutions.

        **This showcase demonstrates:**
        - Interactive HR dashboards and visualizations
        - Data collection and form processing
        - Integration with HR data sources
        - Deployment in Snowflake
        """)
    with col2:
        st.markdown("**[Image Placeholder]**")

    # What you can build section
    st.markdown('<h2 class="subheader">🚀 What You Can Build</h2>', unsafe_allow_html=True)

    solution_types = st.container()
    with solution_types:
        tab1, tab2, tab3, tab4 = st.tabs(["Dashboards", "Self-Service Tools", "Data Collection", "Predictive Analytics"])

        with tab1:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**[Image Placeholder]**")
            with col2:
                st.subheader("Interactive HR Dashboards")
                st.markdown("""
                - **Executive Dashboards**: High-level KPIs and trends
                - **HR Business Partner Dashboards**: Team-specific metrics
                - **Talent Acquisition Dashboards**: Recruiting pipeline and metrics
                - **Employee Experience Dashboards**: Engagement and satisfaction
                - **DEI Dashboards**: Diversity, equity, and inclusion metrics
                """)

        with tab2:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**[Image Placeholder]**")
            with col2:
                st.subheader("Self-Service HR Tools")
                st.markdown("""
                - **Compensation Calculators**: Salary planning and budgeting
                - **Headcount Planners**: Workforce planning scenarios
                - **Manager Analytics**: Team performance and engagement
                - **Talent Search**: Skills-based employee search
                - **Attrition Prediction**: Retention risk modeling
                """)

        with tab3:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**[Image Placeholder]**")
            with col2:
                st.subheader("HR Data Collection Applications")
                st.markdown("""
                - **Employee Surveys**: Engagement and pulse surveys
                - **Performance Reviews**: Multi-step review processes
                - **Onboarding Feedback**: New hire experience tracking
                - **Exit Interviews**: Standardized exit data collection
                - **Skills Assessments**: Competency tracking
                """)

        with tab4:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**[Image Placeholder]**")
            with col2:
                st.subheader("Predictive HR Analytics")
                st.markdown("""
                - **Attrition Prediction**: Machine learning for retention
                - **Talent Matching**: AI-powered role recommendations
                - **Performance Forecasting**: Trend analysis and predictions
                - **Hiring Optimization**: Recruitment funnel analysis
                - **Engagement Drivers**: Correlation and causation analysis
                """)

    # How to use this showcase
    st.markdown('<h2 class="subheader">📘 How to Use This Showcase</h2>', unsafe_allow_html=True)

    st.markdown("""
    This showcase demonstrates various PI analytics capabilities through interactive examples.
    Here's how to get the most out of it:

    1. **Explore the modules** in the sidebar to see different PI analytics capabilities
    2. **Interact with the examples** to understand how they work
    3. **View the code** behind each example to learn implementation details
    4. **Note features** you'd like to incorporate into your own custom solutions
    5. **Check the deployment guide** for instructions on implementing in Snowflake

    Each module demonstrates different aspects of what's possible with Streamlit for PI Analytics.
    """)

    # Use case highlights
    st.markdown('<h2 class="subheader">💡 PI Analytics Use Cases</h2>', unsafe_allow_html=True)

    use_cases = st.container()
    with use_cases:
        case1, case2, case3 = st.columns(3)

        with case1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("### Talent Acquisition Analytics")
            st.markdown("""
            - Visualize recruiting pipeline metrics
            - Track source effectiveness
            - Monitor time-to-fill and cost metrics
            - Analyze candidate diversity
            - Forecast hiring needs
            """)
            st.markdown('</div>', unsafe_allow_html=True)

        with case2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("### Employee Retention")
            st.markdown("""
            - Identify retention risk factors
            - Track attrition rates and trends
            - Analyze exit survey feedback
            - Model compensation impact
            - Create "what-if" retention scenarios
            """)
            st.markdown('</div>', unsafe_allow_html=True)

        with case3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown("### Workforce Analytics")
            st.markdown("""
            - Monitor team composition metrics
            - Analyze career progression
            - Track skill distribution
            - Visualize org structure
            - Plan future workforce needs
            """)
            st.markdown('</div>', unsafe_allow_html=True)

    # Implementation path
    st.markdown('<h2 class="subheader">🛣️ Implementation Path</h2>', unsafe_allow_html=True)

    # Create a horizontal steps indicator
    steps = st.columns(5)

    for i, (title, desc) in enumerate([
        ("Explore", "Browse this showcase to identify useful features"),
        ("Prototype", "Create a prototype with your HR data"),
        ("Deploy", "Set up in Snowflake environment"),
        ("Test", "Validate with stakeholders"),
        ("Scale", "Expand to more HR use cases")
    ]):
        with steps[i]:
            st.markdown(f"### {i+1}. {title}")
            st.markdown(desc)

    # Demo walkthrough steps
    progress_bar = st.progress(0)
    for i in range(100):
        # Update progress bar to simulate activity
        progress_bar.progress(i + 1)

    # Call to action
    st.success("""
    **Ready to explore more possibilities?** Navigate through the modules in the sidebar to see what Streamlit can do!

    For questions or custom solutions, contact the Product Engineering team.
    """)

if __name__ == "__main__":
    main()