import streamlit as st
import pandas as pd
import numpy as np
import time

def deployment_module():
    st.title("Deploying HR Analytics in Snowflake")
    
    st.markdown("""
    ## Streamlit in Snowflake Deployment Guide
    
    This guide will help you deploy your HR analytics applications directly in Snowflake,
    allowing seamless integration with your HR data warehouse.
    """)
    
    # Create tabs for deployment sections
    tab1, tab2, tab3, tab4 = st.tabs(["🚀 Deployment Steps", "🔐 Security & Access", "⚙️ Best Practices", "📊 Examples"])
    
    with tab1:
        st.header("Deploying Your HR Analytics App")
        
        st.subheader("1️⃣ Prepare Your Environment")
        
        # Create stage
        st.code("""
CREATE STAGE IF NOT EXISTS hr_analytics_stage;
        """, language="sql")
        
        # Upload files
        with st.expander("Upload Your App Files", expanded=True):
            st.code("""
-- Upload main application file
PUT file://hr_app.py @hr_analytics_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

-- Upload module files
PUT file://hr_data_module.py @hr_analytics_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://hr_visualizations_module.py @hr_analytics_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://hr_filters_module.py @hr_analytics_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://hr_forms_module.py @hr_analytics_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://hr_data_connections_module.py @hr_analytics_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://hr_capstone_module.py @hr_analytics_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://deployment_module.py @hr_analytics_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

-- Upload dependencies
PUT file://requirements.txt @hr_analytics_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
            """, language="sql")
        
        # Create app
        with st.expander("Create the Streamlit App", expanded=True):
            st.code("""
CREATE STREAMLIT APP hr_analytics_app
    ROOT_LOCATION = '@hr_analytics_stage'
    MAIN_FILE = 'hr_app.py'
    QUERY_WAREHOUSE = 'ANALYTICS_WH';
            """, language="sql")
        
        st.subheader("2️⃣ Configure Permissions")
        
        # Grant access
        st.code("""
-- Grant access to specific roles
GRANT USAGE ON STREAMLIT APP hr_analytics_app TO ROLE HR_ANALYST;
GRANT USAGE ON STREAMLIT APP hr_analytics_app TO ROLE HR_BUSINESS_PARTNER;
GRANT USAGE ON STREAMLIT APP hr_analytics_app TO ROLE PEOPLE_MANAGER;

-- Grant data access
GRANT SELECT ON DATABASE.HR_DATA.EMPLOYEES TO STREAMLIT APP hr_analytics_app;
GRANT SELECT ON DATABASE.HR_DATA.DEPARTMENTS TO STREAMLIT APP hr_analytics_app;
GRANT SELECT ON DATABASE.HR_DATA.COMPENSATION TO STREAMLIT APP hr_analytics_app;
GRANT SELECT ON DATABASE.HR_DATA.PERFORMANCE TO STREAMLIT APP hr_analytics_app;
        """, language="sql")
        
        st.subheader("3️⃣ Update and Maintain")
        
        # Update code
        with st.expander("Update Your App"):
            st.code("""
-- Update application files
PUT file://hr_app.py @hr_analytics_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
PUT file://hr_data_module.py @hr_analytics_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

-- No need to recreate the app - changes are applied automatically
            """, language="sql")
        
        # Testing in dev
        with st.expander("Development Workflow"):
            st.markdown("""
            **Recommended Development Workflow:**
            
            1. Create a development version of your app:
            ```sql
            CREATE STREAMLIT APP hr_analytics_app_dev
                ROOT_LOCATION = '@hr_analytics_stage_dev'
                MAIN_FILE = 'hr_app.py'
                QUERY_WAREHOUSE = 'DEV_WH';
            ```
            
            2. Test changes in the development app
            3. Once verified, promote to production:
            ```sql
            PUT file://hr_app.py @hr_analytics_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
            ```
            """)
    
    with tab2:
        st.header("Security & Access Control")
        
        st.subheader("Role-Based Access Control")
        
        # Example RBAC setup
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Role Hierarchy")
            
            roles_df = pd.DataFrame({
                "Role": ["ACCOUNTADMIN", "SYSADMIN", "HR_ADMIN", "HR_ANALYST", "HR_BUSINESS_PARTNER", "PEOPLE_MANAGER"],
                "Access Level": ["Full Admin", "System Admin", "HR Data Admin", "HR Analyst", "HR Business Partner", "Manager Self-Service"],
                "Can Deploy Apps": ["✅", "✅", "✅", "❌", "❌", "❌"],
                "Can View Sensitive Data": ["✅", "✅", "✅", "✅", "⚠️ Limited", "❌"]
            })
            
            st.dataframe(roles_df, use_container_width=True)
        
        with col2:
            st.markdown("### Data Access Patterns")
            
            # Show a simple diagram of data access patterns
            st.markdown("""
            ```
            ACCOUNTADMIN
            └── SYSADMIN
                └── HR_ADMIN
                    ├── HR_ANALYST
                    │   └── (All HR Data)
                    ├── HR_BUSINESS_PARTNER
                    │   └── (Department-specific)
                    └── PEOPLE_MANAGER
                        └── (Team-specific)
            ```
            """)
        
        st.subheader("Row-Level Security")
        
        # Row-level security example
        with st.expander("Implementing Row-Level Security", expanded=True):
            st.code("""
-- Create a secure view with row-level security
CREATE OR REPLACE SECURE VIEW HR_DATA.EMPLOYEE_SECURE AS
SELECT 
    e.*
FROM 
    HR_DATA.EMPLOYEES e
WHERE
    -- Analysts can see all records
    CURRENT_ROLE() = 'HR_ANALYST'
    
    -- Business partners can only see their business units
    OR (CURRENT_ROLE() = 'HR_BUSINESS_PARTNER' AND e.BUSINESS_UNIT IN 
        (SELECT BUSINESS_UNIT FROM HR_DATA.BUSINESS_PARTNER_ASSIGNMENTS WHERE PARTNER_ID = CURRENT_USER()))
    
    -- Managers can only see their direct/indirect reports
    OR (CURRENT_ROLE() = 'PEOPLE_MANAGER' AND e.EMPLOYEE_ID IN 
        (SELECT EMPLOYEE_ID FROM HR_DATA.REPORTING_HIERARCHY WHERE MANAGER_ID = CURRENT_USER()));

-- Grant access to the secure view
GRANT SELECT ON HR_DATA.EMPLOYEE_SECURE TO ROLE HR_ANALYST;
GRANT SELECT ON HR_DATA.EMPLOYEE_SECURE TO ROLE HR_BUSINESS_PARTNER;
GRANT SELECT ON HR_DATA.EMPLOYEE_SECURE TO ROLE PEOPLE_MANAGER;
            """, language="sql")
        
        st.subheader("Data Masking")
        
        # Data masking example
        with st.expander("Data Masking for Sensitive HR Data"):
            st.code("""
-- Create a masking policy for salary data
CREATE OR REPLACE MASKING POLICY HR_DATA.SALARY_MASK AS
    (val NUMBER) RETURNS NUMBER ->
    CASE
        WHEN CURRENT_ROLE() IN ('HR_ADMIN', 'HR_ANALYST') THEN val
        WHEN CURRENT_ROLE() = 'HR_BUSINESS_PARTNER' THEN 
            -- Business partners see salary ranges, not exact values
            CASE
                WHEN val < 50000 THEN 50000
                WHEN val BETWEEN 50000 AND 100000 THEN 75000
                WHEN val BETWEEN 100000 AND 150000 THEN 125000
                ELSE 150000
            END
        ELSE NULL
    END;

-- Apply the masking policy
ALTER TABLE HR_DATA.EMPLOYEES MODIFY COLUMN SALARY SET MASKING POLICY HR_DATA.SALARY_MASK;
            """, language="sql")
    
    with tab3:
        st.header("Best Practices for HR Analytics in Snowflake")
        
        # Performance best practices
        st.subheader("⚡ Performance Optimization")
        
        performance_tips = [
            {
                "Tip": "Use st.cache_data for expensive queries",
                "Example": """
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_employee_data():
    return conn.query("SELECT * FROM HR_DATA.EMPLOYEE_SECURE")
                """
            },
            {
                "Tip": "Pre-aggregate data in Snowflake views",
                "Example": """
CREATE OR REPLACE VIEW HR_DATA.DEPARTMENT_METRICS AS
SELECT
    DEPARTMENT,
    COUNT(*) AS HEADCOUNT,
    AVG(SALARY) AS AVG_SALARY,
    AVG(TENURE_YEARS) AS AVG_TENURE,
    SUM(CASE WHEN PERFORMANCE_RATING >= 4 THEN 1 ELSE 0 END) / COUNT(*) AS HIGH_PERFORMER_RATIO
FROM HR_DATA.EMPLOYEES
GROUP BY DEPARTMENT;
                """
            },
            {
                "Tip": "Implement pagination for large datasets",
                "Example": """
page_size = 100
page_number = st.number_input("Page", min_value=1, value=1)
offset = (page_number - 1) * page_size

query = f\"\"\"
SELECT * FROM HR_DATA.EMPLOYEES
LIMIT {page_size} OFFSET {offset}
\"\"\"
                """
            }
        ]
        
        for i, tip in enumerate(performance_tips):
            with st.expander(f"{i+1}. {tip['Tip']}", expanded=i==0):
                st.code(tip['Example'])
        
        # Security best practices
        st.subheader("🔒 Security Best Practices")
        
        security_tips = [
            {
                "Tip": "Use Snowflake's native authentication",
                "Example": """
# Let Snowflake handle authentication
# No need to manage credentials in the app
from snowflake.snowpark.context import get_active_session

# Get the current session
session = get_active_session()
                """
            },
            {
                "Tip": "Validate all user inputs",
                "Example": """
# Never use raw user input in queries
department = st.selectbox("Department", ["Sales", "Marketing", "Engineering"])

# Use parameterized queries
query = "SELECT * FROM HR_DATA.EMPLOYEES WHERE DEPARTMENT = ?"
df = session.sql(query, params=[department]).collect()
                """
            },
            {
                "Tip": "Use secure views for data access",
                "Example": """
# In Snowflake:
CREATE SECURE VIEW HR_DATA.EMPLOYEE_METRICS AS
SELECT
    DEPARTMENT,
    JOB_LEVEL,
    COUNT(*) AS EMPLOYEE_COUNT,
    AVG(SALARY) AS AVG_SALARY
FROM HR_DATA.EMPLOYEES
GROUP BY DEPARTMENT, JOB_LEVEL;

# In Streamlit:
df = session.table("HR_DATA.EMPLOYEE_METRICS").collect()
                """
            }
        ]
        
        for i, tip in enumerate(security_tips):
            with st.expander(f"{i+1}. {tip['Tip']}", expanded=i==0):
                st.code(tip['Example'])
        
        # UX best practices
        st.subheader("🎨 User Experience Best Practices")
        
        ux_tips = [
            {
                "Tip": "Add loading indicators",
                "Example": """
with st.spinner("Loading employee data..."):
    employee_data = load_employee_data()
    
# For longer operations, use progress bars
progress_bar = st.progress(0)
for i in range(100):
    # Perform long operation in steps
    time.sleep(0.01)
    progress_bar.progress(i + 1)
                """
            },
            {
                "Tip": "Provide clear error messages",
                "Example": """
try:
    data = run_complex_query()
except Exception as e:
    st.error(f"Unable to load data: {str(e)}")
    st.info("Please try selecting a different department or contact the HR Analytics team for assistance.")
                """
            },
            {
                "Tip": "Include help text and tooltips",
                "Example": """
st.selectbox(
    "Select Attrition Risk Metric",
    options=["Predicted Attrition", "Flight Risk Score", "Retention Index"],
    help="Predicted Attrition uses machine learning to forecast probability of leaving within 6 months."
)
                """
            }
        ]
        
        for i, tip in enumerate(ux_tips):
            with st.expander(f"{i+1}. {tip['Tip']}", expanded=i==0):
                st.code(tip['Example'])
    
    with tab4:
        st.header("HR Analytics in Snowflake Examples")
        
        # Show example screenshots and descriptions
        st.subheader("Example 1: HR Headcount Dashboard")
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.image("https://streamlit.io/images/brand/examples/app-analytics-dashboard.png", caption="Headcount Dashboard")
        
        with col2:
            st.markdown("""
            **HR Headcount Dashboard**
            
            This dashboard provides real-time visibility into employee headcount metrics across departments, locations, and job levels.
            
            **Key Features:**
            - Direct Snowflake integration with HR data
            - Role-based access control for HR teams
            - Interactive filters using Streamlit widgets
            - Automatic updates using scheduled Snowflake tasks
            
            **Example Query:**
            ```sql
            SELECT 
                DEPARTMENT,
                COUNT(*) AS HEADCOUNT,
                SUM(SALARY) AS TOTAL_COMPENSATION
            FROM HR_DATA.EMPLOYEES
            WHERE ACTIVE = TRUE
            GROUP BY DEPARTMENT
            ORDER BY HEADCOUNT DESC;
            ```
            """)
        
        st.divider()
        
        st.subheader("Example 2: Attrition Prediction Dashboard")
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.image("https://streamlit.io/images/brand/examples/app-finance.png", caption="Attrition Analytics")
        
        with col2:
            st.markdown("""
            **Attrition Prediction Dashboard**
            
            This app leverages machine learning models deployed in Snowflake to predict employee attrition risk.
            
            **Key Features:**
            - ML model scoring using Snowpark Python
            - Dynamic risk scoring with weekly updates
            - Drill-down analysis for at-risk employees
            - Scenario planning tools for retention strategies
            
            **Example Integration:**
            ```python
            # Using Snowpark for model predictions
            from snowflake.snowpark.functions import call_udf
            
            # Call the ML model UDF in Snowflake
            session.table("HR_DATA.EMPLOYEES") \
                .with_column("ATTRITION_RISK", 
                            call_udf("HR_MODELS.PREDICT_ATTRITION", 
                                    col("TENURE"), 
                                    col("PERFORMANCE_RATING"),
                                    col("COMPENSATION_RATIO"))) \
                .collect()
            ```
            """)
        
        st.divider()
        
        st.subheader("Example 3: Compensation Analytics")
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.image("https://streamlit.io/images/brand/examples/app-survey-dashboard.png", caption="Compensation Analytics")
        
        with col2:
            st.markdown("""
            **Compensation Analytics Dashboard**
            
            This dashboard provides compensation analysis tools with robust security controls for sensitive data.
            
            **Key Features:**
            - Granular data masking based on user roles
            - Market comparison using external data sources
            - Pay equity analysis tools
            - Budget scenario planning
            
            **Security Implementation:**
            ```sql
            -- Row-level security with dynamic data masking
            CREATE OR REPLACE ROW ACCESS POLICY HR_DATA.COMP_RAP AS
                (DEPARTMENT VARCHAR) RETURNS BOOLEAN ->
                CURRENT_ROLE() = 'HR_ADMIN'
                OR 
                (CURRENT_ROLE() = 'HR_BUSINESS_PARTNER' AND 
                DEPARTMENT IN (SELECT DEPARTMENT FROM HR_DATA.BP_ASSIGNMENTS 
                               WHERE EMAIL = CURRENT_USER()));
            
            -- Apply the policy
            ALTER TABLE HR_DATA.COMPENSATION ADD ROW ACCESS POLICY HR_DATA.COMP_RAP ON (DEPARTMENT);
            ```
            """)
    
    # Call to action
    st.divider()
    st.success("""
    **Ready to deploy your HR analytics app in Snowflake?**
    
    Contact the Data Engineering team to set up your development environment and get started!
    """)

