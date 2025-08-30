import streamlit as st
import pandas as pd
import numpy as np
import datetime
import math

def hr_visualizations_module():
    st.title("HR Data Visualization in Streamlit")
    
    # Module introduction with context
    st.markdown("""
    ## Making Magic Company: People Insights
    
    Effective data visualization transforms HR data into actionable insights. This module covers
    how to create compelling visualizations for HR metrics and KPIs using Streamlit.
    """)
    
    # Generate sample HR data
    @st.cache_data
    def generate_sample_hr_data(size=200):
        """Generate a realistic employee dataset for HR analytics demonstrations"""
        np.random.seed(42)  # For reproducibility
        
        # Current date for calculations
        today = datetime.datetime.now().date()
        
        # Employee IDs and basic info
        employee_ids = np.arange(1000, 1000+size)
        departments = ['Engineering', 'Product', 'Marketing', 'Sales', 'Customer Support', 
                      'Finance', 'HR', 'Operations', 'Research', 'Legal']
        dept_weights = [0.25, 0.15, 0.1, 0.15, 0.1, 0.05, 0.05, 0.1, 0.03, 0.02]
        
        job_levels = ['Entry', 'Associate', 'Mid-Level', 'Senior', 'Manager', 'Director', 'VP', 'Executive']
        level_weights = [0.15, 0.2, 0.25, 0.2, 0.1, 0.05, 0.03, 0.02]
        
        locations = ['Orlando', 'New York', 'San Francisco', 'Chicago', 'Austin', 'Remote']
        location_weights = [0.3, 0.15, 0.2, 0.1, 0.05, 0.2]
        
        # Generate basic employee data
        data = {
            'employee_id': employee_ids,
            'department': np.random.choice(departments, size=size, p=dept_weights),
            'job_level': np.random.choice(job_levels, size=size, p=level_weights),
            'location': np.random.choice(locations, size=size, p=location_weights),
            'hire_date': [today - datetime.timedelta(days=np.random.randint(1, 365*10)) for _ in range(size)],
        }
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Calculate tenure
        df['tenure_years'] = [(today - hire_date).days / 365 for hire_date in df['hire_date']]
        df['tenure_years'] = df['tenure_years'].round(1)
        
        # Add salary information
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
        # Add some variation
        df['salary'] = df['salary'] * np.random.uniform(0.8, 1.2, size=size)
        df['salary'] = df['salary'].round(-3)  # Round to nearest thousand
        
        # Add performance ratings (1-5 scale)
        df['performance_rating'] = np.random.normal(3.5, 0.8, size=size)
        df['performance_rating'] = df['performance_rating'].clip(1, 5).round(1)
        
        # Add engagement scores (1-10 scale)
        df['engagement_score'] = np.random.normal(7, 1.5, size=size)
        df['engagement_score'] = df['engagement_score'].clip(1, 10).round(1)
        
        # Add attrition risk (0-100%)
        df['attrition_risk'] = np.random.beta(2, 5, size=size) * 100
        df['attrition_risk'] = df['attrition_risk'].round(1)
        
        # Add gender (simplified)
        df['gender'] = np.random.choice(['Male', 'Female', 'Non-Binary'], 
                                       size=size, p=[0.48, 0.48, 0.04])
        
        # Add ethnicity (simplified categories for demo)
        df['ethnicity'] = np.random.choice(['Category A', 'Category B', 'Category C', 
                                           'Category D', 'Category E'], size=size)
        
        # Add historical data points
        # Monthly engagement scores for the past year
        months = 12
        for i in range(1, months+1):
            month_date = today - datetime.timedelta(days=30*i)
            month_name = month_date.strftime('%b')
            # Base the historical scores on current score with some random variation
            df[f'engagement_{month_name}'] = df['engagement_score'] + np.random.normal(0, 0.8, size=size)
            df[f'engagement_{month_name}'] = df[f'engagement_{month_name}'].clip(1, 10).round(1)
        
        # Create time-series data for headcount
        headcount_data = []
        for i in range(0, months+1):
            month_date = today - datetime.timedelta(days=30*i)
            month_name = month_date.strftime('%b %Y')
            
            # Calculate how many employees were active in each month
            monthly_headcount = sum(df['hire_date'] <= month_date)
            
            # Add some random attrition
            if i > 0:  # No attrition in current month
                attrition = int(monthly_headcount * np.random.uniform(0.005, 0.02))
                monthly_headcount -= attrition
            
            headcount_data.append({
                'month': month_name,
                'headcount': monthly_headcount
            })
        
        # Convert to DataFrame
        headcount_df = pd.DataFrame(headcount_data)
        
        return df, headcount_df
    
    # Generate sample data
    employee_df, headcount_df = generate_sample_hr_data()
    
    # Section 1: Basic HR Visualizations
    st.header("1. Basic HR Visualizations")
    
    # Use tabs for the learning components
    tab1, tab2, tab3 = st.tabs(["🔍 Live Example", "💻 Code", "📚 Explanation"])
    
    with tab1:
        st.subheader("Essential HR Metrics and Charts")
        
        # Display key metrics in a clean layout
        st.markdown("### Key HR Metrics")
        
        # Create columns for metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            headcount = len(employee_df)
            st.metric(
                label="Total Headcount", 
                value=f"{headcount:,}",
                delta=f"+{headcount - headcount_df.iloc[1]['headcount']} vs. prev month"
            )
        
        with col2:
            avg_tenure = employee_df['tenure_years'].mean()
            st.metric(
                label="Avg. Tenure", 
                value=f"{avg_tenure:.1f} years",
                delta=None
            )
        
        with col3:
            avg_engagement = employee_df['engagement_score'].mean()
            
            # Get previous month engagement
            prev_month = datetime.datetime.now().date() - datetime.timedelta(days=30)
            prev_month_name = prev_month.strftime('%b')
            prev_engagement = employee_df[f'engagement_{prev_month_name}'].mean()
            
            delta = avg_engagement - prev_engagement
            
            st.metric(
                label="Engagement Score", 
                value=f"{avg_engagement:.1f}/10",
                delta=f"{delta:+.1f} vs. prev month",
                delta_color="normal"
            )
        
        with col4:
            avg_risk = employee_df['attrition_risk'].mean()
            st.metric(
                label="Avg. Attrition Risk", 
                value=f"{avg_risk:.1f}%",
                delta="-2.3% vs. prev month",
                delta_color="inverse"  # Lower risk is better
            )
        
        # Create visualizations
        st.markdown("### Department Distribution")
        
        # Calculate department counts
        dept_counts = employee_df['department'].value_counts().reset_index()
        dept_counts.columns = ['Department', 'Count']
        
        # Display as chart
        st.bar_chart(
            dept_counts.set_index('Department'),
            use_container_width=True
        )
        
        # Show employee distribution by job level
        st.markdown("### Job Level Distribution")
        
        # Order levels correctly
        level_order = ['Entry', 'Associate', 'Mid-Level', 'Senior', 'Manager', 'Director', 'VP', 'Executive']
        
        # Calculate level counts
        level_counts = employee_df['job_level'].value_counts().reindex(level_order).reset_index()
        level_counts.columns = ['Job Level', 'Count']
        level_counts = level_counts.dropna()
        
        # Display as chart
        st.bar_chart(
            level_counts.set_index('Job Level'),
            use_container_width=True
        )
        
        # Show location distribution
        st.markdown("### Location Distribution")
        
        # Calculate location counts
        location_counts = employee_df['location'].value_counts().reset_index()
        location_counts.columns = ['Location', 'Count']
        
        # Display as pie chart using Streamlit
        st.bar_chart(
            location_counts.set_index('Location'),
            use_container_width=True
        )
    
    with tab2:
        # Store code snippets in variables
        metrics_code = """
# Create columns for key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    headcount = len(employee_df)
    st.metric(
        label="Total Headcount", 
        value=f"{headcount:,}",
        delta=f"+{headcount - headcount_df.iloc[1]['headcount']} vs. prev month"
    )

with col2:
    avg_tenure = employee_df['tenure_years'].mean()
    st.metric(
        label="Avg. Tenure", 
        value=f"{avg_tenure:.1f} years",
        delta=None
    )

with col3:
    avg_engagement = employee_df['engagement_score'].mean()
    
    # Get previous month engagement
    prev_month = datetime.datetime.now().date() - datetime.timedelta(days=30)
    prev_month_name = prev_month.strftime('%b')
    prev_engagement = employee_df[f'engagement_{prev_month_name}'].mean()
    
    delta = avg_engagement - prev_engagement
    
    st.metric(
        label="Engagement Score", 
        value=f"{avg_engagement:.1f}/10",
        delta=f"{delta:+.1f} vs. prev month",
        delta_color="normal"
    )

with col4:
    avg_risk = employee_df['attrition_risk'].mean()
    st.metric(
        label="Avg. Attrition Risk", 
        value=f"{avg_risk:.1f}%",
        delta="-2.3% vs. prev month",
        delta_color="inverse"  # Lower risk is better
    )
"""
        
        charts_code = """
# Department Distribution
st.markdown("### Department Distribution")

# Calculate department counts
dept_counts = employee_df['department'].value_counts().reset_index()
dept_counts.columns = ['Department', 'Count']

# Display as chart
st.bar_chart(
    dept_counts.set_index('Department'),
    use_container_width=True
)

# Job Level Distribution
st.markdown("### Job Level Distribution")

# Order levels correctly
level_order = ['Entry', 'Associate', 'Mid-Level', 'Senior', 'Manager', 'Director', 'VP', 'Executive']

# Calculate level counts
level_counts = employee_df['job_level'].value_counts().reindex(level_order).reset_index()
level_counts.columns = ['Job Level', 'Count']
level_counts = level_counts.dropna()

# Display as chart
st.bar_chart(
    level_counts.set_index('Job Level'),
    use_container_width=True
)
"""
        
        # Display code snippets
        st.subheader("Metrics Display Code")
        st.code(metrics_code)
        
        st.subheader("Charts Display Code")
        st.code(charts_code)
    
    with tab3:
        st.subheader("HR Visualization Best Practices")
        
        with st.expander("Key Metrics and KPIs", expanded=True):
            st.markdown("""
            **Best Practices for HR Metrics Visualization:**
            
            1. **Use the st.metric Component**
               - Perfect for displaying KPIs with comparisons
               - Helps highlight trends with delta indicators
               - Keep labels concise and clear
            
            2. **Choose Appropriate Comparisons**
               - Compare to previous periods (YoY, MoM)
               - Compare to targets or benchmarks
               - Use delta_color="inverse" when lower is better (e.g., attrition)
            
            3. **Group Related Metrics**
               - Use columns to organize metrics by category
               - Place most important metrics first (left to right)
               - Maintain consistent formatting across similar metrics
            
            4. **Format for Readability**
               - Use thousands separators for large numbers
               - Include units (%, years, $)
               - Round to appropriate precision (usually 1 decimal place for rates)
            """)
            
        with st.expander("Chart Selection for HR Data"):
            st.markdown("""
            **Choosing the Right Chart Type:**
            
            | Data Type | Best Chart Types | Examples |
            |-----------|------------------|----------|
            | Categorical distributions | Bar, Pie | Department headcount, Gender distribution |
            | Time series | Line, Area | Headcount trends, Engagement over time |
            | Rankings | Horizontal bar | Top departments by engagement |
            | Part-to-whole | Stacked bar, Pie | Team composition, Budget allocation |
            | Correlations | Scatter, Bubble | Salary vs. Performance, Engagement vs. Tenure |
            | Geographic | Maps | Office locations, Remote worker distribution |
            
            **Chart Selection Tips for HR Data:**
            
            - **Bar charts** are versatile and familiar - use for most categorical comparisons
            - **Line charts** show trends over time - ideal for metrics tracking
            - **Pie charts** should be used sparingly and only with few categories (<6)
            - **Scatter plots** help identify relationships between variables
            
            Remember that simpler visualizations are often more effective for decision-making.
            """)
    
    # Add a divider between sections
    st.divider()
    
    # Section 2: Interactive HR Dashboards
    st.header("2. Interactive HR Dashboards")
    
    # Use tabs for the learning components
    tab1, tab2, tab3 = st.tabs(["🔍 Live Example", "💻 Code", "📚 Explanation"])
    
    with tab1:
        st.subheader("Headcount Analysis Dashboard")
        
        # Create interactive filters
        st.markdown("### Dashboard Filters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Department filter
            selected_departments = st.multiselect(
                "Select Departments:",
                options=sorted(employee_df['department'].unique()),
                default=sorted(employee_df['department'].unique())
            )
        
        with col2:
            # Job level filter
            selected_levels = st.multiselect(
                "Select Job Levels:",
                options=level_order,
                default=level_order
            )
        
        # Filter the data
        filtered_df = employee_df[
            (employee_df['department'].isin(selected_departments)) &
            (employee_df['job_level'].isin(selected_levels))
        ]
        
        # Show filtered headcount
        st.markdown("### Filtered Headcount Analysis")
        
        # Display summary metrics based on filtered data
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtered_count = len(filtered_df)
            total_count = len(employee_df)
            st.metric(
                "Filtered Headcount", 
                f"{filtered_count:,}",
                f"{filtered_count/total_count:.1%} of total"
            )
        
        with col2:
            avg_salary = filtered_df['salary'].mean()
            st.metric(
                "Avg. Salary", 
                f"${avg_salary:,.0f}",
                None
            )
        
        with col3:
            avg_tenure = filtered_df['tenure_years'].mean()
            st.metric(
                "Avg. Tenure", 
                f"{avg_tenure:.1f} years",
                None
            )
        
        # Show headcount by department
        if len(selected_departments) > 1:
            st.markdown("### Headcount by Department")
            dept_counts = filtered_df['department'].value_counts().reset_index()
            dept_counts.columns = ['Department', 'Count']
            st.bar_chart(dept_counts.set_index('Department'))
        
        # Show headcount by job level
        if len(selected_levels) > 1:
            st.markdown("### Headcount by Job Level")
            level_counts = filtered_df['job_level'].value_counts().reindex(level_order).reset_index()
            level_counts.columns = ['Job Level', 'Count']
            level_counts = level_counts.dropna()
            st.bar_chart(level_counts.set_index('Job Level'))
        
        # Tenure distribution visualization
        st.markdown("### Tenure Distribution")
        
        # Create tenure bins
        tenure_bins = [0, 1, 2, 3, 5, 10, 15, 20]
        bin_labels = ['<1', '1-2', '2-3', '3-5', '5-10', '10-15', '15+']
        
        filtered_df['tenure_bin'] = pd.cut(
            filtered_df['tenure_years'], 
            bins=tenure_bins, 
            labels=bin_labels,
            right=False
        )
        
        tenure_counts = filtered_df['tenure_bin'].value_counts().reindex(bin_labels).reset_index()
        tenure_counts.columns = ['Tenure (Years)', 'Count']
        tenure_counts = tenure_counts.dropna()
        
        st.bar_chart(tenure_counts.set_index('Tenure (Years)'))
        
        # Time series headcount data
        st.markdown("### Headcount Trend (Past 12 Months)")
        
        # We'll use the pre-generated headcount data for simplicity
        # In a real app, you would filter this based on selection
        headcount_df = headcount_df.sort_values('month')
        
        # Convert to format for Streamlit chart
        headcount_chart_df = pd.DataFrame({
            'Headcount': headcount_df['headcount'].values
        }, index=headcount_df['month'])
        
        st.line_chart(headcount_chart_df)
    
    with tab2:
        # Store code snippets in variables
        dashboard_filters_code = """
# Create interactive filters
st.markdown("### Dashboard Filters")

col1, col2 = st.columns(2)

with col1:
    # Department filter
    selected_departments = st.multiselect(
        "Select Departments:",
        options=sorted(employee_df['department'].unique()),
        default=sorted(employee_df['department'].unique())
    )

with col2:
    # Job level filter
    selected_levels = st.multiselect(
        "Select Job Levels:",
        options=level_order,
        default=level_order
    )

# Filter the data
filtered_df = employee_df[
    (employee_df['department'].isin(selected_departments)) &
    (employee_df['job_level'].isin(selected_levels))
]
"""
        
        filtered_metrics_code = """
# Display summary metrics based on filtered data
col1, col2, col3 = st.columns(3)

with col1:
    filtered_count = len(filtered_df)
    total_count = len(employee_df)
    st.metric(
        "Filtered Headcount", 
        f"{filtered_count:,}",
        f"{filtered_count/total_count:.1%} of total"
    )

with col2:
    avg_salary = filtered_df['salary'].mean()
    st.metric(
        "Avg. Salary", 
        f"${avg_salary:,.0f}",
        None
    )

with col3:
    avg_tenure = filtered_df['tenure_years'].mean()
    st.metric(
        "Avg. Tenure", 
        f"{avg_tenure:.1f} years",
        None
    )
"""
        
        tenure_distribution_code = """
# Tenure distribution visualization
st.markdown("### Tenure Distribution")

# Create tenure bins
tenure_bins = [0, 1, 2, 3, 5, 10, 15, 20]
bin_labels = ['<1', '1-2', '2-3', '3-5', '5-10', '10-15', '15+']

filtered_df['tenure_bin'] = pd.cut(
    filtered_df['tenure_years'], 
    bins=tenure_bins, 
    labels=bin_labels,
    right=False
)

tenure_counts = filtered_df['tenure_bin'].value_counts().reindex(bin_labels).reset_index()
tenure_counts.columns = ['Tenure (Years)', 'Count']
tenure_counts = tenure_counts.dropna()

st.bar_chart(tenure_counts.set_index('Tenure (Years)'))
"""
        
        # Display code snippets
        st.subheader("Dashboard Filters Code")
        st.code(dashboard_filters_code)
        
        st.subheader("Filtered Metrics Code")
        st.code(filtered_metrics_code)
        
        st.subheader("Tenure Distribution Code")
        st.code(tenure_distribution_code)
    
    with tab3:
        st.subheader("Interactive Dashboard Design")
        
        with st.expander("Dashboard Design Principles", expanded=True):
            st.markdown("""
            **HR Dashboard Design Best Practices:**
            
            1. **Start with User Needs**
               - Different HR stakeholders need different views
               - Executives want high-level KPIs and trends
               - HR Business Partners need detailed team analytics
               - Recruiters focus on talent acquisition metrics
            
            2. **Apply a Clear Visual Hierarchy**
               - Place most important information at the top
               - Group related metrics and visualizations
               - Use consistent layout patterns across dashboards
               - Include clear section headers and descriptions
            
            3. **Enable Interactive Exploration**
               - Add filters that affect all dashboard elements
               - Allow drilling down from summary to detail
               - Maintain context when filtering
               - Provide clear visual feedback when filters are applied
            
            4. **Optimize for Performance**
               - Use caching for data-heavy operations (`@st.cache_data`)
               - Calculate metrics after filtering, not before
               - Limit the number of visualizations per page
               - Consider using tabs for different dashboard sections
            """)
            
        with st.expander("Effective Filtering Strategies"):
            st.markdown("""
            **Filtering Best Practices for HR Dashboards:**
            
            1. **Choose Appropriate Filter Types**
               - Use multiselect for selecting multiple categories
               - Use selectbox for single selection
               - Use sliders for numeric ranges
               - Use date inputs for time periods
            
            2. **Set Sensible Defaults**
               - Start with all values selected for overview
               - Pre-select the most common or relevant options
               - Remember user selections using session state
            
            3. **Place Filters Strategically**
               - Group filters at the top of the dashboard
               - Consider sidebar for complex filter sets
               - Keep filters visible when scrolling
            
            4. **Provide Filter Feedback**
               - Show how many records match the filter criteria
               - Display which filters are currently active
               - Allow easily resetting filters to default
            
            5. **Cascade Filters When Appropriate**
               - Update available options based on previous selections
               - Filter out invalid combinations
               - Maintain consistent behavior across filter sets
            """)
    
    # Add a divider between sections
    st.divider()
    
    # Section 3: Advanced HR Visualization Techniques
    st.header("3. Advanced HR Visualization Techniques")
    
    # Use tabs for the learning components
    tab1, tab2, tab3 = st.tabs(["🔍 Live Example", "💻 Code", "📚 Explanation"])
    
    with tab1:
        st.subheader("Employee Distribution Analysis")
        
        # Create a more advanced visualization layout
        st.markdown("### Salary Distribution by Job Level")
        
        # Create box plot-like visualization using Streamlit components
        job_levels = employee_df['job_level'].unique()
        
        # Prepare data for visualization
        boxplot_data = {}
        
        for level in level_order:
            if level in job_levels:
                level_salaries = employee_df[employee_df['job_level'] == level]['salary']
                if len(level_salaries) > 0:
                    boxplot_data[level] = {
                        'min': level_salaries.min(),
                        'q1': level_salaries.quantile(0.25),
                        'median': level_salaries.median(),
                        'q3': level_salaries.quantile(0.75),
                        'max': level_salaries.max(),
                        'mean': level_salaries.mean()
                    }
        
        # Create a manual box plot visualization
        for level, stats in boxplot_data.items():
            st.markdown(f"**{level}**")
            
            # Create a custom horizontal bar to represent the box plot
            col1, col2, col3 = st.columns([2, 8, 2])
            
            with col1:
                st.write(f"${stats['min']:,.0f}")
            
            with col2:
                # Create a progress bar to simulate box plot
                # Scale the values to 0-100 range
                salary_range = stats['max'] - stats['min']
                q1_pos = (stats['q1'] - stats['min']) / salary_range * 100
                median_pos = (stats['median'] - stats['min']) / salary_range * 100
                q3_pos = (stats['q3'] - stats['min']) / salary_range * 100
                
                # Custom HTML to create a box plot-like visualization
                box_html = f"""
                <div style="position: relative; height: 20px; width: 100%; background-color: #f0f2f6; border-radius: 3px;">
                    <div style="position: absolute; left: 0%; width: 100%; height: 100%; background-color: #f0f2f6; border-radius: 3px;"></div>
                    <div style="position: absolute; left: {q1_pos}%; width: {q3_pos - q1_pos}%; height: 100%; background-color: #9AD1FF; border-radius: 3px;"></div>
                    <div style="position: absolute; left: {median_pos}%; width: 2px; height: 100%; background-color: #0068C9; border-radius: 0px;"></div>
                </div>
                """
                st.markdown(box_html, unsafe_allow_html=True)
                
                # Add mean marker
                mean_pos = (stats['mean'] - stats['min']) / salary_range * 100
                mean_html = f"""
                <div style="position: relative; height: 20px; width: 100%;">
                    <div style="position: absolute; left: {mean_pos}%; top: -10px; transform: translateX(-50%);">
                        <span style="color: #FF4B4B; font-size: 15px;">▼</span>
                    </div>
                </div>
                """
                st.markdown(mean_html, unsafe_allow_html=True)
            
            with col3:
                st.write(f"${stats['max']:,.0f}")
            
            # Display the mean value
            st.caption(f"Mean: ${stats['mean']:,.0f} | Median: ${stats['median']:,.0f}")
        
        # Performance vs Engagement Scatter Plot Simulation
        st.markdown("### Performance vs. Engagement")
        
        # Prepare data for grid display
        performance_ranges = [1, 2, 3, 4, 5]
        engagement_ranges = [1, 3, 5, 7, 9, 11]  # For 1-10 scale
        
        # Create a heatmap-like visualization
        heatmap_data = []
        
        for i in range(len(performance_ranges)-1):
            for j in range(len(engagement_ranges)-1):
                p_min, p_max = performance_ranges[i], performance_ranges[i+1]
                e_min, e_max = engagement_ranges[j], engagement_ranges[j+1]
                
                count = len(employee_df[
                    (employee_df['performance_rating'] >= p_min) & 
                    (employee_df['performance_rating'] < p_max) &
                    (employee_df['engagement_score'] >= e_min) & 
                    (employee_df['engagement_score'] < e_max)
                ])
                
                heatmap_data.append({
                    'performance': f"{p_min}-{p_max}",
                    'engagement': f"{e_min}-{e_max}",
                    'count': count
                })
        
        # Convert to dataframe
        heatmap_df = pd.DataFrame(heatmap_data)
        
        # Create a pivot table
        heatmap_pivot = heatmap_df.pivot(index='performance', columns='engagement', values='count')
        
        # Display as a styled dataframe
        st.dataframe(
            heatmap_pivot,
            use_container_width=True,
            height=220
        )
        
        # Diversity Visualization
        st.markdown("### Diversity by Department")
        
        # Calculate diversity distribution by department
        diversity_by_dept = pd.crosstab(
            employee_df['department'], 
            employee_df['ethnicity'],
            normalize='index'
        ) * 100
        
        # Convert to long form for stacked bar chart
        diversity_long = diversity_by_dept.reset_index().melt(
            id_vars=['department'],
            var_name='ethnicity',
            value_name='percentage'
        )
        
        # Group by department and ethnicity
        diversity_grouped = diversity_long.groupby(['department', 'ethnicity'])['percentage'].sum().reset_index()
        
        # Display as table
        diversity_pivot = diversity_grouped.pivot(index='department', columns='ethnicity', values='percentage')
        diversity_pivot = diversity_pivot.round(1)
        
        st.dataframe(
            diversity_pivot,
            use_container_width=True
        )
        
        st.caption("Values represent percentage (%) of each ethnicity category within departments")
    
    with tab2:
        # Store code snippets in variables
        boxplot_code = """
# Create box plot-like visualization for salary distribution
job_levels = employee_df['job_level'].unique()

# Prepare data for visualization
boxplot_data = {}

for level in level_order:
    if level in job_levels:
        level_salaries = employee_df[employee_df['job_level'] == level]['salary']
        if len(level_salaries) > 0:
            boxplot_data[level] = {
                'min': level_salaries.min(),
                'q1': level_salaries.quantile(0.25),
                'median': level_salaries.median(),
                'q3': level_salaries.quantile(0.75),
                'max': level_salaries.max(),
                'mean': level_salaries.mean()
            }

# Create a manual box plot visualization
for level, stats in boxplot_data.items():
    st.markdown(f"**{level}**")
    
    # Create a custom horizontal bar to represent the box plot
    col1, col2, col3 = st.columns([2, 8, 2])
    
    with col1:
        st.write(f"${stats['min']:,.0f}")
    
    with col2:
        # Create a progress bar to simulate box plot
        # Scale the values to 0-100 range
        salary_range = stats['max'] - stats['min']
        q1_pos = (stats['q1'] - stats['min']) / salary_range * 100
        median_pos = (stats['median'] - stats['min']) / salary_range * 100
        q3_pos = (stats['q3'] - stats['min']) / salary_range * 100
        
        # Custom HTML to create a box plot-like visualization
        box_html = f\"\"\"
        <div style="position: relative; height: 20px; width: 100%; background-color: #f0f2f6; border-radius: 3px;">
            <div style="position: absolute; left: 0%; width: 100%; height: 100%; background-color: #f0f2f6; border-radius: 3px;"></div>
            <div style="position: absolute; left: {q1_pos}%; width: {q3_pos - q1_pos}%; height: 100%; background-color: #9AD1FF; border-radius: 3px;"></div>
            <div style="position: absolute; left: {median_pos}%; width: 2px; height: 100%; background-color: #0068C9; border-radius: 0px;"></div>
        </div>
        \"\"\"
        st.markdown(box_html, unsafe_allow_html=True)
"""
        
        heatmap_code = """
# Performance vs Engagement Heatmap
st.markdown("### Performance vs. Engagement")

# Prepare data for grid display
performance_ranges = [1, 2, 3, 4, 5]
engagement_ranges = [1, 3, 5, 7, 9, 11]  # For 1-10 scale

# Create a heatmap-like visualization
heatmap_data = []

for i in range(len(performance_ranges)-1):
    for j in range(len(engagement_ranges)-1):
        p_min, p_max = performance_ranges[i], performance_ranges[i+1]
        e_min, e_max = engagement_ranges[j], engagement_ranges[j+1]
        
        count = len(employee_df[
            (employee_df['performance_rating'] >= p_min) & 
            (employee_df['performance_rating'] < p_max) &
            (employee_df['engagement_score'] >= e_min) & 
            (employee_df['engagement_score'] < e_max)
        ])
        
        heatmap_data.append({
            'performance': f"{p_min}-{p_max}",
            'engagement': f"{e_min}-{e_max}",
            'count': count
        })

# Convert to dataframe
heatmap_df = pd.DataFrame(heatmap_data)

# Create a pivot table
heatmap_pivot = heatmap_df.pivot(index='performance', columns='engagement', values='count')

# Display as a styled dataframe
st.dataframe(
    heatmap_pivot,
    use_container_width=True,
    height=220
)
"""
        
        diversity_code = """
# Diversity Visualization
st.markdown("### Diversity by Department")

# Calculate diversity distribution by department
diversity_by_dept = pd.crosstab(
    employee_df['department'], 
    employee_df['ethnicity'],
    normalize='index'
) * 100

# Convert to long form for visualization
diversity_long = diversity_by_dept.reset_index().melt(
    id_vars=['department'],
    var_name='ethnicity',
    value_name='percentage'
)

# Group by department and ethnicity
diversity_grouped = diversity_long.groupby(['department', 'ethnicity'])['percentage'].sum().reset_index()

# Display as table
diversity_pivot = diversity_grouped.pivot(index='department', columns='ethnicity', values='percentage')
diversity_pivot = diversity_pivot.round(1)

st.dataframe(
    diversity_pivot,
    use_container_width=True
)
"""
        
        # Display code snippets
        st.subheader("Custom Box Plot Code")
        st.code(boxplot_code)
        
        st.subheader("Heatmap Visualization Code")
        st.code(heatmap_code)
        
        st.subheader("Diversity Analysis Code")
        st.code(diversity_code)
    
    with tab3:
        st.subheader("Advanced Visualization Techniques")
        
        with st.expander("Creating Custom Visualizations", expanded=True):
            st.markdown("""
            **Building Custom Visualizations in Streamlit:**
            
            When built-in chart options aren't enough, you can create custom visualizations using:
            
            1. **HTML/CSS with st.markdown**
               - Use HTML and CSS for completely custom visuals
               - Create interactive elements with minimal JavaScript
               - Style with CSS to match your app's design
            
            2. **Dataframes with Styling**
               - Use pandas styler to create heatmaps
               - Apply color scales to highlight patterns
               - Create custom tables with formatted values
            
            3. **Composite Components**
               - Combine standard Streamlit components creatively
               - Use columns to create side-by-side comparisons
               - Layer components to build more complex visuals
            
            4. **Advanced Visualization Libraries**
               - For more complex visualizations, consider using Plotly
               - Altair provides excellent declarative visualizations
               - Bokeh enables interactive JavaScript-powered charts
            
            Remember that custom visualizations may require more maintenance,
            so balance customization with maintainability.
            """)
            
        with st.expander("Visualization Ethics for HR Data"):
            st.markdown("""
            **Ethical Considerations for HR Visualizations:**
            
            1. **Privacy and Confidentiality**
               - Never display individual-level data for small groups
               - Aggregate data to protect employee privacy
               - Consider implementing access controls for sensitive dashboards
               - Remove identifiable information from visualizations
            
            2. **Avoiding Bias in Visualizations**
               - Be conscious of color choices (avoid reinforcing stereotypes)
               - Present complete data, not cherry-picked views
               - Include appropriate context and benchmarks
               - Be transparent about data limitations
            
            3. **Accessibility**
               - Use colorblind-friendly palettes
               - Don't rely solely on color to convey information
               - Provide text alternatives to charts where possible
               - Ensure dashboards work with screen readers
            
            4. **Responsible Data Storytelling**
               - Avoid visualizations that could stigmatize groups
               - Present multiple perspectives when relevant
               - Be transparent about methodology
               - Highlight uncertainty where it exists
            
            5. **Making HR Data Actionable**
               - Focus on insights that drive positive change
               - Connect visualizations to potential actions
               - Highlight patterns without attributing blame
               - Create psychologically safe environments for data discussions
            """)
    
    # Add a practical challenge
    st.divider()
    st.header("🧩 Practice Challenge")
    
    challenge_description = """
    **Challenge**: Create an Attrition Risk Dashboard
    
    Using the employee data provided, create a visualization that helps identify:
    
    1. Which departments have the highest average attrition risk
    2. The relationship between tenure and attrition risk
    3. How performance ratings correlate with attrition risk
    
    Bonus: Add interactivity to filter by department or job level.
    """
    
    st.info(challenge_description)
    
    # Provide a hint
    with st.expander("See Hint"):
        hint_code = """
# Attrition Risk Dashboard

# Create filters
department = st.selectbox(
    "Select Department:",
    options=["All Departments"] + sorted(employee_df['department'].unique().tolist())
)

# Filter data
if department == "All Departments":
    risk_df = employee_df.copy()
else:
    risk_df = employee_df[employee_df['department'] == department]

# Calculate departmental risk averages
dept_risk = risk_df.groupby('department')['attrition_risk'].mean().sort_values(ascending=False).reset_index()
dept_risk.columns = ['Department', 'Avg Risk (%)']
dept_risk['Avg Risk (%)'] = dept_risk['Avg Risk (%)'].round(1)

# Display as bar chart
st.bar_chart(dept_risk.set_index('Department'))

# Create a scatter plot of tenure vs risk
st.markdown("### Tenure vs. Attrition Risk")

# Group by tenure years (rounded to nearest year)
risk_df['tenure_rounded'] = risk_df['tenure_years'].round(0).astype(int)
tenure_risk = risk_df.groupby('tenure_rounded')['attrition_risk'].mean().reset_index()
tenure_risk.columns = ['Tenure (Years)', 'Avg Risk (%)']

# Display as line chart
st.line_chart(tenure_risk.set_index('Tenure (Years)'))
"""
        st.code(hint_code)
    
    # Next steps
    st.divider()
    st.markdown("**Next Module**: [HR Forms & Data Collection](placeholder)")