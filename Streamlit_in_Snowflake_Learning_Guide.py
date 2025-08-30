import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page Configuration
st.set_page_config(
    page_title="Streamlit in Snowflake Guide",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .lesson-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .code-example {
        background-color: #2e2e2e;
        color: #f8f8f2;
        padding: 15px;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_lesson' not in st.session_state:
    st.session_state.current_lesson = 0
if 'completed_lessons' not in st.session_state:
    st.session_state.completed_lessons = set()
if 'user_code' not in st.session_state:
    st.session_state.user_code = {}
if 'sample_data' not in st.session_state:
    # Generate sample HR data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='M')
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations']
    
    data = []
    for date in dates:
        for dept in departments:
            headcount = np.random.randint(50, 200)
            open_positions = np.random.randint(5, 25)
            attrition = np.random.randint(2, 15)
            savings = open_positions * np.random.randint(80000, 150000) / 12
            
            data.append({
                'Date': date,
                'Department': dept,
                'Headcount': headcount,
                'Open_Positions': open_positions,
                'Attrition': attrition,
                'Monthly_Savings': savings,
                'Budget': np.random.randint(1000000, 5000000),
                'Actual_Spend': np.random.randint(800000, 4500000)
            })
    
    st.session_state.sample_data = pd.DataFrame(data)

# Sidebar Navigation
with st.sidebar:
    st.markdown("# 🎓 Learning Path")
    st.markdown("---")
    
    lessons = [
        "🏠 Welcome & Overview",
        "🔌 Module 1: Snowflake Connection",
        "📊 Module 2: Data Structures",
        "⚙️ Module 3: Building Components",
        "📈 Module 4: Advanced Visualizations",
        "🛠️ Module 5: Metric Testing Tool",
        "🚀 Module 6: Build Your Own App",
        "📚 Resources & Best Practices"
    ]
    
    for i, lesson in enumerate(lessons):
        if i in st.session_state.completed_lessons:
            status = "✅"
        elif i == st.session_state.current_lesson:
            status = "👉"
        else:
            status = "⭕"
        
        if st.button(f"{status} {lesson}", key=f"lesson_{i}", use_container_width=True):
            st.session_state.current_lesson = i
    
    st.markdown("---")
    st.markdown("### 📈 Your Progress")
    progress = len(st.session_state.completed_lessons) / len(lessons)
    st.progress(progress)
    st.markdown(f"**{len(st.session_state.completed_lessons)}/{len(lessons)} Modules Completed**")

# Main Content Area
if st.session_state.current_lesson == 0:
    # Welcome & Overview
    st.markdown('<p class="main-header">Welcome to Streamlit in Snowflake! ❄️</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Interactive Guide for the Report Engineering Team</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 What You'll Learn
        
        This interactive guide will teach you how to:
        - **Connect** Streamlit apps to Snowflake data
        - **Structure** your data for optimal performance
        - **Build** interactive dashboards and web applications
        - **Create** metric testing tools and analytical interfaces
        - **Deploy** solutions for HR analytics and reporting
        
        ### 💡 Why Streamlit in Snowflake?
        
        - **Native Integration**: Direct access to your Snowflake data
        - **No Infrastructure**: Apps run directly in Snowflake
        - **Security**: Leverages Snowflake's security model
        - **Performance**: Optimized for large-scale data operations
        - **Collaboration**: Easy sharing within your organization
        """)
        
        st.info("""
        **🎓 Learning Approach**: Each module includes:
        - Concept explanation
        - Live code examples
        - Interactive exercises
        - Hands-on building experience
        """)
        
    with col2:
        st.markdown("### 🏢 Your Team Context")
        st.markdown("""
        **People Insights Team**
        - Data Strategy & Platform
        - Enterprise HR Partners
        - Headcount Management
        - Survey Analytics
        """)
        
        st.markdown("### 📊 Use Cases")
        st.markdown("""
        - Position Forecasting
        - Savings Analysis
        - Metric Testing
        - Population Analysis
        - Trend Visualization
        """)
    
    if st.button("🚀 Start Learning", type="primary", use_container_width=True):
        st.session_state.current_lesson = 1
        st.session_state.completed_lessons.add(0)
        st.rerun()

elif st.session_state.current_lesson == 1:
    # Module 1: Snowflake Connection
    st.markdown("# 🔌 Module 1: Connecting to Snowflake")
    
    tabs = st.tabs(["📖 Learn", "💻 Code", "🎯 Practice"])
    
    with tabs[0]:
        st.markdown("""
        ### Understanding Snowflake Connection in Streamlit
        
        When running Streamlit **within** Snowflake (Streamlit in Snowflake - SiS), the connection is handled automatically!
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Streamlit in Snowflake (SiS)")
            st.code("""
# Automatic connection - no credentials needed!
from snowflake.snowpark.context import get_active_session

session = get_active_session()

# Query data directly
df = session.sql('''
    SELECT * FROM HR_DATA.METRICS.HEADCOUNT
    WHERE DATE >= '2024-01-01'
''').to_pandas()
            """, language="python")
            
        with col2:
            st.markdown("#### 📝 External Streamlit App")
            st.code("""
# Manual connection required
import snowflake.connector

conn = snowflake.connector.connect(
    account='your_account',
    user='your_user',
    password='your_password',
    warehouse='COMPUTE_WH',
    database='HR_DATA',
    schema='METRICS'
)
            """, language="python")
        
        st.success("""
        **🎯 Key Advantage**: With SiS, you get automatic authentication, role-based access control, 
        and direct access to all your Snowflake objects without managing credentials!
        """)
        
    with tabs[1]:
        st.markdown("### 🔧 Connection Patterns")
        
        st.markdown("#### 1. Basic Query Pattern")
        st.code("""
from snowflake.snowpark.context import get_active_session
import streamlit as st
import pandas as pd

# Get session
session = get_active_session()

# Cache data for performance
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data(query):
    return session.sql(query).to_pandas()

# Use the function
df = load_data("SELECT * FROM HR_METRICS WHERE YEAR = 2024")
st.dataframe(df)
        """, language="python")
        
        st.markdown("#### 2. Dynamic Query Builder")
        st.code("""
def build_query(table, filters=None, columns="*"):
    query = f"SELECT {columns} FROM {table}"
    
    if filters:
        conditions = [f"{k} = '{v}'" for k, v in filters.items()]
        query += " WHERE " + " AND ".join(conditions)
    
    return query

# Usage
filters = {"DEPARTMENT": dept_selection, "YEAR": 2024}
query = build_query("HR_DATA.METRICS.HEADCOUNT", filters)
df = session.sql(query).to_pandas()
        """, language="python")
        
    with tabs[2]:
        st.markdown("### 🎯 Practice: Connect and Query")
        
        st.markdown("Let's practice with a simulated connection:")
        
        # Simulated connection interface
        col1, col2 = st.columns(2)
        
        with col1:
            database = st.selectbox("Select Database", ["HR_DATA", "FINANCE_DATA", "OPERATIONS"])
            schema = st.selectbox("Select Schema", ["METRICS", "RAW", "STAGING"])
            table = st.selectbox("Select Table", ["HEADCOUNT", "POSITIONS", "BUDGETS"])
        
        with col2:
            date_filter = st.date_input("Filter Date From", value=datetime(2024, 1, 1))
            dept_filter = st.multiselect("Filter Departments", 
                                        ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations"])
        
        if st.button("🔍 Execute Query", type="primary"):
            # Simulate query execution
            query = f"""
            SELECT * FROM {database}.{schema}.{table}
            WHERE DATE >= '{date_filter}'
            {f"AND DEPARTMENT IN ({','.join([f'\'{d}\'' for d in dept_filter])})" if dept_filter else ""}
            """
            
            st.code(query, language="sql")
            
            # Show sample data
            st.success("✅ Query executed successfully!")
            filtered_data = st.session_state.sample_data.copy()
            if dept_filter:
                filtered_data = filtered_data[filtered_data['Department'].isin(dept_filter)]
            st.dataframe(filtered_data.head(10))
            
            st.session_state.completed_lessons.add(1)

elif st.session_state.current_lesson == 2:
    # Module 2: Data Structures
    st.markdown("# 📊 Module 2: Data Structures for Streamlit")
    
    tabs = st.tabs(["📖 Concepts", "🏗️ Structure Design", "⚡ Performance", "🎯 Practice"])
    
    with tabs[0]:
        st.markdown("""
        ### Optimal Data Structures for Streamlit Apps
        
        The way you structure your data in Snowflake directly impacts your Streamlit app's performance and functionality.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 📁 Recommended Structure
            
            **1. Pre-aggregated Views**
            - Create materialized views for common aggregations
            - Reduces computation time in the app
            
            **2. Dimensional Model**
            - Fact tables for metrics
            - Dimension tables for attributes
            - Bridge tables for many-to-many relationships
            
            **3. Time-Series Optimization**
            - Partition by date
            - Cluster on frequently filtered columns
            """)
            
        with col2:
            st.markdown("""
            #### 🎯 For HR Analytics
            
            **Fact Tables:**
            - `FACT_HEADCOUNT` - Daily snapshots
            - `FACT_POSITIONS` - Position tracking
            - `FACT_SAVINGS` - Financial metrics
            
            **Dimension Tables:**
            - `DIM_EMPLOYEE` - Employee attributes
            - `DIM_DEPARTMENT` - Org structure
            - `DIM_DATE` - Date dimensions
            
            **Aggregation Tables:**
            - `AGG_MONTHLY_METRICS` - Pre-calculated KPIs
            """)
        
        st.info("""
        **💡 Pro Tip**: Pre-calculate complex metrics in Snowflake views rather than computing them in Streamlit. 
        This significantly improves app responsiveness!
        """)
        
    with tabs[1]:
        st.markdown("### 🏗️ Designing Your Data Structure")
        
        st.markdown("#### Example: Metric Testing Tool Data Structure")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**Input: Wide Format for Testing**")
            wide_data = pd.DataFrame({
                'Date': pd.date_range('2024-01', periods=3, freq='M'),
                'Metric_A_Dept1': [100, 105, 110],
                'Metric_A_Dept2': [200, 210, 220],
                'Metric_B_Dept1': [150, 155, 160],
                'Metric_B_Dept2': [250, 260, 270]
            })
            st.dataframe(wide_data, use_container_width=True)
            
        with col2:
            st.markdown("**Output: Long Format for Visualization**")
            long_data = pd.DataFrame({
                'Date': pd.date_range('2024-01', periods=6, freq='M').tolist() * 2,
                'Department': ['Dept1'] * 6 + ['Dept2'] * 6,
                'Metric': ['A', 'A', 'A', 'B', 'B', 'B'] * 2,
                'Value': [100, 105, 110, 150, 155, 160, 200, 210, 220, 250, 260, 270]
            })
            st.dataframe(long_data.head(8), use_container_width=True)
        
        st.code("""
-- Create a pre-calculated metrics table for your testing tool
CREATE OR REPLACE TABLE METRIC_TESTING_DATA AS
WITH base_metrics AS (
    SELECT 
        DATE,
        DEPARTMENT,
        POPULATION_SEGMENT,
        -- Different metric definitions
        HEADCOUNT as METRIC_DEF_1,
        HEADCOUNT - ATTRITION as METRIC_DEF_2,
        HEADCOUNT - ATTRITION + NEW_HIRES as METRIC_DEF_3,
        (HEADCOUNT - ATTRITION + NEW_HIRES) * 0.95 as METRIC_DEF_4,
        (HEADCOUNT + CONTRACTORS) as METRIC_DEF_5
    FROM FACT_HEADCOUNT
)
SELECT * FROM base_metrics;

-- Create an index for fast filtering
ALTER TABLE METRIC_TESTING_DATA 
CLUSTER BY (DATE, DEPARTMENT, POPULATION_SEGMENT);
        """, language="sql")
        
    with tabs[2]:
        st.markdown("### ⚡ Performance Optimization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🚀 Best Practices
            
            1. **Use Caching Strategically**
               - Cache expensive queries
               - Set appropriate TTL
               - Clear cache when data updates
            
            2. **Implement Pagination**
               - Don't load entire datasets
               - Use LIMIT and OFFSET
               - Implement infinite scroll
            
            3. **Optimize Queries**
               - Push filters to SQL
               - Use appropriate indexes
               - Minimize data transfer
            """)
            
        with col2:
            st.code("""
# Caching pattern for large datasets
@st.cache_data(ttl=3600)
def load_metrics(date_from, date_to, dept):
    query = f'''
    SELECT * FROM AGG_MONTHLY_METRICS
    WHERE DATE BETWEEN '{date_from}' AND '{date_to}'
    AND DEPARTMENT = '{dept}'
    LIMIT 10000
    '''
    return session.sql(query).to_pandas()

# Incremental loading pattern
def load_paginated(page=1, page_size=100):
    offset = (page - 1) * page_size
    query = f'''
    SELECT * FROM LARGE_TABLE
    LIMIT {page_size} OFFSET {offset}
    '''
    return session.sql(query).to_pandas()
            """, language="python")
        
    with tabs[3]:
        st.markdown("### 🎯 Practice: Design Your Structure")
        
        st.markdown("Let's design a data structure for a headcount forecasting tool:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Define Your Metrics")
            metric1 = st.text_input("Metric 1 Name", "Current_Headcount")
            metric2 = st.text_input("Metric 2 Name", "Projected_Headcount")
            metric3 = st.text_input("Metric 3 Name", "Variance")
            
            st.markdown("#### Define Dimensions")
            dims = st.multiselect("Select Dimensions", 
                                 ["Date", "Department", "Location", "Job_Level", "Cost_Center"],
                                 default=["Date", "Department"])
        
        with col2:
            st.markdown("#### Define Aggregations")
            aggs = st.multiselect("Pre-calculate these aggregations",
                                ["Monthly_Average", "Quarterly_Sum", "YTD_Total", "YoY_Growth"],
                                default=["Monthly_Average"])
            
            st.markdown("#### Performance Settings")
            partition = st.selectbox("Partition By", ["Date", "Department", "None"])
            cluster = st.multiselect("Cluster By", ["Date", "Department", "Location"])
        
        if st.button("🏗️ Generate Structure", type="primary"):
            sql_code = f"""
-- Fact Table
CREATE OR REPLACE TABLE FACT_FORECAST AS
SELECT 
    {', '.join(dims)},
    {metric1},
    {metric2},
    {metric3}
FROM source_data;

-- Aggregation Table
CREATE OR REPLACE TABLE AGG_FORECAST_{aggs[0].upper() if aggs else 'METRICS'} AS
SELECT 
    {', '.join(dims)},
    {f'AVG({metric1}) as AVG_{metric1},' if 'Monthly_Average' in aggs else ''}
    {f'SUM({metric2}) as SUM_{metric2},' if 'Quarterly_Sum' in aggs else ''}
    {f'SUM({metric3}) as TOTAL_{metric3}' if 'YTD_Total' in aggs else ''}
FROM FACT_FORECAST
GROUP BY {', '.join(dims)};

{f'-- Performance Optimization' if partition != 'None' or cluster else ''}
{f'ALTER TABLE FACT_FORECAST CLUSTER BY ({", ".join(cluster)});' if cluster else ''}
            """
            
            st.code(sql_code, language="sql")
            st.success("✅ Structure designed! Copy this SQL to create your tables in Snowflake.")
            st.session_state.completed_lessons.add(2)

elif st.session_state.current_lesson == 3:
    # Module 3: Building Components
    st.markdown("# ⚙️ Module 3: Building Interactive Components")
    
    tabs = st.tabs(["🎛️ Input Controls", "📊 Display Components", "🔄 Interactivity", "🎯 Build"])
    
    with tabs[0]:
        st.markdown("### 🎛️ Input Controls for HR Analytics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Date Controls")
            date_single = st.date_input("Single Date", datetime.now())
            date_range = st.date_input("Date Range", 
                                      value=(datetime.now() - timedelta(days=30), datetime.now()))
            
            st.markdown("#### Numeric Inputs")
            threshold = st.slider("Threshold", 0, 100, 50)
            target = st.number_input("Target Value", value=1000)
            
        with col2:
            st.markdown("#### Selection Controls")
            dept = st.selectbox("Department", ["Engineering", "Sales", "HR"])
            metrics = st.multiselect("Metrics", ["Headcount", "Attrition", "Savings"])
            radio_choice = st.radio("View Type", ["Table", "Chart", "Summary"])
            
        with col3:
            st.markdown("#### Advanced Controls")
            with st.expander("Filters"):
                location = st.selectbox("Location", ["All", "Remote", "Office"])
                level = st.selectbox("Level", ["All", "Junior", "Senior", "Lead"])
            
            toggle = st.toggle("Show Advanced Options")
            if toggle:
                st.text_area("Custom SQL Filter", "DEPARTMENT = 'Engineering'")
        
        st.info("💡 **Tip**: Group related controls together and use expanders for advanced options to keep the UI clean.")
        
    with tabs[1]:
        st.markdown("### 📊 Display Components")
        
        # Generate sample data for display
        display_data = st.session_state.sample_data.copy()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Metrics Display")
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                st.metric("Total Headcount", "1,234", "+5.2%")
            with metric_col2:
                st.metric("Open Positions", "45", "-12", delta_color="inverse")
            with metric_col3:
                st.metric("Monthly Savings", "$234K", "+$15K")
            
            st.markdown("#### Data Tables")
            st.dataframe(
                display_data.head(),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Monthly_Savings": st.column_config.NumberColumn(
                        "Savings",
                        format="$%.0f"
                    ),
                    "Date": st.column_config.DateColumn(
                        "Month",
                        format="MMM YYYY"
                    )
                }
            )
            
        with col2:
            st.markdown("#### Interactive Charts")
            
            chart_data = display_data.groupby('Department')['Headcount'].sum().reset_index()
            fig = px.bar(chart_data, x='Department', y='Headcount', 
                        title="Headcount by Department",
                        color='Headcount',
                        color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Progress Indicators")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.progress(0.65, text="Hiring Progress: 65%")
        with col2:
            st.progress(0.82, text="Budget Utilization: 82%")
        with col3:
            st.progress(0.45, text="Savings Target: 45%")
        
    with tabs[2]:
        st.markdown("### 🔄 Creating Interactivity")
        
        st.markdown("#### State Management Example")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Interactive Filters**")
            
            # Department filter with callback
            selected_dept = st.selectbox(
                "Select Department",
                options=st.session_state.sample_data['Department'].unique(),
                key="dept_filter"
            )
            
            # Date range filter
            date_range = st.select_slider(
                "Select Date Range",
                options=st.session_state.sample_data['Date'].dt.strftime('%Y-%m').unique(),
                value=(st.session_state.sample_data['Date'].dt.strftime('%Y-%m').iloc[0],
                      st.session_state.sample_data['Date'].dt.strftime('%Y-%m').iloc[-1])
            )
            
            # Metric selection
            selected_metric = st.radio(
                "Select Metric",
                ["Headcount", "Open_Positions", "Monthly_Savings"]
            )
        
        with col2:
            st.markdown("**Dynamic Visualization**")
            
            # Filter data based on selections
            filtered_data = st.session_state.sample_data[
                st.session_state.sample_data['Department'] == selected_dept
            ].copy()
            
            # Create interactive chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=filtered_data['Date'],
                y=filtered_data[selected_metric],
                mode='lines+markers',
                name=selected_metric,
                line=dict(width=3)
            ))
            
            fig.update_layout(
                title=f"{selected_metric} Trend for {selected_dept}",
                xaxis_title="Date",
                yaxis_title=selected_metric,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.code("""
# Pattern for reactive updates
def update_chart():
    filtered_data = df[df['Department'] == st.session_state.dept_filter]
    return create_chart(filtered_data)

# Use callbacks for immediate updates
dept = st.selectbox("Department", options, 
                    key="dept_filter",
                    on_change=update_chart)
        """, language="python")
        
    with tabs[3]:
        st.markdown("### 🎯 Build Your Component")
        
        st.markdown("Create a custom metric comparison component:")
        
        with st.container():
            st.markdown("#### Component Builder")
            
            # Component settings
            col1, col2, col3 = st.columns(3)
            
            with col1:
                component_type = st.selectbox("Component Type", 
                    ["Metric Card", "Comparison Chart", "Data Table", "KPI Dashboard"])
            
            with col2:
                num_metrics = st.number_input("Number of Metrics", 1, 5, 3)
            
            with col3:
                layout = st.radio("Layout", ["Horizontal", "Vertical", "Grid"])
            
            # Build the component
            if component_type == "Metric Card":
                st.markdown("---")
                if layout == "Horizontal":
                    cols = st.columns(num_metrics)
                    for i, col in enumerate(cols[:num_metrics]):
                        with col:
                            value = np.random.randint(100, 1000)
                            delta = np.random.randint(-50, 50)
                            st.metric(f"Metric {i+1}", value, f"{delta:+d}")
                
                elif layout == "Grid":
                    rows = (num_metrics + 1) // 2
                    for row in range(rows):
                        cols = st.columns(2)
                        for col_idx, col in enumerate(cols):
                            metric_idx = row * 2 + col_idx
                            if metric_idx < num_metrics:
                                with col:
                                    value = np.random.randint(100, 1000)
                                    delta = np.random.randint(-50, 50)
                                    st.metric(f"Metric {metric_idx+1}", value, f"{delta:+d}")
            
            elif component_type == "Comparison Chart":
                # Generate comparison data
                categories = ['Q1', 'Q2', 'Q3', 'Q4']
                fig = go.Figure()
                
                for i in range(num_metrics):
                    fig.add_trace(go.Bar(
                        name=f'Metric {i+1}',
                        x=categories,
                        y=np.random.randint(50, 200, 4)
                    ))
                
                fig.update_layout(barmode='group', title="Metric Comparison")
                st.plotly_chart(fig, use_container_width=True)
            
            # Show the code
            with st.expander("📝 View Generated Code"):
                if component_type == "Metric Card":
                    code = f"""
# Metric Cards Component
cols = st.columns({num_metrics})
for i, col in enumerate(cols):
    with col:
        value = fetch_metric_value(metric_names[i])
        delta = calculate_delta(metric_names[i])
        st.metric(metric_names[i], value, delta)
                    """
                else:
                    code = f"""
# Comparison Chart Component
fig = go.Figure()
for metric in selected_metrics:
    fig.add_trace(go.Bar(
        name=metric,
        x=periods,
        y=get_metric_values(metric, periods)
    ))
fig.update_layout(barmode='group')
st.plotly_chart(fig, use_container_width=True)
                    """
                st.code(code, language="python")
            
            if st.button("✅ Complete Module", type="primary"):
                st.session_state.completed_lessons.add(3)
                st.success("Great job! You've learned how to build interactive components!")

elif st.session_state.current_lesson == 4:
    # Module 4: Advanced Visualizations
    st.markdown("# 📈 Module 4: Advanced Visualizations")
    
    tabs = st.tabs(["📊 Chart Types", "🎨 Customization", "📈 Multi-Metric", "🎯 Practice"])
    
    with tabs[0]:
        st.markdown("### 📊 Advanced Chart Types for HR Analytics")
        
        # Prepare sample data
        viz_data = st.session_state.sample_data.copy()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Hierarchical Visualizations")
            
            # Sunburst chart
            sunburst_data = pd.DataFrame({
                'Department': ['Engineering'] * 3 + ['Sales'] * 3 + ['HR'] * 2,
                'Team': ['Backend', 'Frontend', 'DevOps', 'Enterprise', 'SMB', 'Partners', 'Recruiting', 'People Ops'],
                'Headcount': [45, 38, 22, 55, 42, 28, 15, 12]
            })
            
            fig_sun = px.sunburst(sunburst_data, 
                                  path=['Department', 'Team'], 
                                  values='Headcount',
                                  title="Organization Hierarchy")
            st.plotly_chart(fig_sun, use_container_width=True)
            
        with col2:
            st.markdown("#### Time-Series with Annotations")
            
            # Line chart with annotations
            ts_data = viz_data.groupby('Date')['Headcount'].sum().reset_index()
            
            fig_ts = go.Figure()
            fig_ts.add_trace(go.Scatter(
                x=ts_data['Date'],
                y=ts_data['Headcount'],
                mode='lines',
                name='Headcount',
                line=dict(color='#1E88E5', width=3)
            ))
            
            # Add annotation
            fig_ts.add_annotation(
                x=ts_data['Date'].iloc[6],
                y=ts_data['Headcount'].iloc[6],
                text="Hiring Freeze",
                showarrow=True,
                arrowhead=2,
                bgcolor="red",
                bordercolor="red",
                font=dict(color="white")
            )
            
            fig_ts.update_layout(title="Headcount Trend with Events")
            st.plotly_chart(fig_ts, use_container_width=True)
        
        # Heatmap
        st.markdown("#### Correlation Heatmap")
        
        # Create correlation matrix
        corr_data = viz_data[['Headcount', 'Open_Positions', 'Attrition', 'Monthly_Savings']].corr()
        
        fig_heat = px.imshow(corr_data,
                            labels=dict(color="Correlation"),
                            x=corr_data.columns,
                            y=corr_data.columns,
                            color_continuous_scale='RdBu',
                            zmin=-1, zmax=1)
        fig_heat.update_layout(title="Metric Correlations")
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with tabs[1]:
        st.markdown("### 🎨 Customization & Styling")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Chart Customization Options")
            
            # Customization controls
            chart_title = st.text_input("Chart Title", "Department Performance")
            color_scheme = st.selectbox("Color Scheme", 
                ["Blues", "Viridis", "Plasma", "Custom"])
            show_grid = st.checkbox("Show Grid", value=True)
            show_legend = st.checkbox("Show Legend", value=True)
            
            if color_scheme == "Custom":
                custom_color = st.color_picker("Pick a color", "#1E88E5")
                colors = [custom_color]
            else:
                colors = None
            
        with col2:
            # Apply customizations
            dept_data = viz_data.groupby('Department')['Monthly_Savings'].sum().reset_index()
            
            fig_custom = px.bar(dept_data, 
                               x='Department', 
                               y='Monthly_Savings',
                               title=chart_title,
                               color='Monthly_Savings',
                               color_continuous_scale=color_scheme if color_scheme != "Custom" else None)
            
            if color_scheme == "Custom":
                fig_custom.update_traces(marker_color=custom_color)
            
            fig_custom.update_layout(
                showlegend=show_legend,
                xaxis=dict(showgrid=show_grid),
                yaxis=dict(showgrid=show_grid)
            )
            
            st.plotly_chart(fig_custom, use_container_width=True)
        
        st.code("""
# Custom theme configuration
custom_theme = {
    'bgcolor': '#f0f2f6',
    'font_family': 'Arial, sans-serif',
    'title_font_size': 20,
    'grid_color': '#e1e5eb',
    'line_colors': ['#1E88E5', '#43A047', '#FB8C00', '#8E24AA']
}

fig.update_layout(
    paper_bgcolor=custom_theme['bgcolor'],
    plot_bgcolor=custom_theme['bgcolor'],
    font=dict(family=custom_theme['font_family']),
    title_font_size=custom_theme['title_font_size'],
    xaxis=dict(gridcolor=custom_theme['grid_color']),
    yaxis=dict(gridcolor=custom_theme['grid_color'])
)
        """, language="python")
        
    with tabs[2]:
        st.markdown("### 📈 Multi-Metric Comparisons")
        
        st.markdown("#### Build a Metric Testing Visualization")
        
        # Metric selection
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            st.markdown("**Select Metrics to Compare**")
            metrics_to_compare = st.multiselect(
                "Choose up to 5 metrics",
                ["Headcount", "Open_Positions", "Attrition", "Monthly_Savings", "Budget"],
                default=["Headcount", "Open_Positions"],
                max_selections=5
            )
            
        with col2:
            st.markdown("**Comparison Type**")
            comparison_type = st.radio(
                "Visualization",
                ["Trend Lines", "Bar Comparison", "Scatter Matrix", "Radar Chart"]
            )
            
        with col3:
            if metrics_to_compare and comparison_type:
                if comparison_type == "Trend Lines":
                    fig_multi = go.Figure()
                    
                    for metric in metrics_to_compare:
                        metric_data = viz_data.groupby('Date')[metric].sum().reset_index()
                        
                        # Normalize data for comparison
                        normalized = (metric_data[metric] - metric_data[metric].min()) / \
                                   (metric_data[metric].max() - metric_data[metric].min())
                        
                        fig_multi.add_trace(go.Scatter(
                            x=metric_data['Date'],
                            y=normalized,
                            mode='lines+markers',
                            name=metric
                        ))
                    
                    fig_multi.update_layout(
                        title="Normalized Metric Comparison",
                        yaxis_title="Normalized Value (0-1)",
                        hovermode='x unified'
                    )
                    
                elif comparison_type == "Bar Comparison":
                    dept_metrics = viz_data.groupby('Department')[metrics_to_compare].sum().reset_index()
                    
                    fig_multi = go.Figure()
                    for metric in metrics_to_compare:
                        fig_multi.add_trace(go.Bar(
                            name=metric,
                            x=dept_metrics['Department'],
                            y=dept_metrics[metric]
                        ))
                    
                    fig_multi.update_layout(
                        title="Metrics by Department",
                        barmode='group'
                    )
                    
                elif comparison_type == "Radar Chart":
                    # Aggregate data for radar chart
                    dept_avg = viz_data.groupby('Department')[metrics_to_compare].mean()
                    
                    fig_multi = go.Figure()
                    
                    for dept in dept_avg.index[:3]:  # Show top 3 departments
                        fig_multi.add_trace(go.Scatterpolar(
                            r=dept_avg.loc[dept].values,
                            theta=metrics_to_compare,
                            fill='toself',
                            name=dept
                        ))
                    
                    fig_multi.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True
                            )),
                        showlegend=True,
                        title="Department Performance Radar"
                    )
                else:
                    fig_multi = go.Figure()
                
                st.plotly_chart(fig_multi, use_container_width=True)
        
    with tabs[3]:
        st.markdown("### 🎯 Practice: Create Your Dashboard")
        
        st.markdown("Build a comprehensive visualization dashboard:")
        
        # Dashboard builder
        st.markdown("#### Dashboard Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            dashboard_title = st.text_input("Dashboard Title", "HR Analytics Dashboard")
            num_charts = st.slider("Number of Charts", 1, 6, 4)
            layout_cols = st.radio("Layout", ["1 Column", "2 Columns", "3 Columns"])
        
        with col2:
            chart_types = []
            for i in range(num_charts):
                chart_type = st.selectbox(
                    f"Chart {i+1} Type",
                    ["Line", "Bar", "Pie", "Scatter", "Heatmap"],
                    key=f"chart_type_{i}"
                )
                chart_types.append(chart_type)
        
        if st.button("📊 Generate Dashboard", type="primary"):
            st.markdown(f"### {dashboard_title}")
            
            # Determine layout
            if layout_cols == "1 Column":
                cols_per_row = 1
            elif layout_cols == "2 Columns":
                cols_per_row = 2
            else:
                cols_per_row = 3
            
            # Create charts
            chart_idx = 0
            while chart_idx < num_charts:
                cols = st.columns(min(cols_per_row, num_charts - chart_idx))
                
                for col in cols:
                    if chart_idx < num_charts:
                        with col:
                            chart_type = chart_types[chart_idx]
                            
                            if chart_type == "Line":
                                data = viz_data.groupby('Date')['Headcount'].sum().reset_index()
                                fig = px.line(data, x='Date', y='Headcount', title=f"Chart {chart_idx+1}: Trend")
                            elif chart_type == "Bar":
                                data = viz_data.groupby('Department')['Headcount'].sum().reset_index()
                                fig = px.bar(data, x='Department', y='Headcount', title=f"Chart {chart_idx+1}: Comparison")
                            elif chart_type == "Pie":
                                data = viz_data.groupby('Department')['Headcount'].sum().reset_index()
                                fig = px.pie(data, values='Headcount', names='Department', title=f"Chart {chart_idx+1}: Distribution")
                            elif chart_type == "Scatter":
                                fig = px.scatter(viz_data, x='Headcount', y='Monthly_Savings', 
                                               color='Department', title=f"Chart {chart_idx+1}: Correlation")
                            else:  # Heatmap
                                pivot_data = viz_data.pivot_table(values='Headcount', 
                                                                 index='Department', 
                                                                 columns=viz_data['Date'].dt.month)
                                fig = px.imshow(pivot_data, title=f"Chart {chart_idx+1}: Heatmap")
                            
                            st.plotly_chart(fig, use_container_width=True)
                        chart_idx += 1
            
            st.success("✅ Dashboard created successfully!")
            st.session_state.completed_lessons.add(4)

elif st.session_state.current_lesson == 5:
    # Module 5: Survey Sentiment Tagging Tool
    st.markdown("# 💬 Module 5: Building a Survey Sentiment Tagging Tool")
    
    st.info("""
    This module demonstrates how to build a powerful survey analysis tool for the People Insights team - 
    enabling sentiment analysis, automatic tagging, and theme extraction from employee feedback.
    """)
    
    tabs = st.tabs(["📐 Architecture", "🔧 Implementation", "🚀 Live Demo", "💡 Enhancements"])
    
    with tabs[0]:
        st.markdown("### 📐 Tool Architecture")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Core Components
            
            1. **Data Layer**
               - Survey responses table
               - Sentiment scores
               - Tag categories
               - Response metadata
            
            2. **Processing Layer**
               - Sentiment analysis
               - Keyword extraction
               - Theme clustering
               - Tag assignment
            
            3. **Visualization Layer**
               - Sentiment distribution
               - Theme trends
               - Department comparisons
               - Word clouds
            """)
            
        with col2:
            st.markdown("""
            #### Data Structure
            
            ```sql
            SURVEY_RESPONSES:
            - Response_ID (VARCHAR)
            - Date (DATE)
            - Department (VARCHAR)
            - Question (VARCHAR)
            - Response_Text (TEXT)
            - Sentiment_Score (FLOAT)
            - Sentiment_Label (VARCHAR)
            - Tags (ARRAY)
            - Theme (VARCHAR)
            ```
            
            #### Key Features
            - Auto-tag responses
            - Sentiment scoring
            - Theme identification
            - Bulk processing
            - Export capabilities
            """)
        
        st.code("""
# Core structure of the survey sentiment tool
class SurveySentimentTool:
    def __init__(self):
        self.sentiment_categories = {
            'positive': ['great', 'excellent', 'love', 'amazing', 'wonderful'],
            'negative': ['poor', 'bad', 'terrible', 'hate', 'awful'],
            'neutral': ['okay', 'fine', 'average', 'normal']
        }
        
        self.tag_categories = {
            'compensation': ['salary', 'pay', 'bonus', 'compensation', 'benefits'],
            'culture': ['culture', 'values', 'team', 'collaboration', 'environment'],
            'growth': ['career', 'development', 'growth', 'learning', 'promotion'],
            'management': ['manager', 'leadership', 'supervision', 'boss'],
            'worklife': ['balance', 'flexibility', 'remote', 'hours', 'time']
        }
    
    def analyze_sentiment(self, text):
        # Simple sentiment scoring (-1 to 1)
        score = 0
        text_lower = text.lower()
        
        for word in self.sentiment_categories['positive']:
            if word in text_lower:
                score += 0.3
        
        for word in self.sentiment_categories['negative']:
            if word in text_lower:
                score -= 0.3
        
        return max(-1, min(1, score))
    
    def auto_tag(self, text):
        tags = []
        text_lower = text.lower()
        
        for category, keywords in self.tag_categories.items():
            for keyword in keywords:
                if keyword in text_lower:
                    tags.append(category)
                    break
        
        return list(set(tags))
        """, language="python")
        
    with tabs[1]:
        st.markdown("### 🔧 Implementation")
        
        # Generate sample survey data
        np.random.seed(42)
        
        sample_responses = [
            "The work-life balance has improved significantly with the new remote policy. Great initiative!",
            "I feel my manager doesn't provide enough feedback on my performance.",
            "Love the learning opportunities and career development programs offered.",
            "The salary is below market rate for my position and experience.",
            "Team collaboration is excellent, really enjoy working with my colleagues.",
            "Need more flexibility in working hours to manage family responsibilities.",
            "The company culture is amazing, very inclusive and supportive environment.",
            "Poor communication from leadership about company direction.",
            "Benefits package is comprehensive but could use better health coverage.",
            "Excellent growth opportunities, I've learned so much this year!",
            "The bonus structure is unclear and seems unfair.",
            "My manager is very supportive and helps me grow professionally.",
            "Work from home policy is too restrictive compared to other companies.",
            "Great team spirit and collaboration across departments.",
            "Limited career advancement opportunities in my department."
        ]
        
        departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations']
        
        # Create sample survey dataframe
        survey_data = []
        for i, response in enumerate(sample_responses * 4):  # Multiply for more data
            dept = np.random.choice(departments)
            date = pd.Timestamp('2024-01-01') + pd.Timedelta(days=np.random.randint(0, 365))
            
            # Simple sentiment calculation
            sentiment_score = np.random.uniform(-1, 1)
            if 'great' in response.lower() or 'excellent' in response.lower() or 'love' in response.lower():
                sentiment_score = abs(sentiment_score)
                sentiment_label = 'Positive'
            elif 'poor' in response.lower() or 'need' in response.lower() or 'limited' in response.lower():
                sentiment_score = -abs(sentiment_score)
                sentiment_label = 'Negative'
            else:
                sentiment_score = sentiment_score * 0.3
                sentiment_label = 'Neutral'
            
            survey_data.append({
                'Response_ID': f'R{1000+i}',
                'Date': date,
                'Department': dept,
                'Response': response,
                'Sentiment_Score': sentiment_score,
                'Sentiment_Label': sentiment_label,
                'Word_Count': len(response.split())
            })
        
        survey_df = pd.DataFrame(survey_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Configuration")
            
            # Sentiment thresholds
            with st.expander("Sentiment Thresholds"):
                positive_threshold = st.slider("Positive threshold", 0.0, 1.0, 0.3)
                negative_threshold = st.slider("Negative threshold", -1.0, 0.0, -0.3)
                
                st.code(f"""
# Sentiment Classification
if score > {positive_threshold}:
    label = "Positive"
elif score < {negative_threshold}:
    label = "Negative"
else:
    label = "Neutral"
                """)
            
            # Tag categories
            with st.expander("Tag Categories"):
                st.markdown("**Current Categories:**")
                categories = {
                    '💰 Compensation': ['salary', 'pay', 'bonus', 'benefits'],
                    '🏢 Culture': ['culture', 'values', 'team', 'environment'],
                    '📈 Growth': ['career', 'development', 'learning', 'promotion'],
                    '👔 Management': ['manager', 'leadership', 'supervision'],
                    '⚖️ Work-Life': ['balance', 'flexibility', 'remote', 'hours']
                }
                
                for cat, keywords in categories.items():
                    st.write(f"{cat}: {', '.join(keywords)}")
        
        with col2:
            st.markdown("#### Sample Data Preview")
            
            # Show sample data
            st.dataframe(
                survey_df.head(10),
                use_container_width=True,
                hide_index=True,
                column_config={
                    'Sentiment_Score': st.column_config.ProgressColumn(
                        "Sentiment",
                        min_value=-1,
                        max_value=1,
                        format="%.2f"
                    ),
                    'Response': st.column_config.TextColumn(
                        "Response",
                        width="large"
                    )
                }
            )
            
            # Quick stats
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            with col_stat1:
                st.metric("Total Responses", len(survey_df))
            with col_stat2:
                avg_sentiment = survey_df['Sentiment_Score'].mean()
                st.metric("Avg Sentiment", f"{avg_sentiment:.2f}")
            with col_stat3:
                positive_pct = (survey_df['Sentiment_Label'] == 'Positive').mean() * 100
                st.metric("Positive %", f"{positive_pct:.1f}%")
    
    with tabs[2]:
        st.markdown("### 🚀 Live Survey Analysis Demo")
        
        # Create three columns for the main interface
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown("#### 🎛️ Controls")
            
            # Department filter
            selected_depts = st.multiselect(
                "Filter Departments",
                options=survey_df['Department'].unique(),
                default=survey_df['Department'].unique()[:3]
            )
            
            # Date range
            date_range = st.date_input(
                "Date Range",
                value=(survey_df['Date'].min(), survey_df['Date'].max()),
                min_value=survey_df['Date'].min(),
                max_value=survey_df['Date'].max()
            )
            
            # Sentiment filter
            sentiment_filter = st.multiselect(
                "Sentiment Filter",
                options=['Positive', 'Neutral', 'Negative'],
                default=['Positive', 'Neutral', 'Negative']
            )
            
            # Analysis type
            analysis_mode = st.radio(
                "Analysis Mode",
                ["Sentiment Overview", "Theme Analysis", "Department Comparison", "Time Trends"]
            )
            
            st.markdown("---")
            
            # Process new response
            st.markdown("#### 🆕 Analyze New Response")
            new_response = st.text_area(
                "Enter survey response:",
                height=100,
                placeholder="Type or paste a survey response here..."
            )
            
            if st.button("🔍 Analyze", type="primary"):
                if new_response:
                    # Simple sentiment analysis
                    sentiment_words = {
                        'positive': ['great', 'excellent', 'good', 'amazing', 'love', 'wonderful', 'fantastic'],
                        'negative': ['bad', 'poor', 'terrible', 'hate', 'awful', 'disappointing', 'frustrated']
                    }
                    
                    score = 0
                    found_words = []
                    
                    for word in sentiment_words['positive']:
                        if word in new_response.lower():
                            score += 0.3
                            found_words.append(f"✅ {word}")
                    
                    for word in sentiment_words['negative']:
                        if word in new_response.lower():
                            score -= 0.3
                            found_words.append(f"❌ {word}")
                    
                    # Determine tags
                    tags = []
                    tag_keywords = {
                        'compensation': ['salary', 'pay', 'bonus', 'compensation'],
                        'culture': ['culture', 'team', 'environment'],
                        'management': ['manager', 'leadership', 'boss'],
                        'growth': ['career', 'growth', 'learning', 'development'],
                        'work-life': ['balance', 'flexibility', 'remote', 'hours']
                    }
                    
                    for tag, keywords in tag_keywords.items():
                        for keyword in keywords:
                            if keyword in new_response.lower():
                                tags.append(tag)
                                break
                    
                    st.success("✅ Analysis Complete!")
                    
                    result_col1, result_col2 = st.columns(2)
                    with result_col1:
                        if score > 0.3:
                            st.success(f"😊 Positive ({score:.2f})")
                        elif score < -0.3:
                            st.error(f"😟 Negative ({score:.2f})")
                        else:
                            st.info(f"😐 Neutral ({score:.2f})")
                    
                    with result_col2:
                        if tags:
                            st.write("**Tags:**", ", ".join(tags))
                        if found_words:
                            st.write("**Keywords:**", ", ".join(found_words))
        
        with col2:
            # Filter data
            filtered_df = survey_df[
                (survey_df['Department'].isin(selected_depts)) &
                (survey_df['Sentiment_Label'].isin(sentiment_filter))
            ]
            
            if analysis_mode == "Sentiment Overview":
                st.markdown("#### 😊 Sentiment Distribution")
                
                # Sentiment pie chart
                sentiment_counts = filtered_df['Sentiment_Label'].value_counts()
                
                fig_pie = px.pie(
                    values=sentiment_counts.values,
                    names=sentiment_counts.index,
                    color_discrete_map={'Positive': '#2E7D32', 'Neutral': '#FFA726', 'Negative': '#C62828'},
                    title="Overall Sentiment Distribution"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                
                # Sentiment by department
                dept_sentiment = filtered_df.groupby(['Department', 'Sentiment_Label']).size().reset_index(name='Count')
                
                fig_bar = px.bar(
                    dept_sentiment,
                    x='Department',
                    y='Count',
                    color='Sentiment_Label',
                    title="Sentiment by Department",
                    color_discrete_map={'Positive': '#2E7D32', 'Neutral': '#FFA726', 'Negative': '#C62828'}
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                
            elif analysis_mode == "Theme Analysis":
                st.markdown("#### 🏷️ Response Themes")
                
                # Simulate theme extraction
                themes = ['Compensation', 'Culture', 'Management', 'Growth', 'Work-Life Balance']
                theme_counts = np.random.randint(10, 50, size=len(themes))
                
                fig_themes = px.bar(
                    x=theme_counts,
                    y=themes,
                    orientation='h',
                    title="Most Common Themes",
                    labels={'x': 'Frequency', 'y': 'Theme'},
                    color=theme_counts,
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_themes, use_container_width=True)
                
                # Word frequency
                st.markdown("**Top Keywords**")
                
                keywords = ['team', 'manager', 'work', 'culture', 'growth', 'balance', 'salary', 'development']
                keyword_freq = np.random.randint(5, 30, size=len(keywords))
                
                word_df = pd.DataFrame({
                    'Keyword': keywords,
                    'Frequency': keyword_freq
                }).sort_values('Frequency', ascending=False)
                
                fig_words = px.treemap(
                    word_df,
                    path=['Keyword'],
                    values='Frequency',
                    title="Keyword Frequency Map"
                )
                st.plotly_chart(fig_words, use_container_width=True)
                
            elif analysis_mode == "Department Comparison":
                st.markdown("#### 🏢 Department Analysis")
                
                # Average sentiment by department
                dept_avg = filtered_df.groupby('Department')['Sentiment_Score'].agg(['mean', 'std', 'count']).reset_index()
                dept_avg.columns = ['Department', 'Avg_Sentiment', 'Std_Dev', 'Response_Count']
                
                fig_comp = px.scatter(
                    dept_avg,
                    x='Avg_Sentiment',
                    y='Department',
                    size='Response_Count',
                    error_x='Std_Dev',
                    title="Department Sentiment Comparison",
                    labels={'Avg_Sentiment': 'Average Sentiment Score'},
                    color='Avg_Sentiment',
                    color_continuous_scale='RdYlGn',
                    range_color=[-1, 1]
                )
                fig_comp.add_vline(x=0, line_dash="dash", line_color="gray")
                st.plotly_chart(fig_comp, use_container_width=True)
                
                # Department details
                st.dataframe(
                    dept_avg.sort_values('Avg_Sentiment', ascending=False),
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        'Avg_Sentiment': st.column_config.ProgressColumn(
                            "Avg Sentiment",
                            min_value=-1,
                            max_value=1,
                            format="%.2f"
                        ),
                        'Std_Dev': st.column_config.NumberColumn(
                            "Std Dev",
                            format="%.2f"
                        )
                    }
                )
                
            else:  # Time Trends
                st.markdown("#### 📈 Sentiment Trends Over Time")
                
                # Group by date and calculate average sentiment
                time_trend = filtered_df.groupby([pd.Grouper(key='Date', freq='M'), 'Department'])['Sentiment_Score'].mean().reset_index()
                
                fig_trend = px.line(
                    time_trend,
                    x='Date',
                    y='Sentiment_Score',
                    color='Department',
                    title="Sentiment Trends by Department",
                    labels={'Sentiment_Score': 'Average Sentiment'},
                    markers=True
                )
                fig_trend.add_hline(y=0, line_dash="dash", line_color="gray")
                fig_trend.update_layout(hovermode='x unified')
                st.plotly_chart(fig_trend, use_container_width=True)
                
                # Volume over time
                volume_trend = filtered_df.groupby(pd.Grouper(key='Date', freq='M')).size().reset_index(name='Response_Count')
                
                fig_volume = px.area(
                    volume_trend,
                    x='Date',
                    y='Response_Count',
                    title="Response Volume Over Time",
                    labels={'Response_Count': 'Number of Responses'}
                )
                st.plotly_chart(fig_volume, use_container_width=True)
        
        with col3:
            st.markdown("#### 📊 Insights")
            
            if len(filtered_df) > 0:
                # Calculate insights
                total_responses = len(filtered_df)
                avg_sentiment = filtered_df['Sentiment_Score'].mean()
                
                # Sentiment breakdown
                sentiment_pcts = filtered_df['Sentiment_Label'].value_counts(normalize=True) * 100
                
                # Best and worst departments
                dept_sentiment = filtered_df.groupby('Department')['Sentiment_Score'].mean()
                best_dept = dept_sentiment.idxmax()
                worst_dept = dept_sentiment.idxmin()
                
                st.info(f"""
                **Summary Statistics**
                
                📝 Total Responses: {total_responses}
                
                😊 Overall Sentiment: {avg_sentiment:.2f}
                
                **Sentiment Breakdown:**
                • Positive: {sentiment_pcts.get('Positive', 0):.1f}%
                • Neutral: {sentiment_pcts.get('Neutral', 0):.1f}%
                • Negative: {sentiment_pcts.get('Negative', 0):.1f}%
                
                **Department Insights:**
                🏆 Best: {best_dept} ({dept_sentiment[best_dept]:.2f})
                ⚠️ Needs Attention: {worst_dept} ({dept_sentiment[worst_dept]:.2f})
                """)
                
                # Action items
                st.markdown("#### 🎯 Suggested Actions")
                
                if avg_sentiment < 0:
                    st.warning("⚠️ Overall sentiment is negative. Consider focus groups to understand concerns.")
                
                if sentiment_pcts.get('Negative', 0) > 30:
                    st.warning("⚠️ High negative feedback. Review common themes in negative responses.")
                
                if dept_sentiment[worst_dept] < -0.3:
                    st.warning(f"⚠️ {worst_dept} department needs immediate attention.")
                
                # Export options
                st.markdown("#### 💾 Export")
                
                export_format = st.selectbox(
                    "Format",
                    ["CSV", "Excel", "JSON"]
                )
                
                if st.button("📥 Download Results"):
                    if export_format == "CSV":
                        csv = filtered_df.to_csv(index=False)
                        st.download_button(
                            "Download CSV",
                            csv,
                            "survey_analysis.csv",
                            "text/csv"
                        )
    
    with tabs[3]:
        st.markdown("### 💡 Advanced Enhancements")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🤖 AI/ML Enhancements
            
            1. **Advanced NLP**
               - Use transformer models (BERT/RoBERTa)
               - Multi-lingual support
               - Sarcasm detection
               - Context-aware sentiment
            
            2. **Topic Modeling**
               - LDA for theme discovery
               - Dynamic topic evolution
               - Hierarchical clustering
               
            3. **Predictive Analytics**
               - Predict employee turnover risk
               - Forecast sentiment trends
               - Early warning system
            """)
            
            st.code("""
# Example: Using TextBlob for sentiment
from textblob import TextBlob

def advanced_sentiment(text):
    blob = TextBlob(text)
    
    # Get polarity (-1 to 1)
    polarity = blob.sentiment.polarity
    
    # Get subjectivity (0 to 1)
    subjectivity = blob.sentiment.subjectivity
    
    # Extract key phrases
    noun_phrases = blob.noun_phrases
    
    return {
        'polarity': polarity,
        'subjectivity': subjectivity,
        'key_phrases': noun_phrases,
        'sentiment': 'positive' if polarity > 0.1 
                    else 'negative' if polarity < -0.1 
                    else 'neutral'
    }
            """, language="python")
        
        with col2:
            st.markdown("""
            #### 📊 Visualization Enhancements
            
            1. **Interactive Dashboards**
               - Real-time updates
               - Drill-down capabilities
               - Custom date ranges
            
            2. **Advanced Charts**
               - Sentiment heatmaps
               - Network graphs for theme relationships
               - Animated time series
            
            3. **Reporting**
               - Automated weekly reports
               - Executive summaries
               - Action item tracking
            """)
            
            st.code("""
# Example: Word cloud generation
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_wordcloud(responses):
    # Combine all responses
    text = ' '.join(responses)
    
    # Generate word cloud
    wordcloud = WordCloud(
        width=800, 
        height=400,
        background_color='white',
        colormap='viridis'
    ).generate(text)
    
    # Display
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    
    return fig
            """, language="python")
        
        st.markdown("---")
        
        st.success("""
        ✅ **Module Complete!**
        
        You've learned how to build a comprehensive survey sentiment analysis tool that can:
        - Automatically analyze and tag survey responses
        - Track sentiment trends across departments and time
        - Identify key themes and patterns
        - Provide actionable insights for HR teams
        
        This tool can significantly reduce the time spent on survey analysis while providing deeper insights into employee feedback.
        """)
        
        if st.button("✅ Complete Module", type="primary"):
            st.session_state.completed_lessons.add(5)
            st.balloons()

                    
elif st.session_state.current_lesson == 6:
    # Module 6: Build Your Own App
    st.markdown("# 🚀 Module 6: Build Your Own App")
    
    st.markdown("""
    Now it's time to apply everything you've learned! This module will guide you through building 
    a complete Streamlit application for your team.
    """)
    
    tabs = st.tabs(["📋 Planning", "🏗️ Scaffold", "⚙️ Build", "🚀 Deploy"])
    
    with tabs[0]:
        st.markdown("### 📋 Plan Your Application")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Define Your App")
            
            app_name = st.text_input("App Name", "HR Analytics Dashboard")
            app_description = st.text_area(
                "App Description",
                "A comprehensive dashboard for tracking headcount, forecasting, and savings analysis.",
                height=100
            )
            
            st.markdown("#### Target Users")
            users = st.multiselect(
                "Who will use this app?",
                ["HR Partners", "Finance Team", "Department Heads", "Executives", "Data Team"],
                default=["HR Partners", "Department Heads"]
            )
            
            st.markdown("#### Key Features")
            features = st.multiselect(
                "Select core features",
                ["Real-time Metrics", "Forecasting", "Comparison Tools", "Export Reports", 
                 "Alerts", "What-if Analysis", "Historical Trends", "Budget Tracking"],
                default=["Real-time Metrics", "Forecasting", "Historical Trends"]
            )
        
        with col2:
            st.markdown("#### Data Requirements")
            
            data_sources = st.multiselect(
                "Data Sources",
                ["Snowflake Tables", "CSV Uploads", "APIs", "Manual Input"],
                default=["Snowflake Tables"]
            )
            
            update_frequency = st.selectbox(
                "Data Update Frequency",
                ["Real-time", "Hourly", "Daily", "Weekly", "Monthly"]
            )
            
            st.markdown("#### Technical Requirements")
            
            auth_required = st.checkbox("Authentication Required", value=True)
            multi_page = st.checkbox("Multi-page Application", value=True)
            export_needed = st.checkbox("Export Functionality", value=True)
            
            if st.button("Generate App Plan", type="primary"):
                st.markdown("---")
                st.markdown("### 📄 Your App Blueprint")
                
                st.json({
                    "app_name": app_name,
                    "description": app_description,
                    "users": users,
                    "features": features,
                    "data_sources": data_sources,
                    "update_frequency": update_frequency,
                    "authentication": auth_required,
                    "multi_page": multi_page,
                    "export_functionality": export_needed
                })
                
                st.session_state.user_code['app_plan'] = {
                    "app_name": app_name,
                    "features": features
                }
    
    with tabs[1]:
        st.markdown("### 🏗️ Generate App Scaffold")
        
        if 'app_plan' in st.session_state.user_code:
            plan = st.session_state.user_code['app_plan']
            
            st.markdown(f"#### Scaffold for: {plan['app_name']}")
            
            # Generate main app structure
            main_code = f"""
import streamlit as st
import pandas as pd
import numpy as np
from snowflake.snowpark.context import get_active_session
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="{plan['app_name']}",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Snowflake session
@st.cache_resource
def init_snowflake():
    return get_active_session()

session = init_snowflake()

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'

# Sidebar Navigation
with st.sidebar:
    st.title("{plan['app_name']}")
    st.markdown("---")
    
    pages = {', '.join([f'"{f}"' for f in plan['features'][:3]])}
    
    for page in pages:
        if st.button(page, use_container_width=True):
            st.session_state.current_page = page

# Main Content Router
if st.session_state.current_page == 'Dashboard':
    st.title("📊 Dashboard")
    
    # Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Headcount", "1,234", "+5.2%")
    with col2:
        st.metric("Open Positions", "45", "-12")
    with col3:
        st.metric("Monthly Savings", "$234K", "+$15K")
    with col4:
        st.metric("Budget Utilization", "78%", "+3%")
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        # Add your chart here
        st.plotly_chart(create_trend_chart(), use_container_width=True)
    
    with col2:
        # Add another chart here
        st.plotly_chart(create_distribution_chart(), use_container_width=True)

elif st.session_state.current_page == 'Forecasting':
    st.title("📈 Forecasting")
    # Add forecasting logic here

# Helper Functions
@st.cache_data(ttl=3600)
def load_data(query):
    return session.sql(query).to_pandas()

def create_trend_chart():
    # Implement your chart logic
    fig = go.Figure()
    # Add traces
    return fig

def create_distribution_chart():
    # Implement your chart logic
    fig = go.Figure()
    # Add traces
    return fig
            """
            
            st.code(main_code, language="python")
            
            # Generate requirements file
            st.markdown("#### Requirements File")
            requirements = """
streamlit==1.28.0
pandas==2.0.3
numpy==1.24.3
plotly==5.17.0
snowflake-snowpark-python==1.8.0
            """
            st.code(requirements, language="text")
            
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Download Main App",
                    main_code,
                    file_name="app.py",
                    mime="text/plain"
                )
            with col2:
                st.download_button(
                    "📥 Download Requirements",
                    requirements,
                    file_name="requirements.txt",
                    mime="text/plain"
                )
        else:
            st.info("👈 Please complete the Planning step first to generate your app scaffold.")
    
    with tabs[2]:
        st.markdown("### ⚙️ Build Your Features")
        
        st.markdown("#### Component Builder")
        
        component_type = st.selectbox(
            "Choose a component to build",
            ["Metric Cards", "Filter Panel", "Chart Section", "Data Table", "Export Function"]
        )
        
        if component_type == "Metric Cards":
            st.markdown("##### Configure Metric Cards")
            
            num_metrics = st.slider("Number of metrics", 1, 8, 4)
            show_delta = st.checkbox("Show delta/change", value=True)
            
            if st.button("Generate Code"):
                code = f"""
# Metric Cards Component
def render_metrics():
    metrics = fetch_current_metrics()
    
    cols = st.columns({num_metrics})
    
    for idx, (col, metric) in enumerate(zip(cols, metrics)):
        with col:
            {'delta = calculate_delta(metric)' if show_delta else ''}
            st.metric(
                metric['name'],
                metric['value'],
                {f"delta" if show_delta else 'None'}
            )

def fetch_current_metrics():
    query = '''
    SELECT 
        metric_name,
        current_value,
        previous_value
    FROM metrics_table
    WHERE date = CURRENT_DATE()
    '''
    return session.sql(query).to_pandas().to_dict('records')
                """
                st.code(code, language="python")
                
        elif component_type == "Filter Panel":
            st.markdown("##### Configure Filters")
            
            filter_types = st.multiselect(
                "Select filter types",
                ["Date Range", "Department", "Location", "Metric", "Employee Type"],
                default=["Date Range", "Department"]
            )
            
            if st.button("Generate Code"):
                code = """
# Filter Panel Component
def render_filters():
    with st.sidebar:
        st.markdown("### Filters")
        
        filters = {}
        """
                
                if "Date Range" in filter_types:
                    code += """
        
        # Date Range Filter
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            key="date_filter"
        )
        filters['date_range'] = date_range
        """
                
                if "Department" in filter_types:
                    code += """
        
        # Department Filter
        departments = load_departments()
        selected_dept = st.multiselect(
            "Select Departments",
            options=departments,
            default=departments[:3],
            key="dept_filter"
        )
        filters['departments'] = selected_dept
        """
                
                code += """
        
        return filters

def apply_filters(df, filters):
    filtered_df = df.copy()
    
    if 'date_range' in filters:
        start_date, end_date = filters['date_range']
        filtered_df = filtered_df[
            (filtered_df['Date'] >= start_date) & 
            (filtered_df['Date'] <= end_date)
        ]
    
    if 'departments' in filters:
        filtered_df = filtered_df[
            filtered_df['Department'].isin(filters['departments'])
        ]
    
    return filtered_df
                """
                st.code(code, language="python")
        
        elif component_type == "Export Function":
            st.markdown("##### Configure Export")
            
            export_formats = st.multiselect(
                "Export formats",
                ["CSV", "Excel", "PDF", "JSON"],
                default=["CSV", "Excel"]
            )
            
            if st.button("Generate Code"):
                code = """
import io
from datetime import datetime

def render_export_button(data, filename_prefix="export"):
    col1, col2 = st.columns([3, 1])
    
    with col2:
        export_format = st.selectbox(
            "Format",
            options=[""" + ', '.join([f'"{fmt}"' for fmt in export_formats]) + """],
            key="export_format"
        )
        
        if st.button("📥 Export Data", use_container_width=True):
            export_data(data, export_format, filename_prefix)

def export_data(data, format, prefix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}"
    """
                
                if "CSV" in export_formats:
                    code += """
    
    if format == "CSV":
        csv = data.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{filename}.csv",
            mime="text/csv"
        )
    """
                
                if "Excel" in export_formats:
                    code += """
    
    elif format == "Excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            data.to_excel(writer, index=False, sheet_name='Data')
        excel_data = output.getvalue()
        
        st.download_button(
            label="Download Excel",
            data=excel_data,
            file_name=f"{filename}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    """
                
                st.code(code, language="python")
    
    with tabs[3]:
        st.markdown("### 🚀 Deployment Guide")
        
        st.markdown("""
        #### Deploying to Streamlit in Snowflake
        
        Follow these steps to deploy your app:
        """)
        
        with st.expander("1️⃣ Prepare Your Environment"):
            st.markdown("""
            1. **Create a Snowflake Stage**:
            ```sql
            CREATE STAGE IF NOT EXISTS streamlit_apps;
            ```
            
            2. **Upload Your App Files**:
            ```sql
            PUT file://app.py @streamlit_apps AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
            PUT file://requirements.txt @streamlit_apps AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
            ```
            
            3. **Create the Streamlit App**:
            ```sql
            CREATE STREAMLIT APP hr_analytics_app
                ROOT_LOCATION = '@streamlit_apps'
                MAIN_FILE = 'app.py'
                QUERY_WAREHOUSE = 'COMPUTE_WH';
            ```
            """)
        
        with st.expander("2️⃣ Configure Permissions"):
            st.markdown("""
            ```sql
            -- Grant access to specific roles
            GRANT USAGE ON STREAMLIT APP hr_analytics_app TO ROLE analyst_role;
            GRANT USAGE ON STREAMLIT APP hr_analytics_app TO ROLE hr_role;
            
            -- Grant data access
            GRANT SELECT ON DATABASE.SCHEMA.TABLE TO STREAMLIT APP hr_analytics_app;
            ```
            """)
        
        with st.expander("3️⃣ Best Practices"):
            st.markdown("""
            ✅ **Performance**:
            - Use st.cache_data for expensive queries
            - Implement pagination for large datasets
            - Pre-aggregate data in Snowflake views
            
            ✅ **Security**:
            - Never hardcode credentials
            - Use Snowflake's role-based access
            - Validate all user inputs
            
            ✅ **Maintenance**:
            - Version control your code
            - Document your data sources
            - Create a testing environment
            
            ✅ **User Experience**:
            - Add loading indicators
            - Provide clear error messages
            - Include help text and tooltips
            """)
        
        if st.button("🎉 Complete Course!", type="primary"):
            st.session_state.completed_lessons.add(6)
            st.balloons()
            st.success("""
            Congratulations! You've completed the Streamlit in Snowflake course! 
            
            You're now ready to build powerful data applications for your team.
            """)

elif st.session_state.current_lesson == 7:
    # Resources & Best Practices
    st.markdown("# 📚 Resources & Best Practices")
    
    tabs = st.tabs(["📖 Documentation", "💡 Best Practices", "🔧 Code Snippets", "🎯 Templates"])
    
    with tabs[0]:
        st.markdown("### 📖 Essential Documentation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Streamlit Resources
            - [Streamlit Documentation](https://docs.streamlit.io)
            - [Streamlit Components](https://streamlit.io/components)
            - [Streamlit Cloud](https://streamlit.io/cloud)
            - [API Reference](https://docs.streamlit.io/library/api-reference)
            
            #### Snowflake Resources
            - [Snowflake Docs](https://docs.snowflake.com)
            - [Snowpark Python](https://docs.snowflake.com/en/developer-guide/snowpark/python/index.html)
            - [Streamlit in Snowflake](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
            """)
            
        with col2:
            st.markdown("""
            #### Useful Libraries
            - **Plotly**: Interactive visualizations
            - **Pandas**: Data manipulation
            - **NumPy**: Numerical computing
            - **Altair**: Declarative visualization
            - **AgGrid**: Advanced data tables
            
            #### Community
            - [Streamlit Forum](https://discuss.streamlit.io)
            - [GitHub Issues](https://github.com/streamlit/streamlit/issues)
            - [Snowflake Community](https://community.snowflake.com)
            """)
    
    with tabs[1]:
        st.markdown("### 💡 Best Practices")
        
        st.markdown("""
        #### 1. Performance Optimization
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success("""
            **✅ DO:**
            - Cache expensive operations
            - Use session state for user inputs
            - Implement pagination
            - Pre-aggregate in Snowflake
            - Use column configuration for tables
            """)
            
        with col2:
            st.error("""
            **❌ DON'T:**
            - Load entire datasets at once
            - Recalculate on every interaction
            - Use global variables
            - Ignore query optimization
            - Forget to clear cache when needed
            """)
        
        st.markdown("""
        #### 2. User Experience
        """)
        
        st.info("""
        - **Clear Navigation**: Use sidebar for navigation and filters
        - **Loading States**: Show progress for long operations
        - **Error Handling**: Provide helpful error messages
        - **Responsive Design**: Test on different screen sizes
        - **Documentation**: Include help text and tooltips
        """)
        
        st.markdown("""
        #### 3. Code Organization
        """)
        
        st.code("""
# Recommended project structure
my_streamlit_app/
├── app.py                 # Main application file
├── requirements.txt       # Dependencies
├── pages/                # Multi-page apps
│   ├── 1_Dashboard.py
│   ├── 2_Analytics.py
│   └── 3_Reports.py
├── utils/                # Utility functions
│   ├── data_loader.py
│   ├── charts.py
│   └── metrics.py
├── config/              # Configuration files
│   └── settings.py
└── tests/              # Test files
    └── test_app.py
        """, language="text")
    
    with tabs[2]:
        st.markdown("### 🔧 Useful Code Snippets")
        
        snippet_type = st.selectbox(
            "Select Snippet Category",
            ["Data Loading", "Caching", "Authentication", "Charts", "Tables", "Forms"]
        )
        
        if snippet_type == "Data Loading":
            st.code("""
# Efficient data loading with error handling
@st.cache_data(ttl=3600)
def load_data_safely(query, params=None):
    try:
        with st.spinner('Loading data...'):
            session = get_active_session()
            if params:
                df = session.sql(query, params).to_pandas()
            else:
                df = session.sql(query).to_pandas()
            return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Usage
data = load_data_safely(
    "SELECT * FROM table WHERE date >= :1",
    params=[start_date]
)
            """, language="python")
            
        elif snippet_type == "Caching":
            st.code("""
# Smart caching patterns
import hashlib

def get_cache_key(*args):
    \"\"\"Generate cache key from arguments\"\"\"
    return hashlib.md5(str(args).encode()).hexdigest()

@st.cache_data(ttl=3600)
def cached_query(query, filters):
    cache_key = get_cache_key(query, tuple(filters.items()))
    return load_data(query, filters)

# Clear specific cache
def clear_cache_for_query(query):
    cached_query.clear()
    st.success("Cache cleared!")

# Cache with dependencies
@st.cache_data(ttl=3600)
def load_with_dependencies(table, date):
    base_data = load_base_data(table)
    filtered_data = filter_by_date(base_data, date)
    return process_data(filtered_data)
            """, language="python")
            
        elif snippet_type == "Authentication":
            st.code("""
# Simple authentication pattern
def check_password():
    \"\"\"Returns `True` if the user had the correct password.\"\"\"

    def password_entered():
        \"\"\"Checks whether a password entered by the user is correct.\"\"\"
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if check_password():
    # Main app code here
    st.write("Welcome to the app!")
            """, language="python")
            
        elif snippet_type == "Charts":
            st.code("""
# Reusable chart functions
def create_time_series_chart(df, x_col, y_cols, title=""):
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set2
    
    for i, col in enumerate(y_cols):
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=df[col],
            mode='lines+markers',
            name=col,
            line=dict(color=colors[i % len(colors)], width=2),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title=x_col,
        yaxis_title="Value",
        hovermode='x unified',
        showlegend=True,
        height=400
    )
    
    return fig

# Animated bar chart
def create_animated_bar(df, x, y, animation_frame, title=""):
    fig = px.bar(
        df, x=x, y=y, 
        animation_frame=animation_frame,
        title=title,
        range_y=[0, df[y].max() * 1.1]
    )
    
    fig.update_layout(
        updatemenus=[{
            'buttons': [
                {'args': [None, {'frame': {'duration': 500}}],
                 'label': 'Play', 'method': 'animate'},
                {'args': [[None], {'frame': {'duration': 0}}],
                 'label': 'Pause', 'method': 'animate'}
            ]
        }]
    )
    
    return fig
            """, language="python")
    
    with tabs[3]:
        st.markdown("### 🎯 App Templates")
        
        template = st.selectbox(
            "Choose a template",
            ["HR Dashboard", "Forecasting Tool", "Report Generator", "Data Explorer"]
        )
        
        if template == "HR Dashboard":
            st.markdown("#### HR Dashboard Template")
            
            template_code = """
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from snowflake.snowpark.context import get_active_session

# Configuration
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="👥",
    layout="wide"
)

# Initialize session
session = get_active_session()

# Header
st.title("👥 HR Analytics Dashboard")
st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# Filters
col1, col2, col3, col4 = st.columns(4)
with col1:
    dept_filter = st.selectbox("Department", ["All", "Engineering", "Sales", "HR"])
with col2:
    location_filter = st.selectbox("Location", ["All", "Remote", "Office"])
with col3:
    start_date = st.date_input("From", datetime.now() - timedelta(days=30))
with col4:
    end_date = st.date_input("To", datetime.now())

# Metrics Row
st.markdown("### Key Metrics")
metric_cols = st.columns(5)

metrics = [
    ("Total Headcount", "1,234", "+45", "inverse"),
    ("Open Positions", "67", "-12", "normal"),
    ("Attrition Rate", "8.5%", "+1.2%", "inverse"),
    ("Avg Time to Fill", "42 days", "-5 days", "normal"),
    ("Budget Utilization", "78%", "+3%", "off")
]

for col, (label, value, delta, delta_color) in zip(metric_cols, metrics):
    with col:
        st.metric(label, value, delta, delta_color=delta_color)

# Charts
st.markdown("### Analytics")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Headcount trend
    st.subheader("Headcount Trend")
    # Add your chart here
    
with chart_col2:
    # Department distribution
    st.subheader("Department Distribution")
    # Add your chart here

# Detailed Table
st.markdown("### Detailed Data")
# Add your table here
            """
            
            st.code(template_code, language="python")
            
            st.download_button(
                "📥 Download Template",
                template_code,
                file_name="hr_dashboard.py",
                mime="text/plain"
            )
        
        if st.button("🎓 Complete Resources Section", type="primary"):
            st.session_state.completed_lessons.add(7)
            st.success("You've completed all modules! You're now a Streamlit in Snowflake expert! 🎉")