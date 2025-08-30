#hr_capstone_module.py
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def hr_capstone_module():
    st.title("HR Analytics Capstone: Building an Integrated Dashboard")
    
    # Module introduction with context
    st.markdown("""
    ## Making Magic Company: People Insights
    
    This capstone module brings together all the concepts you've learned to create a comprehensive 
    HR Analytics Dashboard. You'll build a complete talent acquisition and retention dashboard that 
    combines multiple components into a cohesive analytics solution.
    """)
    
    # Setup page configuration
    st.set_page_config = lambda **kwargs: None  # Prevent set_page_config error if already set
    
    # Load sample data
    @st.cache_data
    def load_sample_hr_data():
        # Generate employee data
        return generate_employee_data(), generate_recruitment_data(), generate_turnover_data()
    
    # Load data
    employee_df, recruitment_df, turnover_df = load_sample_hr_data()
    
    # Dashboard navigation
    st.sidebar.title("Dashboard Navigation")
    dashboard_section = st.sidebar.radio(
        "Select Section",
        ["Overview", "Talent Acquisition", "Employee Retention", "Diversity & Inclusion"]
    )
    
    # Dashboard filters in sidebar
    st.sidebar.title("Filters")
    
    # Department filter
    departments = sorted(employee_df['department'].unique())
    selected_departments = st.sidebar.multiselect(
        "Department",
        options=departments,
        default=departments
    )
    
    # Location filter
    locations = sorted(employee_df['location'].unique())
    selected_locations = st.sidebar.multiselect(
        "Location",
        options=locations,
        default=locations
    )
    
    # Date range filter for the dashboard
    current_year = datetime.datetime.now().year
    date_range = st.sidebar.slider(
        "Date Range",
        min_value=current_year-3,
        max_value=current_year,
        value=(current_year-1, current_year)
    )
    
    # Apply filters to dataframes
    filtered_employees = employee_df[
        (employee_df['department'].isin(selected_departments)) &
        (employee_df['location'].isin(selected_locations))
    ]
    
    filtered_recruitment = recruitment_df[
        (recruitment_df['department'].isin(selected_departments)) &
        (recruitment_df['location'].isin(selected_locations)) &
        (recruitment_df['year'] >= date_range[0]) &
        (recruitment_df['year'] <= date_range[1])
    ]
    
    filtered_turnover = turnover_df[
        (turnover_df['department'].isin(selected_departments)) &
        (turnover_df['location'].isin(selected_locations)) &
        (turnover_df['year'] >= date_range[0]) &
        (turnover_df['year'] <= date_range[1])
    ]
    
    # Dashboard sections
    if dashboard_section == "Overview":
        display_overview_dashboard(filtered_employees, filtered_recruitment, filtered_turnover)
    elif dashboard_section == "Talent Acquisition":
        display_talent_acquisition_dashboard(filtered_recruitment)
    elif dashboard_section == "Employee Retention":
        display_employee_retention_dashboard(filtered_employees, filtered_turnover)
    elif dashboard_section == "Diversity & Inclusion":
        display_diversity_dashboard(filtered_employees)
    
    # Add a divider
    st.divider()
    
    # Dashboard code explanation
    with st.expander("See Dashboard Code"):
        dashboard_code = """
# HR Analytics Dashboard Structure

# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data (using cached function)
@st.cache_data
def load_data():
    # In a real app, this would load from a database or file
    return employee_df, recruitment_df, turnover_df

# Dashboard navigation in sidebar
st.sidebar.title("Dashboard Navigation")
dashboard_section = st.sidebar.radio(
    "Select Section",
    ["Overview", "Talent Acquisition", "Employee Retention", "Diversity & Inclusion"]
)

# Global filters in sidebar
st.sidebar.title("Filters")

# Department filter
departments = sorted(employee_df['department'].unique())
selected_departments = st.sidebar.multiselect(
    "Department",
    options=departments,
    default=departments
)

# Location filter
locations = sorted(employee_df['location'].unique())
selected_locations = st.sidebar.multiselect(
    "Location",
    options=locations,
    default=locations
)

# Apply filters to dataframes
filtered_employees = employee_df[
    (employee_df['department'].isin(selected_departments)) &
    (employee_df['location'].isin(selected_locations))
]

# Display appropriate dashboard section based on navigation
if dashboard_section == "Overview":
    display_overview_dashboard(filtered_employees, filtered_recruitment, filtered_turnover)
elif dashboard_section == "Talent Acquisition":
    display_talent_acquisition_dashboard(filtered_recruitment)
# ... other dashboard sections

# Dashboard section implementation
def display_overview_dashboard(employees, recruitment, turnover):
    st.title("HR Analytics Overview")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Employees", f"{len(employees)}")
    
    with col2:
        st.metric("Avg. Tenure", f"{employees['tenure_years'].mean():.1f} years")
    
    # ... more metrics and visualizations
"""
        st.code(dashboard_code)
    
    # Add a message about integration
    st.markdown("""
    ### Learning Integration
    
    This capstone dashboard demonstrates how to integrate concepts from all previous modules:
    
    - **Data Fundamentals**: Data structures, metrics, and KPIs
    - **Visualizations**: Interactive charts and effective design
    - **Filters**: Connected filters that update all dashboard elements
    - **Forms**: Employee feedback integration
    - **Data Connections**: Simulated data pipeline
    
    Try exploring different sections and applying filters to see how all components work together!
    """)

