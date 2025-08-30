import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import io
import json
import os

def hr_data_connections_module():
    st.title("HR Data Connections in Streamlit")
    
    # Module introduction with context
    st.markdown("""
    ## Making Magic Company: People Insights
    
    Connecting to various HR data sources is essential for building effective analytics applications.
    This module covers how to load, transform, and integrate HR data from files, databases, and APIs.
    """)
    
    # Section 1: Working with HR Data Files
    st.header("1. Working with HR Data Files")
    
    # Use tabs for the learning components
    tab1, tab2, tab3 = st.tabs(["🔍 Live Example", "💻 Code", "📚 Explanation"])
    
    with tab1:
        st.subheader("Loading and Transforming HR Data")
        
        # File uploader for HR data
        st.markdown("### Upload HR Data File")
        
        uploaded_file = st.file_uploader(
            "Upload CSV or Excel file",
            type=["csv", "xlsx"],
            help="Upload your HR data file (CSV or Excel format)"
        )
        
        # Sample data option
        use_sample_data = st.checkbox("Use sample data instead", value=not uploaded_file)
        
        # Process the uploaded file or use sample data
        if uploaded_file or use_sample_data:
            # Display loading spinner
            with st.spinner("Processing data..."):
                if use_sample_data:
                    # Generate sample HR data
                    employee_data = generate_sample_hr_data()
                    file_type = "Sample Data"
                else:
                    # Determine file type and read accordingly
                    file_type = uploaded_file.name.split(".")[-1].lower()
                    
                    if file_type == "csv":
                        employee_data = pd.read_csv(uploaded_file)
                    elif file_type == "xlsx":
                        employee_data = pd.read_excel(uploaded_file)
            
            # Show basic file info
            st.markdown(f"### Data Overview: {file_type}")
            
            # Data summary
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Rows", f"{len(employee_data):,}")
            
            with col2:
                st.metric("Columns", f"{len(employee_data.columns):,}")
            
            with col3:
                # Check for potential duplicate employees
                if "employee_id" in employee_data.columns:
                    duplicates = employee_data["employee_id"].duplicated().sum()
                    st.metric("Duplicate IDs", f"{duplicates:,}")
                else:
                    st.metric("Data Fields", f"{employee_data.size:,}")
            
            # Display data
            st.markdown("### Data Preview")
            st.dataframe(employee_data.head(10), use_container_width=True)
            
            # Basic data cleaning and transformation options
            st.markdown("### Data Cleaning Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Drop nulls option
                drop_nulls = st.checkbox("Drop rows with missing values", value=False)
                
                # Fix column names
                fix_columns = st.checkbox("Standardize column names", value=True)
            
            with col2:
                # Convert date columns
                convert_dates = st.checkbox("Convert date columns", value=True)
                
                # Categorical encoding
                encode_categories = st.checkbox("Encode categorical variables", value=False)
            
            # Apply selected transformations
            if st.button("Apply Transformations"):
                with st.spinner("Transforming data..."):
                    # Make a copy of the original data
                    transformed_data = employee_data.copy()
                    
                    # Track transformations applied
                    transformations = []
                    
                    # Drop nulls if selected
                    if drop_nulls:
                        initial_rows = len(transformed_data)
                        transformed_data = transformed_data.dropna()
                        rows_dropped = initial_rows - len(transformed_data)
                        transformations.append(f"Dropped {rows_dropped} rows with missing values")
                    
                    # Fix column names if selected
                    if fix_columns:
                        # Convert to lowercase, replace spaces with underscores
                        transformed_data.columns = [col.lower().replace(" ", "_") for col in transformed_data.columns]
                        transformations.append("Standardized column names to lowercase with underscores")
                    
                    # Convert date columns if selected
                    if convert_dates:
                        # Identify potential date columns
                        date_cols = []
                        for col in transformed_data.columns:
                            if any(date_term in col.lower() for date_term in ["date", "birth", "hire", "start", "end"]):
                                try:
                                    transformed_data[col] = pd.to_datetime(transformed_data[col])
                                    date_cols.append(col)
                                except:
                                    pass  # Skip if conversion fails
                        
                        if date_cols:
                            transformations.append(f"Converted {len(date_cols)} columns to datetime: {', '.join(date_cols)}")
                    
                    # Encode categorical variables if selected
                    if encode_categories:
                        # Identify categorical columns (object type with few unique values)
                        cat_cols = []
                        for col in transformed_data.select_dtypes(include=["object"]).columns:
                            if transformed_data[col].nunique() < 10:  # Arbitrary threshold for categorical
                                # Create dummies
                                dummies = pd.get_dummies(transformed_data[col], prefix=col)
                                # Add dummies to dataframe
                                transformed_data = pd.concat([transformed_data, dummies], axis=1)
                                cat_cols.append(col)
                        
                        if cat_cols:
                            transformations.append(f"Created dummy variables for {len(cat_cols)} categorical columns")
                    
                    # Display transformation summary
                    if transformations:
                        st.success(f"Applied {len(transformations)} transformations:")
                        for i, transform in enumerate(transformations):
                            st.markdown(f"{i+1}. {transform}")
                        
                        # Show transformed data
                        st.markdown("### Transformed Data")
                        st.dataframe(transformed_data.head(10), use_container_width=True)
                        
                        # Option to download transformed data
                        transformed_csv = transformed_data.to_csv(index=False)
                        st.download_button(
                            label="Download Transformed Data",
                            data=transformed_csv,
                            file_name="transformed_hr_data.csv",
                            mime="text/csv"
                        )
                    else:
                        st.info("No transformations selected or applied.")
    
    with tab2:
        # Store code snippets in variables
        file_loading_code = """
# File uploader for HR data
uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"],
    help="Upload your HR data file (CSV or Excel format)"
)

# Process the uploaded file
if uploaded_file:
    # Determine file type and read accordingly
    file_type = uploaded_file.name.split(".")[-1].lower()
    
    if file_type == "csv":
        employee_data = pd.read_csv(uploaded_file)
    elif file_type == "xlsx":
        employee_data = pd.read_excel(uploaded_file)
    
    # Show basic file info
    st.markdown(f"### Data Overview: {file_type}")
    
    # Data summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Rows", f"{len(employee_data):,}")
    
    with col2:
        st.metric("Columns", f"{len(employee_data.columns):,}")
    
    with col3:
        # Check for potential duplicate employees
        if "employee_id" in employee_data.columns:
            duplicates = employee_data["employee_id"].duplicated().sum()
            st.metric("Duplicate IDs", f"{duplicates:,}")
"""
        
        data_transformation_code = """
# Apply selected transformations
if st.button("Apply Transformations"):
    with st.spinner("Transforming data..."):
        # Make a copy of the original data
        transformed_data = employee_data.copy()
        
        # Track transformations applied
        transformations = []
        
        # Drop nulls if selected
        if drop_nulls:
            initial_rows = len(transformed_data)
            transformed_data = transformed_data.dropna()
            rows_dropped = initial_rows - len(transformed_data)
            transformations.append(f"Dropped {rows_dropped} rows with missing values")
        
        # Fix column names if selected
        if fix_columns:
            # Convert to lowercase, replace spaces with underscores
            transformed_data.columns = [col.lower().replace(" ", "_") for col in transformed_data.columns]
            transformations.append("Standardized column names to lowercase with underscores")
        
        # Convert date columns if selected
        if convert_dates:
            # Identify potential date columns
            date_cols = []
            for col in transformed_data.columns:
                if any(date_term in col.lower() for date_term in ["date", "birth", "hire", "start", "end"]):
                    try:
                        transformed_data[col] = pd.to_datetime(transformed_data[col])
                        date_cols.append(col)
                    except:
                        pass  # Skip if conversion fails
            
            if date_cols:
                transformations.append(f"Converted {len(date_cols)} columns to datetime: {', '.join(date_cols)}")
"""
        
        sample_data_code = """
# Function to generate sample HR data
def generate_sample_hr_data(rows=100):
    np.random.seed(42)
    
    # Employee IDs
    employee_ids = np.arange(1001, 1001 + rows)
    
    # Departments
    departments = ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance', 'Operations']
    dept_weights = [0.3, 0.15, 0.2, 0.1, 0.15, 0.1]
    
    # Job levels
    job_levels = ['Entry', 'Associate', 'Senior', 'Manager', 'Director']
    level_weights = [0.2, 0.3, 0.3, 0.15, 0.05]
    
    # Locations
    locations = ['New York', 'San Francisco', 'Chicago', 'Remote']
    
    # Generate data
    today = datetime.datetime.now().date()
    
    data = {
        'employee_id': employee_ids,
        'department': np.random.choice(departments, size=rows, p=dept_weights),
        'job_level': np.random.choice(job_levels, size=rows, p=level_weights),
        'location': np.random.choice(locations, size=rows),
        'hire_date': [today - datetime.timedelta(days=np.random.randint(1, 3650)) for _ in range(rows)],
        'salary': np.random.normal(80000, 30000, size=rows).astype(int),
        'bonus_pct': np.random.uniform(0.05, 0.25, size=rows).round(2),
        'performance_score': np.random.randint(1, 6, size=rows)
    }
    
    return pd.DataFrame(data)
"""
        
        # Display code snippets
        st.subheader("File Loading Code")
        st.code(file_loading_code)
        
        st.subheader("Data Transformation Code")
        st.code(data_transformation_code)
        
        st.subheader("Sample Data Generation Code")
        st.code(sample_data_code)
    
    with tab3:
        st.subheader("HR Data File Best Practices")
        
        with st.expander("HR Data File Types", expanded=True):
            st.markdown("""
            **Common HR Data File Formats:**
            
            1. **CSV (Comma-Separated Values)**
               - Simple, universal format
               - Easy to create from most HR systems
               - Readable by virtually all data tools
               - Best for tabular data without complex formatting
               - Load with `pd.read_csv()`
            
            2. **Excel (XLSX)**
               - Common in HR departments
               - Supports multiple sheets and formatting
               - Good for reports with calculations
               - Can contain macros (be cautious)
               - Load with `pd.read_excel()`
            
            3. **JSON**
               - Hierarchical data structure
               - Common format for API responses
               - Good for nested data (e.g., employee with benefits)
               - More verbose than CSV
               - Load with `pd.read_json()` or `json.loads()`
            
            4. **Parquet**
               - Columnar storage format
               - Excellent compression
               - Fast for analytical queries
               - Good for large HR datasets
               - Load with `pd.read_parquet()`
            
            5. **Database Exports**
               - Direct exports from HRIS systems
               - May come in proprietary formats
               - Often require special connectors
               - Can be large and comprehensive
            """)
            
        with st.expander("Data Cleaning for HR Analytics"):
            st.markdown("""
            **Essential HR Data Cleaning Steps:**
            
            1. **Standardize Column Names**
               - Convert to lowercase for consistency
               - Replace spaces with underscores
               - Standardize naming conventions
               - Example: `EMPLOYEE NAME` → `employee_name`
            
            2. **Handle Missing Values**
               - Identify causes of missing data
               - For employee data, missing values often require investigation
               - Consider business rules for imputation
               - Document missing value strategy
            
            3. **Date Standardization**
               - Convert all dates to datetime format
               - Handle different date formats (US vs. international)
               - Check for impossible dates
               - Calculate derived fields (tenure, age, etc.)
            
            4. **Categorical Encoding**
               - Standardize categories (e.g., "Eng." vs. "Engineering")
               - Create dummy variables for analysis
               - Consider hierarchical categories (job levels)
               - Ensure categories are consistent over time
            
            5. **Outlier Detection**
               - Check for salary outliers
               - Validate hire dates and birthdates
               - Investigate extreme performance ratings
               - Use business context to interpret outliers
            """)
            
        with st.expander("Data Quality Considerations"):
            st.markdown("""
            **HR Data Quality Checks:**
            
            1. **Uniqueness Constraints**
               - Verify unique employee IDs
               - Check for duplicate records
               - Validate email uniqueness
               - Ensure one active record per employee
            
            2. **Referential Integrity**
               - Validate manager IDs exist in employee table
               - Ensure departments exist in department table
               - Check that job codes are valid
               - Verify location codes match location master data
            
            3. **Business Rule Validation**
               - Hire date before termination date
               - Age within reasonable range
               - Salary within range for job level
               - Performance ratings within valid scale
            
            4. **Temporal Consistency**
               - Check for anachronisms (future dates)
               - Validate historical records
               - Ensure consistent time periods
               - Check sequence of career events
            
            5. **Documentation**
               - Record all data cleaning steps
               - Document data quality issues
               - Track changes to original data
               - Maintain data dictionary
            """)
    
    # Add a divider between sections
    st.divider()
    
    # Section 2: Database Connections
    st.header("2. Database Connections")
    
    # Use tabs for the learning components
    tab1, tab2, tab3 = st.tabs(["🔍 Live Example", "💻 Code", "📚 Explanation"])
    
    with tab1:
        st.subheader("Connecting to HR Databases")
        
        # Database connection simulation
        st.markdown("""
        ### HR Database Connection
        
        In a real application, you would connect to your HR database system
        (e.g., Workday, SAP SuccessFactors, or a custom HRIS). This example
        simulates a database connection to demonstrate the concepts.
        """)
        
        # Database type selection
        db_type = st.selectbox(
            "Select Database Type",
            options=["PostgreSQL", "MySQL", "Snowflake", "SQL Server", "Oracle"]
        )
        
        # Connection form
        with st.form("db_connection_form"):
            st.markdown(f"### {db_type} Connection Parameters")
            
            col1, col2 = st.columns(2)
            
            with col1:
                host = st.text_input("Host", value="hr-database.makingmagic.com")
                port = st.text_input("Port", value=get_default_port(db_type))
                database = st.text_input("Database", value="hr_analytics")
            
            with col2:
                username = st.text_input("Username", value="hr_analyst")
                password = st.text_input("Password", value="••••••••", type="password")
                use_ssl = st.checkbox("Use SSL", value=True)
            
            # Connection string display
            connection_string = generate_connection_string(db_type, host, port, database, username)
            st.code(connection_string)
            
            # Submit button
            connect_button = st.form_submit_button("Connect")
        
        # Simulate connection
        if connect_button:
            with st.spinner(f"Connecting to {db_type} database..."):
                # Simulate connection delay
                time.sleep(1.5)
                
                # Simulate successful connection
                st.success(f"Connected to {database} on {host}")
                
                # Show available tables
                st.markdown("### Available HR Tables")
                
                # Display simulated tables
                hr_tables = [
                    {"name": "employees", "rows": 1452, "last_updated": "2025-07-15"},
                    {"name": "departments", "rows": 18, "last_updated": "2025-06-30"},
                    {"name": "job_levels", "rows": 12, "last_updated": "2025-04-10"},
                    {"name": "compensation_history", "rows": 4328, "last_updated": "2025-08-01"},
                    {"name": "performance_ratings", "rows": 3945, "last_updated": "2025-07-31"},
                    {"name": "benefits_enrollment", "rows": 1380, "last_updated": "2025-08-05"}
                ]
                
                tables_df = pd.DataFrame(hr_tables)
                st.dataframe(tables_df, use_container_width=True)
                
                # Sample query section
                st.markdown("### Run SQL Query")
                
                query = st.text_area(
                    "Enter SQL Query",
                    value="""SELECT d.department_name, 
       COUNT(e.employee_id) as headcount,
       AVG(e.salary) as avg_salary,
       SUM(e.salary) as total_compensation
FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE e.status = 'Active'
GROUP BY d.department_name
ORDER BY headcount DESC;""",
                    height=150
                )
                
                # Execute query button
                if st.button("Execute Query"):
                    with st.spinner("Executing query..."):
                        # Simulate query execution
                        time.sleep(2)
                        
                        # Generate mock query results
                        mock_results = generate_mock_query_results(query)
                        
                        # Display results
                        st.markdown("### Query Results")
                        st.dataframe(mock_results, use_container_width=True)
                        
                        # Download option
                        csv = mock_results.to_csv(index=False)
                        st.download_button(
                            label="Download Results as CSV",
                            data=csv,
                            file_name="query_results.csv",
                            mime="text/csv"
                        )
    
    with tab2:
        # Store code snippets in variables
        db_connection_code = """
# PostgreSQL connection example
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# Connection parameters
host = "hr-database.makingmagic.com"
port = "5432"
database = "hr_analytics"
username = "hr_analyst"
password = "your_password"  # Use secure methods for passwords in production

# Method 1: Using psycopg2 directly
def query_hr_data_psycopg2(query):
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=username,
            password=password,
            port=port
        )
        
        # Create a cursor
        cur = conn.cursor()
        
        # Execute the query
        cur.execute(query)
        
        # Fetch the results
        columns = [desc[0] for desc in cur.description]
        results = cur.fetchall()
        
        # Create a DataFrame
        df = pd.DataFrame(results, columns=columns)
        
        # Close the cursor
        cur.close()
        
        return df
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return None
    
    finally:
        if conn is not None:
            conn.close()

# Method 2: Using SQLAlchemy (easier with pandas)
def query_hr_data_sqlalchemy(query):
    try:
        # Create SQLAlchemy engine
        engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')
        
        # Execute query directly with pandas
        df = pd.read_sql(query, engine)
        
        return df
    
    except Exception as error:
        print(f"Error: {error}")
        return None
"""
        
        snowflake_connection_code = """
# Snowflake connection example
import snowflake.connector
import pandas as pd

# Connection parameters
account = "makingmagic"
user = "hr_analyst"
password = "your_password"  # Use secure methods for passwords in production
warehouse = "HR_WAREHOUSE"
database = "HR_ANALYTICS"
schema = "PUBLIC"

def query_snowflake_data(query):
    conn = None
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            user=user,
            password=password,
            account=account,
            warehouse=warehouse,
            database=database,
            schema=schema
        )
        
        # Execute query
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Fetch results
        results = cursor.fetchall()
        
        # Get column names
        column_names = [desc[0] for desc in cursor.description]
        
        # Create DataFrame
        df = pd.DataFrame(results, columns=column_names)
        
        # Close cursor and connection
        cursor.close()
        
        return df
    
    except Exception as error:
        print(f"Error: {error}")
        return None
    
    finally:
        if conn:
            conn.close()
"""
        
        connection_pooling_code = """
# Connection pooling for better performance
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Create a connection pool
def create_connection_pool(db_url, pool_size=5, max_overflow=10):
    engine = create_engine(
        db_url,
        poolclass=QueuePool,
        pool_size=pool_size,          # Initial pool size
        max_overflow=max_overflow,    # Maximum overflow connections
        pool_timeout=30,              # Timeout in seconds
        pool_recycle=1800             # Recycle connections after 30 minutes
    )
    return engine

# Example usage in Streamlit
if "db_engine" not in st.session_state:
    db_url = f'postgresql://{username}:{password}@{host}:{port}/{database}'
    st.session_state.db_engine = create_connection_pool(db_url)

# Use the connection pool for queries
def run_query(query):
    try:
        with st.session_state.db_engine.connect() as conn:
            df = pd.read_sql(query, conn)
            return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return None
"""
        
        # Display code snippets
        st.subheader("PostgreSQL Connection Code")
        st.code(db_connection_code)
        
        st.subheader("Snowflake Connection Code")
        st.code(snowflake_connection_code)
        
        st.subheader("Connection Pooling Code")
        st.code(connection_pooling_code)
    
    with tab3:
        st.subheader("Database Connection Best Practices")
        
        with st.expander("HR Database Systems", expanded=True):
            st.markdown("""
            **Common HR Database Systems:**
            
            1. **HRIS Databases**
               - Workday: API-driven, module-based system
               - SAP SuccessFactors: Comprehensive HR suite
               - Oracle HCM: Enterprise-level HR system
               - ADP: Payroll and HR database
               - BambooHR: SMB-focused HR database
            
            2. **Database Types**
               - PostgreSQL: Open-source, robust for analytics
               - MySQL: Common in smaller HR systems
               - Snowflake: Cloud data warehouse, good for HR analytics
               - SQL Server: Common in enterprise environments
               - Oracle: Enterprise-grade for large HR systems
            
            3. **Data Warehouse Options**
               - Snowflake: Popular cloud data warehouse
               - BigQuery: Google's serverless data warehouse
               - Redshift: AWS data warehouse
               - Azure Synapse: Microsoft's analytics service
               - Databricks: Unified analytics platform
            
            4. **Connection Methods**
               - Direct database connection
               - API integrations
               - ODBC/JDBC connections
               - ETL pipelines (Airflow, dbt)
               - Data replication services
            """)
            
        with st.expander("Security and Compliance"):
            st.markdown("""
            **HR Data Security Best Practices:**
            
            1. **Secure Connection Handling**
               - Never hardcode credentials in applications
               - Use environment variables or secrets management
               - Implement connection pooling
               - Encrypt all connections (SSL/TLS)
               - Rotate credentials regularly
            
            2. **Authentication Options**
               - Username/password (basic)
               - IAM roles (AWS)
               - OAuth 2.0 (for API connections)
               - Key-based authentication
               - SSO integration
            
            3. **Access Control**
               - Use least privilege principles
               - Create read-only analytics users
               - Implement row-level security for HR data
               - Use database views to restrict sensitive data
               - Audit all database access
            
            4. **Compliance Considerations**
               - GDPR requirements for employee data
               - SOC 2 compliance for data handling
               - HIPAA for benefits and health data
               - Data residency requirements
               - Data retention policies
            
            5. **Data Masking and Anonymization**
               - Mask PII in development environments
               - Hash employee IDs for analytics
               - Aggregate sensitive data when possible
               - Implement anonymization for reporting
               - Create secure data extracts
            """)
            
        with st.expander("Query Optimization"):
            st.markdown("""
            **SQL Query Optimization for HR Analytics:**
            
            1. **Performance Considerations**
               - Use appropriate indexes on employee_id, department_id
               - Limit the columns you SELECT
               - Filter early in the query (WHERE before JOIN)
               - Be cautious with wildcard (*) selections
               - Use EXPLAIN to analyze query plans
            
            2. **Common HR SQL Patterns**
               - Point-in-time analysis using effective dating
               - Hierarchical queries for org structure
               - Window functions for compensation analysis
               - Self-joins for manager relationships
               - Conditional aggregation for demographics
            
            3. **Advanced Techniques**
               - Materialized views for common HR metrics
               - Partitioning by date for historical analysis
               - Query parameterization for reusability
               - CTEs for complex HR hierarchies
               - Stored procedures for standard HR reports
            
            4. **Streamlit-Specific Approaches**
               - Cache database connections
               - Use st.cache_data for query results
               - Implement pagination for large result sets
               - Consider asynchronous queries for long-running reports
               - Add progress indicators for complex queries
            """)
    
    # Add a divider between sections
    st.divider()
    
    # Section 3: API Connections
    st.header("3. API Connections")
    
    # Use tabs for the learning components
    tab1, tab2, tab3 = st.tabs(["🔍 Live Example", "💻 Code", "📚 Explanation"])
    
    with tab1:
        st.subheader("Connecting to HR APIs")
        
        # HR API selection
        st.markdown("### HR System API Integration")
        
        api_system = st.selectbox(
            "Select HR System",
            options=["Workday", "SAP SuccessFactors", "BambooHR", "ADP", "Custom HRIS"]
        )
        
        # API endpoint configuration
        st.markdown(f"### {api_system} API Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            api_url = st.text_input(
                "API Base URL",
                value=f"https://api.{api_system.lower().replace(' ', '')}.com/v2"
            )
            
            auth_method = st.radio(
                "Authentication Method",
                options=["OAuth 2.0", "API Key", "Basic Auth"],
                horizontal=True
            )
        
        with col2:
            if auth_method == "OAuth 2.0":
                client_id = st.text_input("Client ID", value="making_magic_hr_analytics")
                client_secret = st.text_input("Client Secret", value="••••••••••••••••", type="password")
            elif auth_method == "API Key":
                api_key = st.text_input("API Key", value="••••••••••••••••", type="password")
            else:  # Basic Auth
                username = st.text_input("Username", value="api_user")
                password = st.text_input("Password", value="••••••••", type="password")
        
        # API endpoints
        st.markdown("### Available API Endpoints")
        
        # Display simulated endpoints
        endpoints = [
            {"endpoint": "/employees", "method": "GET", "description": "Retrieve employee data"},
            {"endpoint": "/employees/{id}", "method": "GET", "description": "Get specific employee"},
            {"endpoint": "/departments", "method": "GET", "description": "List all departments"},
            {"endpoint": "/reports/headcount", "method": "GET", "description": "Get headcount reports"},
            {"endpoint": "/compensation", "method": "GET", "description": "Retrieve compensation data"},
            {"endpoint": "/time-off", "method": "GET", "description": "Get time-off requests"}
        ]
        
        endpoints_df = pd.DataFrame(endpoints)
        st.dataframe(endpoints_df, use_container_width=True)
        
        # API request builder
        st.markdown("### API Request Builder")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_endpoint = st.selectbox(
                "Select Endpoint",
                options=[endpoint["endpoint"] for endpoint in endpoints]
            )
        
        with col2:
            http_method = st.selectbox(
                "HTTP Method",
                options=["GET", "POST", "PUT", "DELETE"],
                index=0
            )
        
        # Request parameters
        st.markdown("#### Request Parameters")
        
        param_cols = st.columns(3)
        
        with param_cols[0]:
            include_inactive = st.checkbox("Include Inactive", value=False)
        
        with param_cols[1]:
            limit = st.number_input("Result Limit", min_value=10, max_value=1000, value=100, step=10)
        
        with param_cols[2]:
            format_type = st.selectbox("Response Format", options=["JSON", "XML"], index=0)
        
        # Generate the request URL
        request_url = f"{api_url}{selected_endpoint}"
        params = []
        
        if include_inactive:
            params.append("include_inactive=true")
        
        params.append(f"limit={limit}")
        params.append(f"format={format_type.lower()}")
        
        if params:
            request_url += "?" + "&".join(params)
        
        # Display the request
        st.markdown("#### API Request")
        st.code(f"{http_method} {request_url}")
        
        # Headers
        headers = {}
        
        if auth_method == "OAuth 2.0":
            headers["Authorization"] = "Bearer {access_token}"
        elif auth_method == "API Key":
            headers["X-API-Key"] = "{api_key}"
        
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        
        # Display headers
        st.markdown("#### Request Headers")
        st.code(json.dumps(headers, indent=2))
        
        # Execute request button
        if st.button("Execute API Request"):
            with st.spinner(f"Sending request to {api_system} API..."):
                # Simulate API request delay
                time.sleep(1.5)
                
                # Generate mock response based on endpoint
                mock_response = generate_mock_api_response(selected_endpoint, include_inactive, limit)
                
                # Display the response
                st.markdown("#### API Response")
                st.json(mock_response)
                
                # Convert to DataFrame if it's a list of objects
                if isinstance(mock_response, dict) and "data" in mock_response and isinstance(mock_response["data"], list):
                    try:
                        response_df = pd.json_normalize(mock_response["data"])
                        
                        st.markdown("#### Response as Table")
                        st.dataframe(response_df, use_container_width=True)
                        
                        # Download option
                        csv = response_df.to_csv(index=False)
                        st.download_button(
                            label="Download as CSV",
                            data=csv,
                            file_name=f"{selected_endpoint.replace('/', '_')}_data.csv",
                            mime="text/csv"
                        )
                    except:
                        st.warning("Could not convert response to table format.")
    
    with tab2:
        # Store code snippets in variables
        api_request_code = """
# Making API requests to HR systems
import requests
import pandas as pd
import json

# API configuration
api_url = "https://api.workday.com/v2"
endpoint = "/employees"

# Authentication parameters
client_id = "your_client_id"
client_secret = "your_client_secret"  # Use secure methods in production

# Step 1: Get OAuth token (if using OAuth)
def get_oauth_token(client_id, client_secret):
    token_url = "https://api.workday.com/oauth2/token"
    
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get token: {response.status_code}, {response.text}")

# Step 2: Make the API request
def get_employee_data(access_token, include_inactive=False, limit=100):
    # Build the URL with parameters
    request_url = f"{api_url}{endpoint}"
    
    params = {
        "limit": limit,
        "format": "json"
    }
    
    if include_inactive:
        params["include_inactive"] = "true"
    
    # Set up headers with authentication
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Make the request
    response = requests.get(request_url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed: {response.status_code}, {response.text}")

# Step 3: Process the API response
def process_employee_data(api_response):
    # Extract the data from the response
    employees = api_response.get("data", [])
    
    # Convert to DataFrame
    df = pd.json_normalize(employees)
    
    return df

# Full process in Streamlit
def fetch_hr_data():
    with st.spinner("Authenticating..."):
        try:
            access_token = get_oauth_token(client_id, client_secret)
            
            with st.spinner("Fetching employee data..."):
                employee_data = get_employee_data(access_token)
                df = process_employee_data(employee_data)
                
                return df
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return None
"""
        
        pagination_code = """
# Handling pagination in HR API responses
def fetch_all_pages(endpoint, access_token, page_size=100):
    # Fetch all pages of results from a paginated API endpoint
    all_results = []
    page = 1
    total_pages = None
    
    while total_pages is None or page <= total_pages:
        # Progress indicator for Streamlit
        if total_pages:
            progress = page / total_pages
            st.progress(progress)
            st.text(f"Fetching page {page} of {total_pages}...")
        else:
            st.text(f"Fetching page {page}...")
        
        # Make request with pagination parameters
        params = {
            "page": page,
            "limit": page_size
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        response = requests.get(endpoint, headers=headers, params=params)
        
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}, {response.text}")
        
        data = response.json()
        
        # Extract results for this page
        results = data.get("data", [])
        all_results.extend(results)
        
        # Update pagination info
        if total_pages is None:
            total_pages = data.get("meta", {}).get("total_pages", 1)
        
        # Move to next page
        page += 1
        
        # Break if this API doesn't support pagination or we've reached the end
        if "meta" not in data or "total_pages" not in data["meta"]:
            break
    
    return all_results
"""
        
        webhook_code = """
# Setting up a webhook receiver for HR system events
from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib
import json

app = FastAPI()

# Webhook secret (store securely in production)
WEBHOOK_SECRET = "your_webhook_secret"

@app.post("/webhooks/hr-events")
async def hr_webhook(request: Request):
    # Get the raw request body
    body = await request.body()
    
    # Verify the webhook signature (if supported by your HR system)
    signature = request.headers.get("X-Webhook-Signature")
    
    if signature:
        computed_signature = hmac.new(
            WEBHOOK_SECRET.encode('utf-8'),
            body,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, computed_signature):
            raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Parse the webhook payload
    try:
        event_data = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # Handle different HR event types
    event_type = event_data.get("event_type")
    
    if event_type == "employee.hired":
        # Handle new employee event
        process_new_employee(event_data)
    elif event_type == "employee.terminated":
        # Handle employee termination
        process_termination(event_data)
    elif event_type == "employee.updated":
        # Handle employee data update
        process_employee_update(event_data)
    
    # Acknowledge receipt
    return {"status": "success", "message": f"Processed {event_type} event"}

def process_new_employee(event_data):
    # Add employee to your analytics database
    # Update headcount metrics
    # Send welcome notification
    pass

# Run with: uvicorn webhook_receiver:app --reload
"""
        
        # Display code snippets
        st.subheader("API Request Code")
        st.code(api_request_code)
        
        st.subheader("Pagination Handling Code")
        st.code(pagination_code)
        
        st.subheader("Webhook Receiver Code")
        st.code(webhook_code)
    
    with tab3:
        st.subheader("HR API Integration Best Practices")
        
        with st.expander("API Integration Strategies", expanded=True):
            st.markdown("""
            **HR API Integration Approaches:**
            
            1. **Data Access Patterns**
               - Real-time vs. batch processing
               - Pull model (your app requests data)
               - Push model (webhooks for events)
               - Change data capture
               - Full vs. incremental data syncs
            
            2. **Authentication Methods**
               - OAuth 2.0 (most modern HR systems)
               - API keys (simpler but less secure)
               - Basic authentication (older systems)
               - JWT (JSON Web Tokens)
               - SSO integration
            
            3. **Data Transformation**
               - Handle different date formats
               - Normalize nested JSON structures
               - Map fields to your data model
               - Convert codes to human-readable values
               - Handle multi-value fields
            
            4. **Error Handling**
               - Implement retries with backoff
               - Log detailed error information
               - Handle rate limiting gracefully
               - Validate responses before processing
               - Monitor API uptime and performance
            """)
            
        with st.expander("Common HR APIs"):
            st.markdown("""
            **Popular HR System APIs:**
            
            1. **Workday API**
               - RESTful API structure
               - OAuth 2.0 authentication
               - Comprehensive HR data access
               - Well-documented endpoints
               - Strong security model
            
            2. **SAP SuccessFactors API**
               - OData protocol
               - Multiple authentication options
               - Module-based endpoints
               - Complex data structures
               - Enterprise-grade security
            
            3. **BambooHR API**
               - Simple REST API
               - API key authentication
               - Good for small/mid-size companies
               - Webhook support
               - File upload/download capabilities
            
            4. **ADP Workforce Now API**
               - REST-based architecture
               - OAuth 2.0 with certificate
               - Focus on payroll and benefits
               - Strict rate limiting
               - Detailed documentation
            
            5. **Custom HRIS Systems**
               - Vary widely in implementation
               - May use older SOAP protocols
               - Often require custom integration
               - May have limited documentation
               - Consider middleware solutions
            """)
            
        with st.expander("Streamlit-Specific API Techniques"):
            st.markdown("""
            **Optimizing API Usage in Streamlit:**
            
            1. **Caching API Responses**
               - Use `@st.cache_data` for API response caching
               - Set appropriate TTL (Time To Live)
               - Cache transformations separately
               - Handle cache invalidation
               - Monitor cache hit rates
            
            2. **Managing API Keys**
               - Use Streamlit secrets management
               - Never hardcode credentials
               - Implement key rotation
               - Consider service accounts
               - Log access for auditing
            
            3. **Performance Optimization**
               - Implement pagination for large datasets
               - Use background jobs for heavy processing
               - Display loading indicators
               - Limit request frequency
               - Consider local data caching
            
            4. **Error Handling for Users**
               - Show user-friendly error messages
               - Implement graceful fallbacks
               - Provide retry options
               - Log detailed errors for debugging
               - Monitor failure rates
            
            5. **State Management**
               - Use session state for API contexts
               - Maintain authentication tokens
               - Track API request history
               - Implement undo/redo capabilities
               - Handle session expiration
            """)
    
    # Add a practical challenge
    st.divider()
    st.header("🧩 Practice Challenge")
    
    challenge_description = """
    **Challenge**: Create a Data Pipeline for HR Analytics
    
    Build a simple data pipeline that:
    
    1. Loads HR data from a file or mock API
    2. Transforms the data (e.g., calculate tenure, standardize departments)
    3. Creates basic HR metrics (headcount, turnover rate, etc.)
    4. Displays the results in a dashboard
    
    Bonus: Add data validation to identify potential data quality issues.
    """
    
    st.info(challenge_description)
    
    # Provide a hint
    with st.expander("See Hint"):
        hint_code = """
# HR Data Pipeline Example

# Step 1: Load data (file or API)
def load_hr_data():
    # Option to use sample data or upload
    use_sample = st.checkbox("Use sample data", value=True)
    
    if use_sample:
        # Generate sample data
        df = generate_sample_hr_data(200)
    else:
        # File uploader
        uploaded_file = st.file_uploader("Upload HR data", type=["csv", "xlsx"])
        
        if uploaded_file:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        else:
            st.warning("Please upload a file or use sample data")
            return None
    
    return df

# Step 2: Transform data
def transform_hr_data(df):
    # Make a copy to avoid modifying the original
    transformed_df = df.copy()
    
    # Calculate tenure in years
    if "hire_date" in transformed_df.columns:
        transformed_df["hire_date"] = pd.to_datetime(transformed_df["hire_date"])
        today = pd.Timestamp.today().normalize()
        transformed_df["tenure_years"] = ((today - transformed_df["hire_date"]).dt.days / 365.25).round(1)
    
    # Standardize department names
    if "department" in transformed_df.columns:
        # Example mapping for inconsistent departments
        dept_mapping = {
            "Eng": "Engineering",
            "Engineering": "Engineering",
            "R&D": "Engineering",
            "Sales": "Sales",
            "Sales & Marketing": "Sales",
            "Marketing": "Marketing",
            "HR": "Human Resources",
            "Human Resources": "Human Resources",
            "Finance": "Finance",
            "Accounting": "Finance",
            "Ops": "Operations",
            "Operations": "Operations"
        }
        
        transformed_df["department_standardized"] = transformed_df["department"].map(dept_mapping)
    
    return transformed_df

# Step 3: Calculate HR metrics
def calculate_hr_metrics(df):
    metrics = {}
    
    # Total headcount
    metrics["total_headcount"] = len(df)
    
    # Headcount by department
    if "department_standardized" in df.columns:
        dept_counts = df["department_standardized"].value_counts()
        metrics["department_headcount"] = dept_counts.to_dict()
    
    # Average tenure
    if "tenure_years" in df.columns:
        metrics["avg_tenure"] = df["tenure_years"].mean()
    
    # Turnover calculation (if status column exists)
    if "status" in df.columns:
        active = df[df["status"] == "Active"].shape[0]
        terminated = df[df["status"] == "Terminated"].shape[0]
        
        if active + terminated > 0:
            metrics["turnover_rate"] = terminated / (active + terminated) * 100
    
    return metrics

# Step 4: Display results
def display_hr_dashboard(df, metrics):
    st.header("HR Analytics Dashboard")
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Headcount", metrics["total_headcount"])
    
    with col2:
        if "avg_tenure" in metrics:
            st.metric("Avg. Tenure (Years)", f"{metrics['avg_tenure']:.1f}")
    
    with col3:
        if "turnover_rate" in metrics:
            st.metric("Turnover Rate", f"{metrics['turnover_rate']:.1f}%")
    
    # Department breakdown
    if "department_headcount" in metrics:
        st.subheader("Headcount by Department")
        
        dept_df = pd.DataFrame({
            "Department": list(metrics["department_headcount"].keys()),
            "Headcount": list(metrics["department_headcount"].values())
        })
        
        st.bar_chart(dept_df.set_index("Department"))
    
    # Other visualizations as needed...

# Main pipeline
df = load_hr_data()

if df is not None:
    with st.spinner("Processing data..."):
        transformed_df = transform_hr_data(df)
        metrics = calculate_hr_metrics(transformed_df)
        
        display_hr_dashboard(transformed_df, metrics)
"""
        st.code(hint_code)
    
    # Next steps
    st.divider()
    st.markdown("**Next Module**: [HR Analytics Capstone](placeholder)")

# Helper functions

# Function to generate sample HR data
def generate_sample_hr_data(rows=100):
    np.random.seed(42)
    
    # Employee IDs
    employee_ids = np.arange(1001, 1001 + rows)
    
    # Departments
    departments = ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance', 'Operations']
    dept_weights = [0.3, 0.15, 0.2, 0.1, 0.15, 0.1]
    
    # Job levels
    job_levels = ['Entry', 'Associate', 'Senior', 'Manager', 'Director']
    level_weights = [0.2, 0.3, 0.3, 0.15, 0.05]
    
    # Locations
    locations = ['New York', 'San Francisco', 'Chicago', 'Remote']
    
    # Generate data
    today = datetime.datetime.now().date()
    
    data = {
        'employee_id': employee_ids,
        'department': np.random.choice(departments, size=rows, p=dept_weights),
        'job_level': np.random.choice(job_levels, size=rows, p=level_weights),
        'location': np.random.choice(locations, size=rows),
        'hire_date': [today - datetime.timedelta(days=np.random.randint(1, 3650)) for _ in range(rows)],
        'salary': np.random.normal(80000, 30000, size=rows).astype(int),
        'bonus_pct': np.random.uniform(0.05, 0.25, size=rows).round(2),
        'performance_score': np.random.randint(1, 6, size=rows)
    }
    
    return pd.DataFrame(data)

# Helper functions for database section
def get_default_port(db_type):
    ports = {
        "PostgreSQL": "5432",
        "MySQL": "3306",
        "Snowflake": "443",
        "SQL Server": "1433",
        "Oracle": "1521"
    }
    return ports.get(db_type, "")

def generate_connection_string(db_type, host, port, database, username):
    if db_type == "PostgreSQL":
        return f"postgresql://{username}:password@{host}:{port}/{database}"
    elif db_type == "MySQL":
        return f"mysql://{username}:password@{host}:{port}/{database}"
    elif db_type == "Snowflake":
        account = host.split('.')[0]
        return f"snowflake://{username}:password@{account}/{database}"
    elif db_type == "SQL Server":
        return f"mssql+pyodbc://{username}:password@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    elif db_type == "Oracle":
        return f"oracle://{username}:password@{host}:{port}/{database}"
    else:
        return ""

def generate_mock_query_results(query):
    # Very simple query parser to generate mock data
    # This is just for demonstration purposes
    
    # Default mock data
    mock_data = {
        "department_name": ["Engineering", "Sales", "Marketing", "HR", "Finance", "Operations"],
        "headcount": [523, 342, 156, 48, 87, 296],
        "avg_salary": [112500, 98700, 94200, 88500, 106800, 78900],
        "total_compensation": [58837500, 33755400, 14695200, 4248000, 9291600, 23356400]
    }
    
    # Create basic dataframe
    df = pd.DataFrame(mock_data)
    
    # Check for specific query patterns
    if "ORDER BY headcount DESC" in query:
        df = df.sort_values("headcount", ascending=False)
    
    if "WHERE" in query and "Active" in query:
        # Simulate filtering to only active employees
        df["headcount"] = (df["headcount"] * 0.92).astype(int)
        df["total_compensation"] = (df["headcount"] * df["avg_salary"]).astype(int)
    
    return df

# Helper function for API section
def generate_mock_api_response(endpoint, include_inactive, limit):
    # Generate mock data based on the endpoint
    if endpoint == "/employees":
        data = []
        status_options = ["Active"] if not include_inactive else ["Active", "Terminated", "On Leave"]
        
        # Generate a limited number of employee records
        for i in range(min(limit, 100)):
            employee = {
                "id": f"EMP{1001 + i}",
                "first_name": f"Employee{i}First",
                "last_name": f"Employee{i}Last",
                "email": f"employee{i}@makingmagic.com",
                "department": np.random.choice(["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations"]),
                "job_title": f"Job Title {i}",
                "status": np.random.choice(status_options, p=[0.85, 0.1, 0.05] if include_inactive else [1.0])
            }
            data.append(employee)
        
        return {
            "meta": {
                "total": limit,
                "page": 1,
                "per_page": limit,
                "total_pages": 1
            },
            "data": data
        }
    
    elif endpoint == "/departments":
        return {
            "meta": {
                "total": 6,
                "page": 1,
                "per_page": limit,
                "total_pages": 1
            },
            "data": [
                {"id": "DEP1", "name": "Engineering", "manager_id": "EMP1050", "employee_count": 523},
                {"id": "DEP2", "name": "Marketing", "manager_id": "EMP1025", "employee_count": 156},
                {"id": "DEP3", "name": "Sales", "manager_id": "EMP1010", "employee_count": 342},
                {"id": "DEP4", "name": "HR", "manager_id": "EMP1015", "employee_count": 48},
                {"id": "DEP5", "name": "Finance", "manager_id": "EMP1020", "employee_count": 87},
                {"id": "DEP6", "name": "Operations", "manager_id": "EMP1030", "employee_count": 296}
            ]
        }
    
    elif endpoint == "/reports/headcount":
        return {
            "meta": {
                "report_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "total_headcount": 1452,
                "active_headcount": 1380
            },
            "data": [
                {"department": "Engineering", "headcount": 523, "percentage": 36.0},
                {"department": "Marketing", "headcount": 156, "percentage": 10.8},
                {"department": "Sales", "headcount": 342, "percentage": 23.6},
                {"department": "HR", "headcount": 48, "percentage": 3.3},
                {"department": "Finance", "headcount": 87, "percentage": 6.0},
                {"department": "Operations", "headcount": 296, "percentage": 20.4}
            ]
        }
    
    else:
        # Generic response for other endpoints
        return {
            "meta": {
                "endpoint": endpoint,
                "status": "success",
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            },
            "data": [
                {"message": f"Mock data for {endpoint.replace('/', ' ').strip()}"}
            ]
        }