# Additional function to generate SQL code for a given use case
def generate_sample_sql(use_case):
    if use_case == "headcount":
        return """
SELECT 
    d.DEPARTMENT_NAME,
    l.LOCATION_NAME,
    COUNT(*) AS HEADCOUNT,
    SUM(CASE WHEN DATEDIFF('DAY', e.HIRE_DATE, CURRENT_DATE()) < 90 THEN 1 ELSE 0 END) AS NEW_HIRES,
    AVG(DATEDIFF('YEAR', e.HIRE_DATE, CURRENT_DATE())) AS AVG_TENURE
FROM 
    HR_DATA.EMPLOYEES e
JOIN 
    HR_DATA.DEPARTMENTS d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
JOIN 
    HR_DATA.LOCATIONS l ON e.LOCATION_ID = l.LOCATION_ID
WHERE 
    e.STATUS = 'ACTIVE'
GROUP BY 
    d.DEPARTMENT_NAME, l.LOCATION_NAME
ORDER BY 
    HEADCOUNT DESC;
"""
    elif use_case == "attrition":
        return """
-- Calculate attrition rate by department
WITH attrition AS (
    SELECT
        d.DEPARTMENT_NAME,
        COUNT(CASE WHEN e.STATUS = 'ACTIVE' THEN 1 END) AS ACTIVE_EMPLOYEES,
        COUNT(CASE WHEN e.STATUS = 'TERMINATED' AND e.TERMINATION_DATE >= DATEADD('MONTH', -12, CURRENT_DATE()) THEN 1 END) AS TERMINATIONS_12M
    FROM
        HR_DATA.EMPLOYEES e
    JOIN
        HR_DATA.DEPARTMENTS d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
    GROUP BY
        d.DEPARTMENT_NAME
)

SELECT
    DEPARTMENT_NAME,
    ACTIVE_EMPLOYEES,
    TERMINATIONS_12M,
    ROUND(TERMINATIONS_12M / (ACTIVE_EMPLOYEES + TERMINATIONS_12M) * 100, 2) AS ATTRITION_RATE_PERCENT
FROM
    attrition
ORDER BY
    ATTRITION_RATE_PERCENT DESC;
"""
    elif use_case == "compensation":
        return """
-- Compensation ratio analysis by job level and department
WITH market_data AS (
    SELECT
        JOB_LEVEL,
        AVG(SALARY) AS MARKET_MEDIAN
    FROM
        EXTERNAL_DATA.COMPENSATION_SURVEY
    WHERE
        SURVEY_YEAR = YEAR(CURRENT_DATE())
    GROUP BY
        JOB_LEVEL
)

SELECT
    d.DEPARTMENT_NAME,
    e.JOB_LEVEL,
    COUNT(*) AS EMPLOYEE_COUNT,
    ROUND(AVG(e.SALARY), 0) AS AVG_SALARY,
    ROUND(m.MARKET_MEDIAN, 0) AS MARKET_MEDIAN,
    ROUND(AVG(e.SALARY) / m.MARKET_MEDIAN * 100, 1) AS COMP_RATIO
FROM
    HR_DATA.EMPLOYEES e
JOIN
    HR_DATA.DEPARTMENTS d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
JOIN
    market_data m ON e.JOB_LEVEL = m.JOB_LEVEL
WHERE
    e.STATUS = 'ACTIVE'
GROUP BY
    d.DEPARTMENT_NAME, e.JOB_LEVEL, m.MARKET_MEDIAN
ORDER BY
    d.DEPARTMENT_NAME, e.JOB_LEVEL;
"""
    else:
        return "-- Select a use case to see sample SQL"