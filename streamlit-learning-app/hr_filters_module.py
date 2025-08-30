import streamlit as st
import pandas as pd
import numpy as np
import datetime

def hr_filters_module():
    st.title("Interactive HR Filters in Streamlit")
    
    # Module introduction with context
    st.markdown("""
    ## Making Magic Company: People Insights
    
    Filters transform static HR reports into interactive tools for business partners and leadership.
    In this module, you'll learn how to create and connect filters to your HR visualizations.
    """)
    
    # Generate sample HR data
    @st.cache_data
    def generate_sample_hr_data():
        np.random.seed(42)
        
        # Date range for the last 2 years
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=730)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Create employee IDs (1000-1999)
        employee_ids = np.arange(1000, 1200)
        
        # Create records with randomly selected employees and dates
        num_records = 1000
        selected_ids = np.random.choice(employee_ids, size=num_records)
        selected_dates = np.random.choice(dates, size=num_records)
        
        # Department distribution
        departments = ['Engineering', 'Product', 'Marketing', 'Sales', 'Customer Support', 
                       'Finance', 'HR', 'Operations', 'Research', 'Legal']
        dept_weights = [0.25, 0.15, 0.1, 0.15, 0.1, 0.05, 0.05, 0.1, 0.03, 0.02]
        
        # Location distribution
        locations = ['Orlando', 'New York', 'San Francisco', 'Chicago', 'Austin', 'Remote']
        location_weights = [0.3, 0.15, 0.2, 0.1, 0.05, 0.2]
        
        # Job level distribution
        job_levels = ['Entry', 'Associate', 'Mid-Level', 'Senior', 'Manager', 'Director', 'VP', 'Executive']
        level_weights = [0.15, 0.2, 0.25, 0.2, 0.1, 0.05, 0.03, 0.02]
        
        # Performance ratings
        performance_ratings = ['Needs Improvement', 'Meets Expectations', 'Exceeds Expectations', 'Outstanding']
        rating_weights = [0.1, 0.5, 0.3, 0.1]
        
        # Generate random data
        data = {
            'employee_id': selected_ids,
            'date': selected_dates,
            'department': np.random.choice(departments, size=num_records, p=dept_weights),
            'location': np.random.choice(locations, size=num_records, p=location_weights),
            'job_level': np.random.choice(job_levels, size=num_records, p=level_weights),
            'tenure_years': np.random.uniform(0, 10, size=num_records).round(1),
            'performance_rating': np.random.choice(performance_ratings, size=num_records, p=rating_weights),
            'engagement_score': np.random.uniform(1, 5, size=num_records).round(1),
            'salary': np.random.normal(80000, 30000, size=num_records).round(-3),
            'bonus_percent': np.random.uniform(0, 0.3, size=num_records).round(2),
        }
        
        df = pd.DataFrame(data)
        
        # Add hiring source for TA analysis
        hiring_sources = ['Internal Referral', 'LinkedIn', 'Job Board', 'University', 'Recruiter', 'Career Fair', 'Website']
        source_weights = [0.3, 0.25, 0.15, 0.1, 0.1, 0.05, 0.05]
        df['hiring_source'] = np.random.choice(hiring_sources, size=num_records, p=source_weights)
        
        # Add time to fill (days) - normal distribution around 45 days
        df['time_to_fill'] = np.random.normal(45, 15, size=num_records).round(0).astype(int)
        df.loc[df['time_to_fill'] < 10, 'time_to_fill'] = 10  # Minimum 10 days
        
        # Add cost per hire - varies by level
        base_cost = 5000
        level_multipliers = {
            'Entry': 0.5,
            'Associate': 0.7,
            'Mid-Level': 1.0,
            'Senior': 1.5,
            'Manager': 2.0,
            'Director': 3.0,
            'VP': 5.0,
            'Executive': 10.0
        }
        
        df['cost_per_hire'] = df['job_level'].apply(lambda x: base_cost * level_multipliers[x] * np.random.uniform(0.8, 1.2))
        df['cost_per_hire'] = df['cost_per_hire'].round(-2)
        
        # Add diversity data (for demonstration purposes only - simplified)
        diversity_categories = ['Category A', 'Category B', 'Category C', 'Category D', 'Category E']
        df['diversity_category'] = np.random.choice(diversity_categories, size=num_records)
        
        return df
    
    hr_df = generate_sample_hr_data()
    
    # Section 1: Simple Department Filter
    st.header("1. Basic HR Data Filtering")
    
    # Use tabs for the learning components
    tab1, tab2, tab3 = st.tabs(["🔍 Live Example", "💻 Code", "📚 Explanation"])
    
    with tab1:
        st.subheader("Department Filter for HR Metrics")
        
        # Simple selectbox filter
        selected_dept = st.selectbox(
            "Select a department to analyze:",
            options=['All Departments'] + sorted(hr_df['department'].unique().tolist())
        )
        
        # Apply filter
        if selected_dept != 'All Departments':
            filtered_df = hr_df[hr_df['department'] == selected_dept]
            st.success(f"Showing HR data for {selected_dept} department only")
        else:
            filtered_df = hr_df
            st.info("Showing HR data for all departments")
        
        # Display filtered data with more privacy-focused approach
        st.write("Sample of employee records (anonymized):")
        display_df = filtered_df[['department', 'job_level', 'location', 'tenure_years', 'performance_rating']].head(10)
        st.dataframe(display_df, use_container_width=True)
        
        # Show simple HR metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_tenure = filtered_df['tenure_years'].mean()
            st.metric(
                label="Avg. Tenure (Years)", 
                value=f"{avg_tenure:.1f}",
                delta=f"{avg_tenure - hr_df['tenure_years'].mean():.1f} vs company avg"
            )
        
        with col2:
            avg_engagement = filtered_df['engagement_score'].mean()
            st.metric(
                label="Avg. Engagement Score", 
                value=f"{avg_engagement:.1f}/5.0",
                delta=f"{avg_engagement - hr_df['engagement_score'].mean():.1f} vs company avg"
            )
        
        with col3:
            high_performers = filtered_df[filtered_df['performance_rating'].isin(['Exceeds Expectations', 'Outstanding'])].shape[0]
            high_performer_pct = high_performers / filtered_df.shape[0] * 100
            company_high_pct = hr_df[hr_df['performance_rating'].isin(['Exceeds Expectations', 'Outstanding'])].shape[0] / hr_df.shape[0] * 100
            st.metric(
                label="High Performers", 
                value=f"{high_performer_pct:.1f}%",
                delta=f"{high_performer_pct - company_high_pct:.1f}% vs company avg"
            )
    
    with tab2:
        st.code("""
# Simple department filter
selected_dept = st.selectbox(
    "Select a department to analyze:",
    options=['All Departments'] + sorted(hr_df['department'].unique().tolist())
)

# Apply filter
if selected_dept != 'All Departments':
    filtered_df = hr_df[hr_df['department'] == selected_dept]
    st.success(f"Showing HR data for {selected_dept} department only")
else:
    filtered_df = hr_df
    st.info("Showing HR data for all departments")

# Display filtered data with more privacy-focused approach
st.write("Sample of employee records (anonymized):")
display_df = filtered_df[['department', 'job_level', 'location', 'tenure_years', 'performance_rating']].head(10)
st.dataframe(display_df, use_container_width=True)

# Show simple HR metrics
col1, col2, col3 = st.columns(3)

with col1:
    avg_tenure = filtered_df['tenure_years'].mean()
    st.metric(
        label="Avg. Tenure (Years)", 
        value=f"{avg_tenure:.1f}",
        delta=f"{avg_tenure - hr_df['tenure_years'].mean():.1f} vs company avg"
    )
""")
    
    with tab3:
        st.subheader("HR Data Filtering Best Practices")
        
        with st.expander("HR Data Filtering Strategy", expanded=True):
            st.markdown("""
            **Key HR Filtering Components:**
            1. **Department/Team Filter**: Essential for org-specific analysis
            2. **Location Filter**: Critical for geographical insights
            3. **Job Level Filter**: Enables career progression analysis
            4. **Date Range Filter**: For trend analysis over time
            
            **Why Filter HR Data?**
            Filtering allows People Insights teams to deliver targeted analysis to business partners
            and leadership, facilitating data-driven decisions about specific teams or employee groups.
            """)
            
        with st.expander("HR Data Privacy Considerations"):
            st.markdown("""
            When building HR analytics apps, always consider:
            
            - **Data Minimization**: Only show what's necessary for the analysis
            - **Aggregation**: Use summaries for small groups to prevent identification
            - **Anonymization**: Remove direct identifiers when showing individual records
            - **Access Control**: Build in permissions using Streamlit's authentication options
            
            ⚠️ **At Making Magic Company**: Always consult our data privacy guidelines when
            building HR analytics applications.
            """)
    
    # Add a divider between sections
    st.divider()
    
    # Section 2: Talent Acquisition Dashboard with Multiple Filters
    st.header("2. Talent Acquisition Dashboard")
    
    # Use tabs again for this section
    tab1, tab2, tab3 = st.tabs(["🔍 Live Example", "💻 Code", "📚 Explanation"])
    
    with tab1:
        st.subheader("Talent Acquisition Performance Dashboard")
        
        # Create a container for TA filters with a subtle background
        with st.container():
            st.markdown("### Recruitment Filters")
            
            # Create 2 columns for filters
            col1, col2 = st.columns(2)
            
            with col1:
                # Department filter
                ta_departments = st.multiselect(
                    "Select Departments:",
                    options=sorted(hr_df['department'].unique().tolist()),
                    default=sorted(hr_df['department'].unique().tolist())
                )
                
                # Job level filter
                ta_job_levels = st.multiselect(
                    "Select Job Levels:",
                    options=sorted(hr_df['job_level'].unique().tolist()),
                    default=sorted(hr_df['job_level'].unique().tolist())
                )
            
            with col2:
                # Hiring source filter
                ta_sources = st.multiselect(
                    "Select Hiring Sources:",
                    options=sorted(hr_df['hiring_source'].unique().tolist()),
                    default=sorted(hr_df['hiring_source'].unique().tolist())
                )
                
                # Date range filter
                ta_date_range = st.date_input(
                    "Select Date Range:",
                    value=(hr_df['date'].min(), hr_df['date'].max()),
                    min_value=hr_df['date'].min(),
                    max_value=hr_df['date'].max()
                )
        
        # Apply multiple filters for TA dashboard
        ta_filtered_df = hr_df.copy()
        
        # Apply each filter if selected options exist
        if ta_departments:
            ta_filtered_df = ta_filtered_df[ta_filtered_df['department'].isin(ta_departments)]
        
        if ta_job_levels:
            ta_filtered_df = ta_filtered_df[ta_filtered_df['job_level'].isin(ta_job_levels)]
            
        if ta_sources:
            ta_filtered_df = ta_filtered_df[ta_filtered_df['hiring_source'].isin(ta_sources)]
        
        if len(ta_date_range) == 2:
            start_date, end_date = ta_date_range
            ta_filtered_df = ta_filtered_df[
                (ta_filtered_df['date'] >= pd.Timestamp(start_date)) & 
                (ta_filtered_df['date'] <= pd.Timestamp(end_date))
            ]
        
        # Display TA metrics in 3 columns
        st.markdown("### Talent Acquisition Metrics")
        metric1, metric2, metric3 = st.columns(3)
        
        with metric1:
            avg_time_to_fill = ta_filtered_df['time_to_fill'].mean()
            company_avg_ttf = hr_df['time_to_fill'].mean()
            delta_pct = ((avg_time_to_fill - company_avg_ttf) / company_avg_ttf) * 100
            st.metric(
                "Avg. Time to Fill (Days)", 
                f"{avg_time_to_fill:.1f}",
                delta=f"{delta_pct:.1f}%",
                delta_color="inverse"  # Lower is better for time to fill
            )
        
        with metric2:
            avg_cost = ta_filtered_df['cost_per_hire'].mean()
            company_avg_cost = hr_df['cost_per_hire'].mean()
            delta_cost_pct = ((avg_cost - company_avg_cost) / company_avg_cost) * 100
            st.metric(
                "Avg. Cost per Hire", 
                f"${avg_cost:,.0f}",
                delta=f"{delta_cost_pct:.1f}%",
                delta_color="inverse"  # Lower is better for cost
            )
        
        with metric3:
            hire_count = ta_filtered_df.shape[0]
            st.metric(
                "Total Hires", 
                f"{hire_count}",
            )
        
        # Create charts based on filtered data
        st.markdown("### Hiring Trends")
        
        # Hires by month chart
        ta_filtered_df['month'] = ta_filtered_df['date'].dt.to_period('M')
        hires_by_month = ta_filtered_df.groupby('month').size().reset_index(name='hires')
        hires_by_month['month'] = hires_by_month['month'].astype(str)
        
        # Convert to format suitable for st.line_chart
        hires_by_month_chart = pd.DataFrame({
            'Hires': hires_by_month['hires'].values
        }, index=hires_by_month['month'])
        
        st.line_chart(hires_by_month_chart)
        
        # TA breakdown charts
        st.markdown("### Hiring Source Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Hires by Source")
            hires_by_source = ta_filtered_df.groupby('hiring_source').size().reset_index(name='count')
            hires_by_source = hires_by_source.sort_values('count', ascending=False)
            
            # Convert to format suitable for st.bar_chart
            source_chart = pd.DataFrame({
                'Hires': hires_by_source['count'].values
            }, index=hires_by_source['hiring_source'])
            
            st.bar_chart(source_chart)
        
        with col2:
            st.subheader("Cost Efficiency by Source")
            cost_by_source = ta_filtered_df.groupby('hiring_source')['cost_per_hire'].mean().reset_index()
            cost_by_source = cost_by_source.sort_values('cost_per_hire')
            
            # Convert to format suitable for st.bar_chart
            cost_chart = pd.DataFrame({
                'Avg Cost': cost_by_source['cost_per_hire'].values
            }, index=cost_by_source['hiring_source'])
            
            st.bar_chart(cost_chart)
            
        # Diversity metrics
        st.markdown("### Diversity in Hiring")
        diversity_counts = ta_filtered_df.groupby('diversity_category').size().reset_index(name='count')
        diversity_pcts = diversity_counts.copy()
        diversity_pcts['percentage'] = diversity_pcts['count'] / diversity_pcts['count'].sum() * 100
        
        # Convert to format suitable for st.bar_chart
        diversity_chart = pd.DataFrame({
            'Percentage': diversity_pcts['percentage'].values
        }, index=diversity_pcts['diversity_category'])
        
        st.bar_chart(diversity_chart)
        
        # Job level distribution
        st.markdown("### Job Level Distribution")
        level_counts = ta_filtered_df.groupby('job_level').size().reset_index(name='count')
        
        # Order job levels logically
        level_order = ['Entry', 'Associate', 'Mid-Level', 'Senior', 'Manager', 'Director', 'VP', 'Executive']
        level_counts['job_level'] = pd.Categorical(level_counts['job_level'], categories=level_order, ordered=True)
        level_counts = level_counts.sort_values('job_level')
        
        # Convert to format suitable for st.bar_chart
        level_chart = pd.DataFrame({
            'Hires': level_counts['count'].values
        }, index=level_counts['job_level'])
        
        st.bar_chart(level_chart)
    
    with tab2:
        st.code("""
# Create a container for TA filters
with st.container():
    st.markdown("### Recruitment Filters")
    
    # Create 2 columns for filters
    col1, col2 = st.columns(2)
    
    with col1:
        # Department filter
        ta_departments = st.multiselect(
            "Select Departments:",
            options=sorted(hr_df['department'].unique().tolist()),
            default=sorted(hr_df['department'].unique().tolist())
        )
        
        # Job level filter
        ta_job_levels = st.multiselect(
            "Select Job Levels:",
            options=sorted(hr_df['job_level'].unique().tolist()),
            default=sorted(hr_df['job_level'].unique().tolist())
        )
    
    with col2:
        # Hiring source filter
        ta_sources = st.multiselect(
            "Select Hiring Sources:",
            options=sorted(hr_df['hiring_source'].unique().tolist()),
            default=sorted(hr_df['hiring_source'].unique().tolist())
        )
        
        # Date range filter
        ta_date_range = st.date_input(
            "Select Date Range:",
            value=(hr_df['date'].min(), hr_df['date'].max()),
            min_value=hr_df['date'].min(),
            max_value=hr_df['date'].max()
        )

# Apply multiple filters for TA dashboard
ta_filtered_df = hr_df.copy()

# Apply each filter if selected options exist
if ta_departments:
    ta_filtered_df = ta_filtered_df[ta_filtered_df['department'].isin(ta_departments)]

if ta_job_levels:
    ta_filtered_df = ta_filtered_df[ta_filtered_df['job_level'].isin(ta_job_levels)]
    
if ta_sources:
    ta_filtered_df = ta_filtered_df[ta_filtered_df['hiring_source'].isin(ta_sources)]

if len(ta_date_range) == 2:
    start_date, end_date = ta_date_range
    ta_filtered_df = ta_filtered_df[
        (ta_filtered_df['date'] >= pd.Timestamp(start_date)) & 
        (ta_filtered_df['date'] <= pd.Timestamp(end_date))
    ]

# Display TA metrics
st.markdown("### Talent Acquisition Metrics")
metric1, metric2, metric3 = st.columns(3)

with metric1:
    avg_time_to_fill = ta_filtered_df['time_to_fill'].mean()
    company_avg_ttf = hr_df['time_to_fill'].mean()
    delta_pct = ((avg_time_to_fill - company_avg_ttf) / company_avg_ttf) * 100
    st.metric(
        "Avg. Time to Fill (Days)", 
        f"{avg_time_to_fill:.1f}",
        delta=f"{delta_pct:.1f}%",
        delta_color="inverse"  # Lower is better for time to fill
    )
""")
    
    with tab3:
        st.subheader("Building Talent Acquisition Dashboards")
        
        with st.expander("TA Dashboard Design Pattern", expanded=True):
            st.markdown("""
            **The TA Dashboard Design Pattern for Making Magic Company:**
            
            1. **Top-level filters**: Department, job level, source, and date range
            2. **Key metrics panel**: Time to fill, cost per hire, total hires
            3. **Trend analysis**: Monthly hiring volume
            4. **Source effectiveness**: Comparing channels by volume and cost
            5. **Diversity insights**: Distribution across diversity categories
            
            This pattern allows talent acquisition teams and hiring managers to analyze
            recruiting performance and make data-driven decisions about sourcing strategy.
            """)
        
        with st.expander("Key TA Metrics to Track"):
            st.markdown("""
            **Critical Talent Acquisition Metrics:**
            
            - **Time to Fill**: Average days from job opening to accepted offer
            - **Cost per Hire**: Total recruiting costs divided by number of hires
            - **Source Effectiveness**: Comparing channels by volume, quality, and cost
            - **Diversity Metrics**: Distribution across demographic categories
            - **Offer Acceptance Rate**: Percentage of offers accepted
            - **Quality of Hire**: Performance ratings of new hires
            
            These metrics help the People Insights team demonstrate TA effectiveness
            and identify opportunities for improvement.
            """)
            
        with st.expander("Customizing for Stakeholders"):
            st.markdown("""
            **Tailoring TA Dashboards for Different Audiences:**
            
            - **Hiring Managers**: Focus on their specific requisitions and candidates
            - **TA Leadership**: Emphasize overall efficiency metrics and trends
            - **Finance**: Highlight cost metrics and budget utilization
            - **Diversity & Inclusion**: Center diversity metrics and inclusion indicators
            - **Executive Leadership**: Provide high-level summary with strategic insights
            
            In Streamlit, you can use `st.session_state` to remember user preferences
            and personalize the dashboard for different stakeholder groups.
            """)
    
    # Add interactive challenge at the end
    st.divider()
    st.header("🧩 Practice Challenge")
    
    st.info("""
    **Challenge**: Create a Time-to-Fill Filter for the TA Dashboard!
    
    Try adding a slider that allows filtering the data to only show hires
    with specific time-to-fill ranges. This will help identify which roles
    or departments have recruiting processes that need optimization.
    """)
    
    with st.expander("See Hint"):
        st.code("""
# Add a time-to-fill range slider
min_ttf, max_ttf = st.slider(
    "Time to Fill Range (days):",
    min_value=int(hr_df['time_to_fill'].min()),
    max_value=int(hr_df['time_to_fill'].max()),
    value=(int(hr_df['time_to_fill'].min()), int(hr_df['time_to_fill'].max()))
)

# Apply the filter to your dataframe
filtered_df = hr_df[hr_df['time_to_fill'].between(min_ttf, max_ttf)]

# Calculate the percentage of hires that fall in this range
pct_in_range = len(filtered_df) / len(hr_df) * 100
st.write(f"{pct_in_range:.1f}% of hires were completed within this time range")
""")
        
    # Actually implement the challenge for users to try
    ttf_range = st.slider(
        "Time to Fill Range (days):",
        min_value=int(hr_df['time_to_fill'].min()),
        max_value=int(hr_df['time_to_fill'].max()),
        value=(int(hr_df['time_to_fill'].min()), int(hr_df['time_to_fill'].max()))
    )
    
    min_ttf, max_ttf = ttf_range
    ttf_filtered_df = hr_df[hr_df['time_to_fill'].between(min_ttf, max_ttf)]
    
    # Show the result
    pct_in_range = len(ttf_filtered_df) / len(hr_df) * 100
    st.write(f"{pct_in_range:.1f}% of hires were completed within {min_ttf}-{max_ttf} days")
    
    # Show a chart of departments by avg time to fill
    dept_ttf = ttf_filtered_df.groupby('department')['time_to_fill'].mean().sort_values().reset_index()
    
    # Convert to format suitable for st.bar_chart
    dept_ttf_chart = pd.DataFrame({
        'Avg Days': dept_ttf['time_to_fill'].values
    }, index=dept_ttf['department'])
    
    st.subheader("Average Time-to-Fill by Department")
    st.bar_chart(dept_ttf_chart)
    
    # Next steps
    st.divider()
    st.markdown("**Next Module**: [HR Forms & Feedback Collection](placeholder)")