# Dashboard section functions
def display_overview_dashboard(employees, recruitment, turnover):
    st.header("HR Analytics Overview")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        headcount = len(employees)
        st.metric(
            "Total Headcount", 
            f"{headcount:,}",
            delta=f"+{len(recruitment[recruitment['status'] == 'Hired']) - len(turnover)}"
        )
    
    with col2:
        avg_tenure = employees['tenure_years'].mean()
        st.metric(
            "Avg. Tenure", 
            f"{avg_tenure:.1f} years",
            delta=None
        )
    
    with col3:
        retention_rate = 100 - (len(turnover) / headcount * 100) if headcount > 0 else 0
        st.metric(
            "Retention Rate", 
            f"{retention_rate:.1f}%",
            delta=f"{retention_rate - 90:.1f}%" if retention_rate != 90 else None,
            delta_color="normal"
        )
    
    with col4:
        time_to_fill = recruitment[recruitment['status'] == 'Hired']['time_to_fill'].mean()
        st.metric(
            "Avg. Time to Fill", 
            f"{time_to_fill:.1f} days",
            delta=f"{time_to_fill - 45:.1f}" if time_to_fill != 45 else None,
            delta_color="inverse"  # Lower is better
        )
    
    # Create two column layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Headcount by Department")
        dept_counts = employees.groupby('department').size().reset_index(name='count')
        dept_counts = dept_counts.sort_values('count', ascending=False)
        
        fig = px.bar(
            dept_counts,
            x='department',
            y='count',
            color='count',
            color_continuous_scale='Blues',
            title='Employee Distribution by Department'
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Talent Pipeline Health")
        
        # Create a funnel chart for recruitment pipeline
        stages = ['Applied', 'Screened', 'Interviewed', 'Offered', 'Hired']
        stage_counts = []
        
        for stage in stages:
            stage_counts.append(len(recruitment[recruitment['stage'] == stage]))
        
        # Ensure the funnel makes sense (counts decrease at each stage)
        for i in range(len(stage_counts)-1, 0, -1):
            if stage_counts[i] > stage_counts[i-1]:
                stage_counts[i-1] = stage_counts[i]
        
        fig = go.Figure(go.Funnel(
            y=stages,
            x=stage_counts,
            textinfo="value+percent initial"
        ))
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Bottom row with time series data
    st.subheader("Employee Trends Over Time")
    
    # Combine recruitment and turnover data by month
    monthly_data = []
    
    # Get unique year-month combinations from both datasets
    recruitment_months = recruitment.groupby(['year', 'month']).size().reset_index()[['year', 'month']]
    turnover_months = turnover.groupby(['year', 'month']).size().reset_index()[['year', 'month']]
    
    all_months = pd.concat([recruitment_months, turnover_months]).drop_duplicates()
    all_months = all_months.sort_values(['year', 'month'])
    
    # Generate time series data
    for _, row in all_months.iterrows():
        year, month = row['year'], row['month']
        
        # Count hires and terminations for this month
        hires = len(recruitment[(recruitment['year'] == year) & 
                                (recruitment['month'] == month) & 
                                (recruitment['status'] == 'Hired')])
        
        terminations = len(turnover[(turnover['year'] == year) & 
                                    (turnover['month'] == month)])
        
        monthly_data.append({
            'year': year,
            'month': month,
            'date': f"{year}-{month:02d}",
            'hires': hires,
            'terminations': terminations,
            'net_change': hires - terminations
        })
    
    # Convert to DataFrame for plotting
    monthly_df = pd.DataFrame(monthly_data)
    
    # Create a dual-axis chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add hire and termination bars
    fig.add_trace(
        go.Bar(
            x=monthly_df['date'],
            y=monthly_df['hires'],
            name="Hires",
            marker_color='#76c893'
        )
    )
    
    fig.add_trace(
        go.Bar(
            x=monthly_df['date'],
            y=monthly_df['terminations'],
            name="Terminations",
            marker_color='#e07a5f'
        )
    )
    
    # Add net change line
    fig.add_trace(
        go.Scatter(
            x=monthly_df['date'],
            y=monthly_df['net_change'],
            name="Net Change",
            line=dict(color='#3a86ff', width=3),
            mode='lines+markers'
        ),
        secondary_y=True
    )
    
    fig.update_layout(
        title="Monthly Hires vs. Terminations",
        barmode='group',
        height=500
    )
    
    fig.update_yaxes(title_text="Count", secondary_y=False)
    fig.update_yaxes(title_text="Net Change", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)

def display_talent_acquisition_dashboard(recruitment):
    st.header("Talent Acquisition Dashboard")
    
    # Apply status filter
    status_filter = st.selectbox(
        "Application Status",
        options=["All Statuses", "Hired", "Rejected", "In Progress"]
    )
    
    if status_filter != "All Statuses":
        filtered_recruitment = recruitment[recruitment['status'] == status_filter]
    else:
        filtered_recruitment = recruitment
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_requisitions = filtered_recruitment['req_id'].nunique()
        st.metric(
            "Open Requisitions", 
            f"{total_requisitions:,}"
        )
    
    with col2:
        total_applicants = len(filtered_recruitment)
        st.metric(
            "Total Applicants", 
            f"{total_applicants:,}"
        )
    
    with col3:
        time_to_fill = filtered_recruitment[filtered_recruitment['status'] == 'Hired']['time_to_fill'].mean()
        st.metric(
            "Time to Fill", 
            f"{time_to_fill:.1f} days" if not pd.isna(time_to_fill) else "N/A"
        )
    
    with col4:
        cost_per_hire = filtered_recruitment[filtered_recruitment['status'] == 'Hired']['cost'].mean()
        st.metric(
            "Cost per Hire", 
            f"${cost_per_hire:,.0f}" if not pd.isna(cost_per_hire) else "N/A"
        )
    
    # Source analysis
    st.subheader("Recruiting Source Analysis")
    
    # Create two column layout
    col1, col2 = st.columns(2)
    
    with col1:
        # Applications by source
        source_counts = filtered_recruitment.groupby('source').size().reset_index(name='count')
        source_counts = source_counts.sort_values('count', ascending=False)
        
        fig = px.bar(
            source_counts,
            x='source',
            y='count',
            color='count',
            title='Applications by Source',
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Hiring success rate by source
        if len(filtered_recruitment[filtered_recruitment['status'] == 'Hired']) > 0:
            # Calculate hire rate by source
            source_totals = filtered_recruitment.groupby('source').size()
            source_hires = filtered_recruitment[filtered_recruitment['status'] == 'Hired'].groupby('source').size()
            
            # Merge into a DataFrame
            source_rates = pd.DataFrame({
                'Applications': source_totals,
                'Hires': source_hires
            }).fillna(0)
            
            # Calculate success rate
            source_rates['Success Rate'] = (source_rates['Hires'] / source_rates['Applications'] * 100).round(1)
            source_rates = source_rates.reset_index()
            source_rates = source_rates.sort_values('Success Rate', ascending=False)
            
            fig = px.bar(
                source_rates,
                x='source',
                y='Success Rate',
                color='Success Rate',
                title='Hiring Success Rate by Source (%)',
                color_continuous_scale='RdYlGn'
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hired candidates in the current selection to calculate success rates.")
    
    # Time to fill analysis
    st.subheader("Time to Fill Analysis")
    
    # Department breakdown of time to fill
    dept_time = filtered_recruitment[filtered_recruitment['status'] == 'Hired'].groupby('department')['time_to_fill'].mean().reset_index()
    dept_time = dept_time.sort_values('time_to_fill')
    
    if not dept_time.empty:
        fig = px.bar(
            dept_time,
            x='department',
            y='time_to_fill',
            color='time_to_fill',
            title='Average Time to Fill by Department (Days)',
            color_continuous_scale='RdYlGn_r'  # Reversed so green is lower (better)
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hired candidates in the current selection to analyze time to fill.")
    
    # Recruitment funnel
    st.subheader("Recruitment Funnel")
    
    # Group data by stage
    stages = ['Applied', 'Screened', 'Interviewed', 'Offered', 'Hired']
    stage_counts = []
    
    for stage in stages:
        stage_counts.append(len(filtered_recruitment[filtered_recruitment['stage'] == stage]))
    
    # Create stage conversion dataframe
    stage_df = pd.DataFrame({
        'Stage': stages,
        'Count': stage_counts
    })
    
    # Calculate conversion rates
    for i in range(1, len(stages)):
        if stage_counts[i-1] > 0:
            stage_df.loc[i, 'Conversion'] = stage_counts[i] / stage_counts[i-1] * 100
        else:
            stage_df.loc[i, 'Conversion'] = 0
    
    # First stage has no conversion rate
    stage_df.loc[0, 'Conversion'] = 100
    
    # Display as a funnel chart
    fig = go.Figure()
    
    # Add the funnel
    fig.add_trace(go.Funnel(
        y=stage_df['Stage'],
        x=stage_df['Count'],
        textinfo="value+percent initial",
        marker=dict(color=['#5fa8d3', '#62b6cb', '#1b4965', '#bee9e8', '#cae9ff'])
    ))
    
    fig.update_layout(
        title="Recruitment Funnel",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Conversion rate table
    st.subheader("Stage Conversion Rates")
    
    # Format conversion rates
    stage_df['Conversion'] = stage_df['Conversion'].round(1).astype(str) + '%'
    
    # Only show conversion rates for stages after Applied
    conversion_df = stage_df[1:].copy()
    conversion_df['Previous Stage'] = stages[:-1]
    conversion_df = conversion_df[['Previous Stage', 'Stage', 'Count', 'Conversion']]
    
    st.dataframe(conversion_df, use_container_width=True)

def display_employee_retention_dashboard(employees, turnover):
    st.header("Employee Retention Dashboard")
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        headcount = len(employees)
        st.metric(
            "Current Headcount", 
            f"{headcount:,}"
        )
    
    with col2:
        terminations = len(turnover)
        turnover_rate = terminations / (headcount + terminations) * 100 if (headcount + terminations) > 0 else 0
        st.metric(
            "Turnover Rate", 
            f"{turnover_rate:.1f}%",
            delta=f"{turnover_rate - 15:.1f}%" if turnover_rate != 15 else None,
            delta_color="inverse"  # Lower is better
        )
    
    with col3:
        avg_tenure = employees['tenure_years'].mean()
        st.metric(
            "Avg. Tenure", 
            f"{avg_tenure:.1f} years"
        )
    
    with col4:
        # Calculate tenure distribution
        under_1yr = len(employees[employees['tenure_years'] < 1])
        tenure_1yr_pct = under_1yr / headcount * 100 if headcount > 0 else 0
        st.metric(
            "New Hire Ratio", 
            f"{tenure_1yr_pct:.1f}%",
            help="Percentage of employees with less than 1 year tenure"
        )
    
    # Create two column layout for retention analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Turnover by Department")
        
        # Calculate turnover rate by department
        dept_headcount = employees.groupby('department').size().to_dict()
        dept_turnover = turnover.groupby('department').size().to_dict()
        
        # Create department turnover dataframe
        dept_data = []
        for dept in dept_headcount.keys():
            current = dept_headcount.get(dept, 0)
            terminated = dept_turnover.get(dept, 0)
            total = current + terminated
            rate = terminated / total * 100 if total > 0 else 0
            
            dept_data.append({
                'Department': dept,
                'Headcount': current,
                'Terminations': terminated,
                'Turnover Rate': rate
            })
        
        dept_df = pd.DataFrame(dept_data)
        dept_df = dept_df.sort_values('Turnover Rate', ascending=False)
        
        # Plot turnover rate by department
        fig = px.bar(
            dept_df,
            x='Department',
            y='Turnover Rate',
            color='Turnover Rate',
            title='Turnover Rate by Department (%)',
            color_continuous_scale='RdYlGn_r'  # Reversed so green is lower (better)
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Turnover by Tenure")
        
        # Create tenure bins
        bins = [0, 1, 2, 3, 5, 10, 100]
        labels = ['<1 year', '1-2 years', '2-3 years', '3-5 years', '5-10 years', '10+ years']
        
        # Bin the terminated employees by tenure
        turnover['tenure_bin'] = pd.cut(turnover['tenure_years'], bins=bins, labels=labels, right=False)
        tenure_turnover = turnover.groupby('tenure_bin').size().reindex(labels).fillna(0)
        
        # Plot turnover by tenure
        fig = px.bar(
            x=labels,
            y=tenure_turnover.values,
            title='Terminations by Tenure',
            labels={'x': 'Tenure', 'y': 'Terminations'},
            color=tenure_turnover.values,
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Turnover reasons analysis
    st.subheader("Turnover Reasons")
    
    # Get turnover reasons
    reason_counts = turnover.groupby('reason').size().reset_index(name='count')
    reason_counts = reason_counts.sort_values('count', ascending=False)
    
    # Plot turnover reasons
    fig = px.pie(
        reason_counts,
        values='count',
        names='reason',
        title='Termination Reasons',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk analysis
    st.subheader("Retention Risk Analysis")
    
    # Use mock risk scores from employee data
    if 'risk_score' in employees.columns:
        # Create risk bins
        risk_bins = [0, 25, 50, 75, 100]
        risk_labels = ['Low Risk (0-25)', 'Moderate Risk (25-50)', 'High Risk (50-75)', 'Very High Risk (75-100)']
        
        employees['risk_bin'] = pd.cut(employees['risk_score'], bins=risk_bins, labels=risk_labels, right=True)
        risk_counts = employees.groupby('risk_bin').size().reset_index(name='count')
        
        # Plot risk distribution
        fig = px.bar(
            risk_counts,
            x='risk_bin',
            y='count',
            color='risk_bin',
            title='Employee Retention Risk Distribution',
            color_discrete_sequence=['#76c893', '#52b69a', '#e9c46a', '#e76f51']
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Risk by department table
        st.subheader("Risk Analysis by Department")
        
        # Calculate average risk by department
        dept_risk = employees.groupby('department')['risk_score'].mean().reset_index()
        dept_risk = dept_risk.sort_values('risk_score', ascending=False)
        dept_risk.columns = ['Department', 'Average Risk Score']
        dept_risk['Average Risk Score'] = dept_risk['Average Risk Score'].round(1)
        
        # Add risk count
        high_risk = employees[employees['risk_score'] >= 75].groupby('department').size().reset_index(name='High Risk Count')
        dept_risk = dept_risk.merge(high_risk, left_on='Department', right_on='department', how='left')
        dept_risk = dept_risk.drop(columns=['department'])
        dept_risk['High Risk Count'] = dept_risk['High Risk Count'].fillna(0).astype(int)
        
        # Add total employees
        dept_counts = employees.groupby('department').size().reset_index(name='Total Employees')
        dept_risk = dept_risk.merge(dept_counts, left_on='Department', right_on='department', how='left')
        dept_risk = dept_risk.drop(columns=['department'])
        
        # Calculate high risk percentage
        dept_risk['High Risk %'] = (dept_risk['High Risk Count'] / dept_risk['Total Employees'] * 100).round(1)
        
        # Display table
        st.dataframe(dept_risk, use_container_width=True)

def display_diversity_dashboard(employees):
    st.header("Diversity & Inclusion Dashboard")
    
    # Key metrics
    st.subheader("Diversity Metrics")
    
    # Gender metrics
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender distribution
        gender_counts = employees.groupby('gender').size().reset_index(name='count')
        gender_pcts = employees.groupby('gender').size() / len(employees) * 100
        
        fig = px.pie(
            gender_counts,
            values='count',
            names='gender',
            title='Gender Distribution',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Ethnicity distribution
        ethnicity_counts = employees.groupby('ethnicity').size().reset_index(name='count')
        
        fig = px.pie(
            ethnicity_counts,
            values='count',
            names='ethnicity',
            title='Ethnicity Distribution',
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Diversity by level
    st.subheader("Diversity by Job Level")
    
    # Gender distribution by level
    gender_level = pd.crosstab(
        employees['job_level'], 
        employees['gender'], 
        normalize='index'
    ) * 100
    
    gender_level_long = gender_level.reset_index().melt(
        id_vars=['job_level'],
        var_name='Gender',
        value_name='Percentage'
    )
    
    # Define the job level order
    level_order = ['Entry', 'Associate', 'Mid-Level', 'Senior', 'Manager', 'Director', 'VP', 'Executive']
    gender_level_long['job_level'] = pd.Categorical(
        gender_level_long['job_level'], 
        categories=level_order, 
        ordered=True
    )
    
    gender_level_long = gender_level_long.sort_values('job_level')
    
    # Plot gender distribution by level
    fig = px.bar(
        gender_level_long,
        x='job_level',
        y='Percentage',
        color='Gender',
        title='Gender Distribution by Job Level',
        barmode='stack'
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Ethnicity by level
    ethnicity_level = pd.crosstab(
        employees['job_level'], 
        employees['ethnicity'], 
        normalize='index'
    ) * 100
    
    ethnicity_level_long = ethnicity_level.reset_index().melt(
        id_vars=['job_level'],
        var_name='Ethnicity',
        value_name='Percentage'
    )
    
    ethnicity_level_long['job_level'] = pd.Categorical(
        ethnicity_level_long['job_level'], 
        categories=level_order, 
        ordered=True
    )
    
    ethnicity_level_long = ethnicity_level_long.sort_values('job_level')
    
    # Plot ethnicity distribution by level
    fig = px.bar(
        ethnicity_level_long,
        x='job_level',
        y='Percentage',
        color='Ethnicity',
        title='Ethnicity Distribution by Job Level',
        barmode='stack'
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Pay equity analysis
    st.subheader("Pay Equity Analysis")
    
    # Gender pay analysis
    gender_pay = employees.groupby('gender')['salary'].agg(['mean', 'median', 'count']).reset_index()
    gender_pay.columns = ['Gender', 'Mean Salary', 'Median Salary', 'Count']
    
    # Calculate overall average
    overall_avg = employees['salary'].mean()
    
    # Format salaries
    gender_pay['Mean Salary'] = gender_pay['Mean Salary'].round(0).astype(int)
    gender_pay['Median Salary'] = gender_pay['Median Salary'].round(0).astype(int)
    
    # Calculate pay ratio to the highest paid gender
    max_salary = gender_pay['Mean Salary'].max()
    gender_pay['Pay Ratio'] = (gender_pay['Mean Salary'] / max_salary * 100).round(1).astype(str) + '%'
    
    # Reorder columns
    gender_pay = gender_pay[['Gender', 'Count', 'Mean Salary', 'Median Salary', 'Pay Ratio']]
    
    # Display table
    st.dataframe(gender_pay, use_container_width=True)
    
    # Plot salary distribution by gender
    col1, col2 = st.columns(2)
    
    with col1:
        # Box plot of salary by gender
        fig = px.box(
            employees,
            x='gender',
            y='salary',
            title='Salary Distribution by Gender',
            color='gender'
        )
        
        # Add a line for company average
        fig.add_shape(
            type="line",
            x0=-0.5,
            y0=overall_avg,
            x1=len(gender_pay)-0.5,
            y1=overall_avg,
            line=dict(color="red", width=2, dash="dash"),
        )
        
        fig.add_annotation(
            x=0,
            y=overall_avg,
            text="Company Average",
            showarrow=True,
            arrowhead=1,
            yshift=10
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Box plot of salary by ethnicity
        fig = px.box(
            employees,
            x='ethnicity',
            y='salary',
            title='Salary Distribution by Ethnicity',
            color='ethnicity'
        )
        
        # Add a line for company average
        fig.add_shape(
            type="line",
            x0=-0.5,
            y0=overall_avg,
            x1=len(employees['ethnicity'].unique())-0.5,
            y1=overall_avg,
            line=dict(color="red", width=2, dash="dash"),
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Inclusion metrics
    if 'inclusion_score' in employees.columns:
        st.subheader("Inclusion Metrics")
        
        # Calculate average inclusion score by demographic
        gender_inclusion = employees.groupby('gender')['inclusion_score'].mean().reset_index()
        gender_inclusion.columns = ['Gender', 'Inclusion Score']
        
        ethnicity_inclusion = employees.groupby('ethnicity')['inclusion_score'].mean().reset_index()
        ethnicity_inclusion.columns = ['Ethnicity', 'Inclusion Score']
        
        # Format scores
        gender_inclusion['Inclusion Score'] = gender_inclusion['Inclusion Score'].round(1)
        ethnicity_inclusion['Inclusion Score'] = ethnicity_inclusion['Inclusion Score'].round(1)
        
        # Display metrics side by side
        col1, col2 = st.columns(2)
        
        with col1:
            # Gender inclusion
            fig = px.bar(
                gender_inclusion,
                x='Gender',
                y='Inclusion Score',
                color='Inclusion Score',
                title='Inclusion Score by Gender',
                color_continuous_scale='Blues',
                range_y=[0, 10]
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Ethnicity inclusion
            fig = px.bar(
                ethnicity_inclusion,
                x='Ethnicity',
                y='Inclusion Score',
                color='Inclusion Score',
                title='Inclusion Score by Ethnicity',
                color_continuous_scale='Blues',
                range_y=[0, 10]
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

# Data generation functions
def generate_employee_data(size=300):
    np.random.seed(42)
    
    # Employee IDs
    employee_ids = np.arange(1001, 1001 + size)
    
    # Basic demographic information
    genders = ['Male', 'Female', 'Non-Binary']
    gender_weights = [0.48, 0.48, 0.04]
    
    ethnicities = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
    ethnicity_weights = [0.35, 0.25, 0.2, 0.15, 0.05]
    
    # Department distribution
    departments = ['Engineering', 'Product', 'Marketing', 'Sales', 'Customer Support', 
                  'Finance', 'HR', 'Operations', 'Research', 'Legal']
    dept_weights = [0.25, 0.15, 0.1, 0.15, 0.1, 0.05, 0.05, 0.1, 0.03, 0.02]
    
    # Job level distribution
    job_levels = ['Entry', 'Associate', 'Mid-Level', 'Senior', 'Manager', 'Director', 'VP', 'Executive']
    level_weights = [0.15, 0.2, 0.25, 0.2, 0.1, 0.05, 0.03, 0.02]
    
    # Location distribution
    locations = ['Orlando', 'New York', 'San Francisco', 'Chicago', 'Austin', 'Remote']
    location_weights = [0.3, 0.15, 0.2, 0.1, 0.05, 0.2]
    
    # Generate basic employee data
    current_year = datetime.datetime.now().year
    
    data = {
        'employee_id': employee_ids,
        'gender': np.random.choice(genders, size=size, p=gender_weights),
        'ethnicity': np.random.choice(ethnicities, size=size, p=ethnicity_weights),
        'department': np.random.choice(departments, size=size, p=dept_weights),
        'job_level': np.random.choice(job_levels, size=size, p=level_weights),
        'location': np.random.choice(locations, size=size, p=location_weights),
        'hire_year': np.random.randint(current_year-10, current_year+1, size=size),
        'hire_month': np.random.randint(1, 13, size=size)
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Calculate tenure
    current_month = datetime.datetime.now().month
    
    df['tenure_years'] = current_year - df['hire_year']
    month_diff = current_month - df['hire_month']
    df.loc[month_diff < 0, 'tenure_years'] = df.loc[month_diff < 0, 'tenure_years'] - 1
    df['tenure_years'] = df['tenure_years'] + (month_diff % 12) / 12
    df['tenure_years'] = df['tenure_years'].round(1)
    
    # Add salary information (based on job level and some random variation)
    base_salary = {
        'Entry': 50000,
        'Associate': 65000,
        'Mid-Level': 85000,
        'Senior': 110000,
        'Manager': 130000,
        'Director': 160000,
        'VP': 200000,
        'Executive': 250000
    }
    
    df['salary'] = df['job_level'].map(base_salary)
    # Add some variation (±20%)
    df['salary'] = df['salary'] * np.random.uniform(0.8, 1.2, size=size)
    # Round to nearest thousand
    df['salary'] = df['salary'].round(-3)
    
    # Add performance ratings
    performance_ratings = [1, 2, 3, 4, 5]
    performance_weights = [0.05, 0.15, 0.6, 0.15, 0.05]
    df['performance_rating'] = np.random.choice(performance_ratings, size=size, p=performance_weights)
    
    # Add retention risk score (0-100)
    df['risk_score'] = np.random.beta(2, 5, size=size) * 100
    df['risk_score'] = df['risk_score'].round(1)
    
    # Add inclusion score (1-10)
    df['inclusion_score'] = np.random.normal(7, 1.5, size=size)
    df['inclusion_score'] = df['inclusion_score'].clip(1, 10).round(1)
    
    return df

def generate_recruitment_data(size=500):
    np.random.seed(43)
    
    # Requisition IDs
    req_ids = [f"REQ-{i:04d}" for i in range(1, 101)]
    
    # Basic information
    departments = ['Engineering', 'Product', 'Marketing', 'Sales', 'Customer Support', 
                  'Finance', 'HR', 'Operations', 'Research', 'Legal']
    dept_weights = [0.25, 0.15, 0.1, 0.15, 0.1, 0.05, 0.05, 0.1, 0.03, 0.02]
    
    job_levels = ['Entry', 'Associate', 'Mid-Level', 'Senior', 'Manager', 'Director', 'VP', 'Executive']
    level_weights = [0.15, 0.2, 0.25, 0.2, 0.1, 0.05, 0.03, 0.02]
    
    locations = ['Orlando', 'New York', 'San Francisco', 'Chicago', 'Austin', 'Remote']
    location_weights = [0.3, 0.15, 0.2, 0.1, 0.05, 0.2]
    
    # Application sources
    sources = ['LinkedIn', 'Indeed', 'Company Website', 'Referral', 'Agency', 'Job Fair', 'Other']
    source_weights = [0.3, 0.2, 0.15, 0.2, 0.05, 0.05, 0.05]
    
    # Application stages
    stages = ['Applied', 'Screened', 'Interviewed', 'Offered', 'Hired']
    
    # Stage distribution (simulating a recruitment funnel)
    # For simplicity, we'll assign directly rather than simulating the full process
    stage_distribution = [0.5, 0.25, 0.15, 0.06, 0.04]  # Should sum to 1
    
    # Status distribution
    statuses = ['In Progress', 'Hired', 'Rejected']
    
    # Generate basic recruitment data
    current_year = datetime.datetime.now().year
    
    data = {
        'req_id': np.random.choice(req_ids, size=size),
        'department': np.random.choice(departments, size=size, p=dept_weights),
        'job_level': np.random.choice(job_levels, size=size, p=level_weights),
        'location': np.random.choice(locations, size=size, p=location_weights),
        'source': np.random.choice(sources, size=size, p=source_weights),
        'year': np.random.choice([current_year-1, current_year], size=size, p=[0.3, 0.7]),
        'month': np.random.randint(1, 13, size=size)
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Assign stages with cumulative distribution
    stage_cutoffs = np.cumsum(stage_distribution)
    random_values = np.random.random(size)
    
    df['stage'] = stages[0]  # Default to Applied
    
    for i in range(1, len(stages)):
        df.loc[random_values < stage_cutoffs[i], 'stage'] = stages[i]
    
    # Assign status based on stage
    df['status'] = 'In Progress'
    df.loc[df['stage'] == 'Hired', 'status'] = 'Hired'
    
    # Some rejected at each stage
    for stage in stages[:-1]:  # All stages except Hired
        stage_mask = df['stage'] == stage
        reject_mask = np.random.random(size) < 0.2  # 20% rejection rate
        df.loc[stage_mask & reject_mask, 'status'] = 'Rejected'
    
    # Add time to fill (only for Hired)
    time_to_fill = {
        'Entry': np.random.normal(30, 10, size),
        'Associate': np.random.normal(35, 10, size),
        'Mid-Level': np.random.normal(45, 15, size),
        'Senior': np.random.normal(60, 20, size),
        'Manager': np.random.normal(75, 20, size),
        'Director': np.random.normal(90, 25, size),
        'VP': np.random.normal(120, 30, size),
        'Executive': np.random.normal(150, 40, size)
    }
    
    for level, times in time_to_fill.items():
        df.loc[(df['job_level'] == level) & (df['status'] == 'Hired'), 'time_to_fill'] = times[(df['job_level'] == level) & (df['status'] == 'Hired')].round()
    
    # Cap at minimum of 7 days
    df.loc[df['time_to_fill'] < 7, 'time_to_fill'] = 7
    
    # Add cost per hire (only for Hired)
    base_cost = {
        'Entry': 3000,
        'Associate': 4000,
        'Mid-Level': 6000,
        'Senior': 8000,
        'Manager': 12000,
        'Director': 20000,
        'VP': 30000,
        'Executive': 50000
    }
    
    # Source factors (multiplier on base cost)
    source_factor = {
        'LinkedIn': 1.2,
        'Indeed': 1.0,
        'Company Website': 0.7,
        'Referral': 0.5,
        'Agency': 2.5,
        'Job Fair': 1.5,
        'Other': 1.0
    }
    
    # Calculate cost
    df['cost'] = 0
    
    for level, cost in base_cost.items():
        for source, factor in source_factor.items():
            mask = (df['job_level'] == level) & (df['source'] == source) & (df['status'] == 'Hired')
            df.loc[mask, 'cost'] = cost * factor * np.random.uniform(0.8, 1.2, sum(mask))
    
    # Round cost to nearest 100
    df.loc[df['cost'] > 0, 'cost'] = df.loc[df['cost'] > 0, 'cost'].round(-2)
    
    return df

def generate_turnover_data(size=50):
    np.random.seed(44)
    
    # Basic information
    departments = ['Engineering', 'Product', 'Marketing', 'Sales', 'Customer Support', 
                  'Finance', 'HR', 'Operations', 'Research', 'Legal']
    dept_weights = [0.25, 0.15, 0.1, 0.15, 0.1, 0.05, 0.05, 0.1, 0.03, 0.02]
    
    job_levels = ['Entry', 'Associate', 'Mid-Level', 'Senior', 'Manager', 'Director', 'VP', 'Executive']
    level_weights = [0.2, 0.25, 0.25, 0.15, 0.08, 0.04, 0.02, 0.01]
    
    locations = ['Orlando', 'New York', 'San Francisco', 'Chicago', 'Austin', 'Remote']
    location_weights = [0.3, 0.15, 0.2, 0.1, 0.05, 0.2]
    
    # Termination reasons
    reasons = ['Voluntary - Better Opportunity', 'Voluntary - Relocation', 'Voluntary - Personal', 
               'Voluntary - Retirement', 'Involuntary - Performance', 'Involuntary - Restructuring',
               'Involuntary - Policy Violation']
    reason_weights = [0.4, 0.1, 0.15, 0.05, 0.15, 0.1, 0.05]
    
    # Generate basic turnover data
    current_year = datetime.datetime.now().year
    
    data = {
        'department': np.random.choice(departments, size=size, p=dept_weights),
        'job_level': np.random.choice(job_levels, size=size, p=level_weights),
        'location': np.random.choice(locations, size=size, p=location_weights),
        'reason': np.random.choice(reasons, size=size, p=reason_weights),
        'year': np.random.choice([current_year-1, current_year], size=size, p=[0.3, 0.7]),
        'month': np.random.randint(1, 13, size=size)
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add tenure at termination
    tenure_means = {
        'Entry': 1.5,
        'Associate': 2.0,
        'Mid-Level': 3.0,
        'Senior': 4.0,
        'Manager': 5.0,
        'Director': 6.0,
        'VP': 4.0,
        'Executive': 3.0
    }
    
    # Generate tenure based on job level
    df['tenure_years'] = 0
    
    for level, mean in tenure_means.items():
        level_mask = df['job_level'] == level
        df.loc[level_mask, 'tenure_years'] = np.random.exponential(mean, size=sum(level_mask))
    
    # Cap at reasonable values and round
    df['tenure_years'] = df['tenure_years'].clip(0.1, 15).round(1)
    
    return df