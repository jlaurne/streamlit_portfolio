import streamlit as st
import pandas as pd
import numpy as np
import datetime

def hr_data_module():
    st.title("HR Data Fundamentals in Streamlit")
    
    # Module introduction with context
    st.markdown("""
    ## Making Magic Company: People Insights
    
    Understanding HR data structures, metrics, and visualization principles is essential for
    building effective HR analytics tools. This module covers the fundamentals of working 
    with HR data in Streamlit applications.
    """)
    
    # Generate sample HR data
    @st.cache_data
    def generate_sample_employee_data(size=200):
        """Generate a realistic employee dataset for HR analytics demonstrations"""
        np.random.seed(42)  # For reproducibility
        
        # Employee IDs (1000-1999)
        employee_ids = np.arange(1000, 1000+size)
        
        # Names (simplified for demo)
        first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Jamie', 'Avery', 
                       'Quinn', 'Skyler', 'Cameron', 'Reese', 'Parker', 'Hayden', 'Dakota']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 
                      'Davis', 'Rodriguez', 'Martinez', 'Lee', 'Nguyen', 'Patel', 'Kim', 'Singh']
        
        # Basic demographics
        genders = ['Male', 'Female', 'Non-Binary']
        gender_weights = [0.48, 0.48, 0.04]
        
        # Employment details
        departments = ['Engineering', 'Product', 'Marketing', 'Sales', 'Customer Support', 
                       'Finance', 'HR', 'Operations', 'Research', 'Legal']
        dept_weights = [0.25, 0.15, 0.1, 0.15, 0.1, 0.05, 0.05, 0.1, 0.03, 0.02]
        
        job_levels = ['Entry', 'Associate', 'Mid-Level', 'Senior', 'Manager', 'Director', 'VP', 'Executive']
        level_weights = [0.15, 0.2, 0.25, 0.2, 0.1, 0.05, 0.03, 0.02]
        
        locations = ['Orlando', 'New York', 'San Francisco', 'Chicago', 'Austin', 'Remote']
        location_weights = [0.3, 0.15, 0.2, 0.1, 0.05, 0.2]
        
        employment_status = ['Active', 'Terminated', 'On Leave']
        status_weights = [0.9, 0.08, 0.02]
        
        # Generate employee data
        today = datetime.datetime.now().date()
        
        data = {
            'employee_id': employee_ids,
            'first_name': np.random.choice(first_names, size=size),
            'last_name': np.random.choice(last_names, size=size),
            'gender': np.random.choice(genders, size=size, p=gender_weights),
            'department': np.random.choice(departments, size=size, p=dept_weights),
            'job_title': ['Title ' + str(np.random.randint(1, 100)) for _ in range(size)],  # Simplified
            'job_level': np.random.choice(job_levels, size=size, p=level_weights),
            'location': np.random.choice(locations, size=size, p=location_weights),
            'hire_date': [today - datetime.timedelta(days=np.random.randint(1, 365*10)) for _ in range(size)],
            'employment_status': np.random.choice(employment_status, size=size, p=status_weights),
            'salary': np.random.normal(80000, 30000, size=size).round(-3),
        }
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Calculate derived fields
        df['tenure_years'] = [(today - hire_date).days / 365 for hire_date in df['hire_date']]
        df['tenure_years'] = df['tenure_years'].round(1)
        
        # Add performance rating (last 3 years)
        ratings = ['Needs Improvement', 'Meets Expectations', 'Exceeds Expectations', 'Outstanding']
        rating_weights = [0.1, 0.5, 0.3, 0.1]
        
        for year in range(1, 4):
            df[f'performance_rating_{year}y_ago'] = np.random.choice(
                ratings, size=size, p=rating_weights
            )
        
        # Add engagement score (1-5 scale)
        df['engagement_score'] = np.random.uniform(1, 5, size=size).round(1)
        
        # Add diversity category (simplified for demonstration)
        diversity_categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
        df['diversity_category'] = np.random.choice(diversity_categories, size=size)
        
        return df
    
    # Generate sample HR data
    employee_df = generate_sample_employee_data()
    
    # Section 1: HR Data Structures
    st.header("1. Understanding HR Data Structures")
    
    # Use tabs for the learning components
    tab1, tab2, tab3 = st.tabs(["🔍 Live Example", "💻 Code", "📚 Explanation"])
    
    with tab1:
        st.subheader("Employee Data Structure")
        
        # Show schema/structure of the data
        st.markdown("### Employee Data Schema")
        
        # Create a more readable schema display
        schema_data = []
        for column in employee_df.columns:
            dtype = str(employee_df[column].dtype)
            sample = str(employee_df[column].iloc[0])
            if len(sample) > 50:
                sample = sample[:47] + "..."
            schema_data.append({"Column": column, "Data Type": dtype, "Sample Value": sample})
        
        schema_df = pd.DataFrame(schema_data)
        st.dataframe(schema_df, use_container_width=True)
        
        # Show sample data with privacy controls
        st.markdown("### Sample Employee Data (Anonymized)")
        
        # Add privacy toggle
        show_sensitive = st.toggle("Show Sensitive Fields", value=False)
        
        # Define sensitive fields
        sensitive_fields = ['first_name', 'last_name', 'salary', 'diversity_category']
        
        # Display appropriate columns based on toggle
        if show_sensitive:
            display_df = employee_df.head(10)
            st.warning("⚠️ In a real application, access to sensitive data should be restricted by role")
        else:
            display_df = employee_df.drop(columns=sensitive_fields).head(10)
            st.success("✅ Displaying only non-sensitive employee data")
        
        # Display the sample data
        st.dataframe(display_df, use_container_width=True)
        
        # Show HR data statistics
        st.markdown("### HR Data Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            active_count = employee_df[employee_df['employment_status'] == 'Active'].shape[0]
            st.metric("Active Employees", active_count)
        
        with col2:
            avg_tenure = employee_df['tenure_years'].mean()
            st.metric("Avg. Tenure (Years)", f"{avg_tenure:.1f}")
        
        with col3:
            departments_count = employee_df['department'].nunique()
            st.metric("Departments", departments_count)
    
    with tab2:
        # Store code snippet in a variable
        data_generation_code = """
# Generate sample HR data
@st.cache_data  # This caches the data to improve performance
def generate_sample_employee_data(size=200):
    \"\"\"Generate a realistic employee dataset for HR analytics demonstrations\"\"\"
    np.random.seed(42)  # For reproducibility
    
    # Employee IDs (1000-1999)
    employee_ids = np.arange(1000, 1000+size)
    
    # Names (simplified for demo)
    first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Jamie']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller']
    
    # Generate employee data
    today = datetime.datetime.now().date()
    
    data = {
        'employee_id': employee_ids,
        'first_name': np.random.choice(first_names, size=size),
        'last_name': np.random.choice(last_names, size=size),
        'department': np.random.choice(['Engineering', 'Product', 'Marketing', 'Sales'], size=size),
        'job_level': np.random.choice(['Entry', 'Associate', 'Mid-Level', 'Senior', 'Manager'], size=size),
        'location': np.random.choice(['Orlando', 'New York', 'San Francisco', 'Remote'], size=size),
        'hire_date': [today - datetime.timedelta(days=np.random.randint(1, 365*10)) for _ in range(size)],
        'employment_status': np.random.choice(['Active', 'Terminated', 'On Leave'], size=size),
        'salary': np.random.normal(80000, 30000, size=size).round(-3),
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Calculate derived fields
    df['tenure_years'] = [(today - hire_date).days / 365 for hire_date in df['hire_date']]
    df['tenure_years'] = df['tenure_years'].round(1)
    
    return df
"""
        
        privacy_code = """
# Display data with privacy controls
show_sensitive = st.toggle("Show Sensitive Fields", value=False)

# Define sensitive fields
sensitive_fields = ['first_name', 'last_name', 'salary', 'diversity_category']

# Display appropriate columns based on toggle
if show_sensitive:
    display_df = employee_df.head(10)
    st.warning("⚠️ In a real application, access to sensitive data should be restricted by role")
else:
    display_df = employee_df.drop(columns=sensitive_fields).head(10)
    st.success("✅ Displaying only non-sensitive employee data")

# Display the sample data
st.dataframe(display_df, use_container_width=True)
"""
        
        # Display code snippets
        st.code(data_generation_code)
        st.code(privacy_code)
    
    with tab3:
        st.subheader("HR Data Structure Best Practices")
        
        with st.expander("Core HR Data Entities", expanded=True):
            st.markdown("""
            **Key HR Data Entities at Making Magic Company:**
            
            1. **Employee Profile Data**
               - Demographic information
               - Employment details
               - Organizational placement
               
            2. **Compensation Data**
               - Salary information
               - Bonus and equity
               - Benefits enrollment
               
            3. **Performance Data**
               - Annual reviews
               - Competency assessments
               - Goals and OKRs
               
            4. **Talent Data**
               - Skills and certifications
               - Career aspirations
               - Succession planning
               
            Properly structuring these data entities ensures consistent reporting and analysis
            across different HR applications.
            """)
            
        with st.expander("HR Data Privacy Considerations"):
            st.markdown("""
            **Privacy Requirements for HR Data:**
            
            - **Data Minimization**: Only collect and display the data needed for specific analysis
            - **Access Controls**: Implement role-based access for sensitive HR information
            - **Aggregation**: Present aggregate data for small groups (n<5) to prevent identification
            - **Anonymization**: Remove direct identifiers when individual-level data is needed
            - **Data Retention**: Apply appropriate retention policies to HR data
            
            At Making Magic Company, we classify HR data into different sensitivity tiers:
            
            | Tier | Data Type | Access Level | Example |
            |------|-----------|--------------|---------|
            | 1 | Public | All employees | Headcount by department |
            | 2 | Internal | HR team & managers | Turnover rates |
            | 3 | Sensitive | HR specialists only | Individual compensation |
            | 4 | Restricted | Senior HR only | Protected class data |
            
            All Streamlit apps should be designed with these privacy tiers in mind.
            """)
    
    # Section 2: HR Metrics and KPIs (Simplified version without plotly)
    st.header("2. HR Metrics and KPIs")
    
    # Use tabs again for this section
    tab1, tab2, tab3 = st.tabs(["🔍 Live Example", "💻 Code", "📚 Explanation"])
    
    with tab1:
        st.subheader("Key HR Metrics Dashboard")
        
        # Create a selector for metric categories
        metric_category = st.selectbox(
            "Select HR Metric Category:",
            ["Workforce Demographics", "Talent Management", "Diversity & Inclusion"]
        )
        
        # Display metrics based on selection
        if metric_category == "Workforce Demographics":
            # Create a dashboard layout with metrics
            st.markdown("### Workforce Composition")
            
            # Create columns for metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Calculate headcount by status
                headcount = employee_df[employee_df['employment_status'] == 'Active'].shape[0]
                st.metric("Total Headcount", headcount)
            
            with col2:
                # Calculate average tenure
                avg_tenure = employee_df[employee_df['employment_status'] == 'Active']['tenure_years'].mean()
                st.metric("Average Tenure", f"{avg_tenure:.1f} years")
            
            with col3:
                # Calculate ratio of managers to individual contributors
                manager_count = employee_df[
                    (employee_df['job_level'].isin(['Manager', 'Director', 'VP', 'Executive'])) & 
                    (employee_df['employment_status'] == 'Active')
                ].shape[0]
                
                ic_count = employee_df[
                    (~employee_df['job_level'].isin(['Manager', 'Director', 'VP', 'Executive'])) & 
                    (employee_df['employment_status'] == 'Active')
                ].shape[0]
                
                span_of_control = ic_count / manager_count if manager_count > 0 else 0
                st.metric("Span of Control", f"{span_of_control:.1f}:1")
            
            # Visualize department distribution using native Streamlit charts
            st.markdown("### Headcount by Department")
            
            # Department distribution
            dept_counts = employee_df[employee_df['employment_status'] == 'Active'].groupby('department').size().reset_index(name='count')
            dept_counts = dept_counts.sort_values('count', ascending=False)
            
            # Display using Streamlit's native bar chart
            st.bar_chart(dept_counts.set_index('department'))
            
            # Visualize location distribution
            st.markdown("### Headcount by Location")
            
            # Location distribution
            loc_counts = employee_df[employee_df['employment_status'] == 'Active'].groupby('location').size().reset_index(name='count')
            loc_counts = loc_counts.sort_values('count', ascending=False)
            
            # Display using Streamlit's native bar chart
            st.bar_chart(loc_counts.set_index('location'))
            
        elif metric_category == "Talent Management":
            # Create columns for talent metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # Performance rating distribution
                st.markdown("### Performance Rating Distribution")
                
                performance_counts = employee_df[
                    employee_df['employment_status'] == 'Active'
                ]['performance_rating_1y_ago'].value_counts().reset_index()
                
                performance_counts.columns = ['Rating', 'Count']
                
                # Display using Streamlit's native bar chart
                st.bar_chart(performance_counts.set_index('Rating'))
            
            with col2:
                # Engagement score by department
                st.markdown("### Engagement Score by Department")
                
                engagement_by_dept = employee_df[
                    employee_df['employment_status'] == 'Active'
                ].groupby('department')['engagement_score'].mean().reset_index()
                
                engagement_by_dept = engagement_by_dept.sort_values('engagement_score', ascending=False)
                
                # Display using Streamlit's native bar chart
                st.bar_chart(engagement_by_dept.set_index('department'))
            
        elif metric_category == "Diversity & Inclusion":
            # Create columns for D&I metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # Gender distribution
                st.markdown("### Gender Distribution")
                
                gender_counts = employee_df[
                    employee_df['employment_status'] == 'Active'
                ]['gender'].value_counts().reset_index()
                
                gender_counts.columns = ['Gender', 'Count']
                
                # Display using Streamlit's native bar chart
                st.bar_chart(gender_counts.set_index('Gender'))
            
            with col2:
                # Diversity category distribution
                st.markdown("### Diversity Category Distribution")
                
                diversity_counts = employee_df[
                    employee_df['employment_status'] == 'Active'
                ]['diversity_category'].value_counts().reset_index()
                
                diversity_counts.columns = ['Category', 'Count']
                
                # Display using Streamlit's native bar chart
                st.bar_chart(diversity_counts.set_index('Category'))
    
    with tab2:
        # Store code snippet in a variable
        hr_metrics_code = """
# Create a selector for metric categories
metric_category = st.selectbox(
    "Select HR Metric Category:",
    ["Workforce Demographics", "Talent Management", "Diversity & Inclusion"]
)

# Display metrics based on selection
if metric_category == "Workforce Demographics":
    # Create a dashboard layout with metrics
    st.markdown("### Workforce Composition")
    
    # Create columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Calculate headcount by status
        headcount = employee_df[employee_df['employment_status'] == 'Active'].shape[0]
        st.metric("Total Headcount", headcount)
    
    with col2:
        # Calculate average tenure
        avg_tenure = employee_df[employee_df['employment_status'] == 'Active']['tenure_years'].mean()
        st.metric("Average Tenure", f"{avg_tenure:.1f} years")
    
    with col3:
        # Calculate ratio of managers to individual contributors
        manager_count = employee_df[
            (employee_df['job_level'].isin(['Manager', 'Director', 'VP', 'Executive'])) & 
            (employee_df['employment_status'] == 'Active')
        ].shape[0]
        
        ic_count = employee_df[
            (~employee_df['job_level'].isin(['Manager', 'Director', 'VP', 'Executive'])) & 
            (employee_df['employment_status'] == 'Active')
        ].shape[0]
        
        span_of_control = ic_count / manager_count if manager_count > 0 else 0
        st.metric("Span of Control", f"{span_of_control:.1f}:1")
    
    # Visualize department distribution
    st.markdown("### Headcount by Department")
    
    # Department distribution
    dept_counts = employee_df[employee_df['employment_status'] == 'Active'].groupby('department').size().reset_index(name='count')
    dept_counts = dept_counts.sort_values('count', ascending=False)
    
    # Display using Streamlit's native bar chart
    st.bar_chart(dept_counts.set_index('department'))
"""
        
        # Display code snippet
        st.code(hr_metrics_code)
    
    with tab3:
        st.subheader("HR Metrics Best Practices")
        
        with st.expander("Core HR Metrics at Making Magic", expanded=True):
            st.markdown("""
            **Essential HR Metrics by Category:**
            
            **1. Workforce Metrics**
            - Headcount (total, by department, by location)
            - Employee turnover rate (voluntary/involuntary)
            - Average tenure
            - Span of control (ICs per manager)
            
            **2. Talent Management Metrics**
            - Performance rating distribution
            - High potential percentage
            - Internal promotion rate
            - Time in role
            
            **3. Diversity & Inclusion Metrics**
            - Gender representation (overall and in leadership)
            - Diversity category distribution
            - Pay equity metrics
            - Inclusive culture indicators
            
            **4. Talent Acquisition Metrics**
            - Time to fill
            - Cost per hire
            - Source effectiveness
            - Diversity of candidate pipeline
            
            **5. Employee Experience Metrics**
            - Engagement score
            - eNPS (Employee Net Promoter Score)
            - Retention risk indicators
            - Learning program effectiveness
            
            When building Streamlit apps for HR analytics, focus on metrics that drive
            actionable insights for the specific use case.
            """)
    
    # Add Practice Challenge
    st.divider()
    st.header("🧩 Practice Challenge")
    
    challenge_description = """
    **Challenge**: Create a basic retention risk dashboard using HR data.
    
    Using the sample employee data, build a simple dashboard that:
    
    1. Shows the count of employees at retention risk
    2. Calculates the percentage of employees at risk by department
    3. Displays a visualization comparing risk across job levels
    
    Hint: You can simulate retention risk by considering employees with:
    - Below average engagement scores
    - High performers with no recent promotion
    - Specific tenure ranges that typically show higher turnover
    """
    
    st.info(challenge_description)
    
    # Provide a hint
    with st.expander("See Hint"):
        hint_code = """
# Create a function to calculate retention risk
def calculate_retention_risk(df):
    # Create a copy of the dataframe
    risk_df = df.copy()
    
    # Flag employees with below average engagement
    avg_engagement = risk_df['engagement_score'].mean()
    risk_df['low_engagement'] = risk_df['engagement_score'] < avg_engagement
    
    # Flag employees in the "risk zone" for tenure (e.g., 1-3 years)
    risk_df['tenure_risk'] = risk_df['tenure_years'].between(1, 3)
    
    # Flag high performers with no recent promotion
    risk_df['high_performer'] = risk_df['performance_rating_1y_ago'].isin(['Exceeds Expectations', 'Outstanding'])
    
    # Calculate overall risk (simple model)
    risk_df['at_risk'] = (
        (risk_df['low_engagement'] & risk_df['tenure_risk']) | 
        (risk_df['high_performer'] & risk_df['tenure_risk'])
    )
    
    return risk_df

# Apply the risk calculation
risk_data = calculate_retention_risk(employee_df)

# Display risk metrics
st.metric("Employees at Risk", risk_data[risk_data['at_risk']].shape[0])

# Calculate risk by department
dept_risk = risk_data.groupby('department')['at_risk'].mean() * 100
st.bar_chart(dept_risk)
"""
        st.code(hint_code)
    
    # Next steps
    st.divider()
    st.markdown("**Next Module**: [HR Data Visualization](placeholder)")