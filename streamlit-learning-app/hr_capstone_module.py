# Enhanced hr_capstone_module.py with Custom Solutions Builder
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json


def hr_capstone_module():
    st.title("HR Analytics Capstone: Building Integrated Solutions")
    
    # Module introduction with enhanced context
    st.markdown("""
    ## Making Magic Company: People Insights Platform
    
    This comprehensive HR Analytics platform demonstrates the power of Streamlit in Snowflake for building 
    enterprise-grade people analytics solutions. Explore pre-built dashboards and learn to create custom 
    applications that leverage real-time data integration.
    """)
    
    # Enhanced setup
    st.set_page_config = lambda **kwargs: None
    
    # Load sample data (keeping existing function)
    @st.cache_data
    def load_sample_hr_data():
        return generate_employee_data(), generate_recruitment_data(), generate_turnover_data()
    
    employee_df, recruitment_df, turnover_df = load_sample_hr_data()
    
    # Enhanced navigation with new Custom Solutions section
    dashboard_section = st.selectbox(
        "Select Module",
        ["Platform Overview", "Talent Acquisition", "Employee Retention", "Diversity & Inclusion", "Custom Solutions Builder", "Enterprise Deployment"],
        key="main_nav"
    )
    
    # Global filters in main area
    st.markdown("### Global Filters")

    # Create columns for horizontal layout
    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        departments = sorted(employee_df['department'].unique())
        selected_departments = st.multiselect(
            "Department",
            options=departments,
            default=departments
        )

    with filter_col2:
        locations = sorted(employee_df['location'].unique())
        selected_locations = st.multiselect(
            "Location",
            options=locations,
            default=locations
        )

    with filter_col3:
        current_year = datetime.datetime.now().year
        date_range = st.slider(
            "Date Range",
            min_value=current_year-3,
            max_value=current_year,
            value=(current_year-1, current_year)
        )

    # Add a divider before the dashboard content
    st.divider()
    
    # Apply filters
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
    
    # Route to appropriate dashboard
    if dashboard_section == "Platform Overview":
        display_enhanced_overview_dashboard(filtered_employees, filtered_recruitment, filtered_turnover)
    elif dashboard_section == "Talent Acquisition":
        display_talent_acquisition_dashboard(filtered_recruitment)
    elif dashboard_section == "Employee Retention":
        display_employee_retention_dashboard(filtered_employees, filtered_turnover)
    elif dashboard_section == "Diversity & Inclusion":
        display_diversity_dashboard(filtered_employees)
    elif dashboard_section == "Custom Solutions Builder":
        display_custom_solutions_builder(filtered_employees, filtered_recruitment, filtered_turnover)
    elif dashboard_section == "Enterprise Deployment":
        display_enterprise_deployment_guide()

def display_enhanced_overview_dashboard(employees, recruitment, turnover):
    """Enhanced overview with portfolio highlights"""
    
    
    st.header("HR Analytics Platform Overview")
    
    # Real-time integration callout
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### Platform Capabilities Showcase")
    with col2:
        st.success("🔄 Real-time Data")
        st.caption(f"Last updated: {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    # Enhanced metrics with business context
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        headcount = len(employees)
        st.metric(
            "Total Workforce", 
            f"{headcount:,}",
            delta=f"+{len(recruitment[recruitment['status'] == 'Hired']) - len(turnover)}",
            help="Real-time headcount with net change calculation"
        )
    
    with col2:
        avg_tenure = employees['tenure_years'].mean()
        st.metric(
            "Avg. Tenure", 
            f"{avg_tenure:.1f} years",
            help="Rolling average tenure across all active employees"
        )
    
    with col3:
        retention_rate = 100 - (len(turnover) / headcount * 100) if headcount > 0 else 0
        st.metric(
            "Retention Rate", 
            f"{retention_rate:.1f}%",
            delta=f"{retention_rate - 90:.1f}%" if retention_rate != 90 else None,
            delta_color="normal",
            help="Annual retention rate with benchmark comparison"
        )
    
    with col4:
        cost_savings = recruitment[recruitment['status'] == 'Hired']['cost'].sum() / 1000 if len(recruitment) > 0 else 0
        st.metric(
            "Recruitment Efficiency", 
            f"${cost_savings:.0f}K",
            help="Total recruitment investment with cost-per-hire optimization"
        )
    
    # Platform features demonstration
    st.markdown("### Platform Architecture Showcase")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Real-time Data Pipeline")
        
        # Simulate real-time data flow
        pipeline_data = pd.DataFrame({
            'Layer': ['Source Systems', 'Snowflake DW', 'Streamlit App', 'Business Users'],
            'Status': ['✅ Connected', '✅ Processing', '✅ Live', '✅ Insights'],
            'Latency': ['< 1 min', '< 30 sec', 'Real-time', 'Interactive']
        })
        
        st.dataframe(
            pipeline_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                'Status': st.column_config.TextColumn('Status', width='medium'),
                'Latency': st.column_config.TextColumn('Data Latency', width='medium')
            }
        )
        
        st.code("""
# Real-time Snowflake Integration
from snowflake.snowpark.context import get_active_session

@st.cache_data(ttl=60)  # 1-minute refresh
def get_live_metrics():
    session = get_active_session()
    return session.sql('''
        SELECT 
            COUNT(*) as headcount,
            AVG(tenure_years) as avg_tenure,
            SUM(CASE WHEN status='active' THEN 1 ELSE 0 END) / COUNT(*) as retention_rate
        FROM HR_WAREHOUSE.EMPLOYEE_FACTS 
        WHERE effective_date = CURRENT_DATE()
    ''').to_pandas()
        """, language="python")
    
    with col2:
        st.markdown("#### Interactive Visualization Engine")
        
        # Demo the headcount trend
        dept_counts = employees.groupby('department').size().reset_index(name='count')
        
        fig = px.treemap(
            dept_counts,
            path=['department'],
            values='count',
            title='Workforce Distribution - Interactive Treemap',
            color='count',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        
    # Business value demonstration
    st.markdown("### Business Impact Metrics")
    
    impact_col1, impact_col2, impact_col3, impact_col4 = st.columns(4)
    
    with impact_col1:
        st.metric("Time Saved", "15 hrs/week", help="Automated reporting eliminates manual data compilation")
    with impact_col2:
        st.metric("Decision Speed", "3x faster", help="Real-time insights enable rapid decision making")
    with impact_col3:
        st.metric("Data Accuracy", "99.8%", help="Single source of truth eliminates data discrepancies")
    with impact_col4:
        st.metric("User Adoption", "94%", help="Intuitive interface drives high engagement")

def display_custom_solutions_builder(employees, recruitment, turnover):
    """Custom Solutions Builder - Portfolio Showcase"""
    
    st.header("Custom HR Solutions Builder")
    
    # Portfolio introduction
    st.markdown("""
    ### Build Enterprise-Grade HR Applications
    
    This interactive builder demonstrates how to rapidly prototype and deploy custom HR analytics solutions 
    using Streamlit in Snowflake. Each solution leverages real-time data integration and can be deployed 
    enterprise-wide in minutes.
    """)
    
    # Showcase real-time capabilities
    st.info("""
    💡 **Portfolio Highlight**: All solutions built here automatically inherit real-time Snowflake integration, 
    role-based security, and enterprise scalability. No additional infrastructure required.
    """)
    
    tabs = st.tabs(["Solution Gallery", "Custom Builder", "Integration Showcase", "Deployment Ready"])
    
    with tabs[0]:
        st.markdown("### Pre-Built Solution Templates")
        
        # Solution gallery with business context
        solutions = [
            {
                "name": "Executive Dashboard",
                "description": "C-suite ready metrics with drill-down capabilities",
                "use_case": "Board presentations, executive reviews",
                "complexity": "Enterprise",
                "build_time": "2 hours"
            },
            {
                "name": "Workforce Planning Tool",
                "description": "Predictive analytics for headcount forecasting",
                "use_case": "Budget planning, scenario modeling",
                "complexity": "Advanced",
                "build_time": "4 hours"
            },
            {
                "name": "Manager Self-Service Portal",
                "description": "Team analytics for people managers",
                "use_case": "Span of control, team insights",
                "complexity": "Standard",
                "build_time": "1 hour"
            },
            {
                "name": "Compensation Analysis Suite",
                "description": "Pay equity and market analysis tools",
                "use_case": "Compensation reviews, equity audits",
                "complexity": "Enterprise",
                "build_time": "6 hours"
            }
        ]
        
        for i, solution in enumerate(solutions):
            with st.expander(f"{solution['name']} - {solution['complexity']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Description**: {solution['description']}")
                    st.markdown(f"**Use Case**: {solution['use_case']}")
                    
                with col2:
                    st.metric("Build Time", solution['build_time'])
                    st.metric("Complexity", solution['complexity'])
                
                if st.button(f"Generate {solution['name']}", key=f"generate_{i}"):
                    generate_solution_code(solution['name'])
    
    with tabs[1]:
        st.markdown("### Interactive Solution Builder")
        
        # Enhanced builder with business focus
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Solution Configuration")
            
            solution_name = st.text_input("Solution Name", "Custom HR Analytics")
            
            business_objective = st.selectbox(
                "Primary Business Objective",
                ["Cost Optimization", "Talent Retention", "Workforce Planning", "Performance Management", "Compliance Reporting"]
            )
            
            target_users = st.multiselect(
                "Target User Groups",
                ["CHRO", "HR Partners", "People Managers", "Finance", "Department Heads"],
                default=["HR Partners"]
            )
            
            data_sources = st.multiselect(
                "Data Integration Points",
                ["HRIS System", "Payroll", "Performance Reviews", "Survey Data", "Financial Systems"],
                default=["HRIS System"]
            )
            
            analytics_features = st.multiselect(
                "Analytics Capabilities",
                ["Real-time Dashboards", "Predictive Modeling", "Trend Analysis", "Comparative Benchmarking", "Automated Alerts"],
                default=["Real-time Dashboards"]
            )
            
            deployment_scope = st.radio(
                "Deployment Scope",
                ["Pilot (Single Department)", "Division-wide", "Enterprise Global"]
            )
            
        with col2:
            st.markdown("#### Solution Preview")
            
            if st.button("Generate Solution Architecture", type="primary"):
                # Create comprehensive solution overview
                st.markdown(f"### {solution_name}")
                st.markdown(f"**Business Objective**: {business_objective}")
                
                # Technical architecture
                st.markdown("#### Technical Architecture")
                
                architecture_code = f"""
# {solution_name} - Enterprise Solution
import streamlit as st
from snowflake.snowpark.context import get_active_session
import plotly.express as px

# Enterprise Configuration
st.set_page_config(
    page_title="{solution_name}",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Snowflake Integration
@st.cache_resource
def init_snowflake_session():
    return get_active_session()

session = init_snowflake_session()

# Role-based Access Control
def check_user_permissions():
    current_role = session.get_current_role()
    authorized_roles = {', '.join([f'"{role}"' for role in target_users])}
    return current_role in authorized_roles

if not check_user_permissions():
    st.error("Access denied. Contact IT for role assignment.")
    st.stop()

# Main Application
def main():
    st.title("{solution_name}")
    st.markdown("**Objective**: {business_objective}")
    
    # Real-time Data Pipeline
    @st.cache_data(ttl=300)  # 5-minute refresh for {deployment_scope.lower()} deployment
    def load_hr_data():
        query = '''
        SELECT * FROM HR_WAREHOUSE.{business_objective.upper()}_METRICS
        WHERE effective_date >= DATEADD(month, -12, CURRENT_DATE())
        '''
        return session.sql(query).to_pandas()
    
    # Analytics Features Implementation
    {generate_feature_code(analytics_features)}
    
    # User-specific Views
    {generate_user_views(target_users)}

if __name__ == "__main__":
    main()
                """
                
                st.code(architecture_code, language="python")
                
                # Business case
                st.markdown("#### Business Impact Projection")
                impact_metrics = {
                    "Cost Optimization": {"savings": "$250K annually", "efficiency": "40% reduction in manual work"},
                    "Talent Retention": {"retention": "15% improvement", "cost_avoidance": "$500K in replacement costs"},
                    "Workforce Planning": {"accuracy": "25% better forecasting", "agility": "50% faster decision making"},
                    "Performance Management": {"engagement": "20% increase", "productivity": "10% improvement"},
                    "Compliance Reporting": {"audit_time": "80% reduction", "accuracy": "99.9% compliance rate"}
                }
                
                if business_objective in impact_metrics:
                    metrics = impact_metrics[business_objective]
                    col_imp1, col_imp2 = st.columns(2)
                    with col_imp1:
                        key1, value1 = list(metrics.items())[0]
                        st.metric(key1.replace('_', ' ').title(), value1)
                    with col_imp2:
                        key2, value2 = list(metrics.items())[1]
                        st.metric(key2.replace('_', ' ').title(), value2)
    
    with tabs[2]:
        st.markdown("### Real-time Integration Showcase")
        
        # Demonstrate live data capabilities
        st.markdown("""
        #### Live Data Pipeline Demonstration
        
        This section showcases the real-time integration capabilities that make Streamlit in Snowflake 
        powerful for enterprise HR analytics.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Data Freshness Monitoring**")
            
            # Simulate real-time monitoring
            data_sources_status = pd.DataFrame({
                'Data Source': ['Employee Master', 'Payroll', 'Performance', 'Recruiting'],
                'Last Updated': ['2 min ago', '15 min ago', '1 hour ago', '30 min ago'],
                'Status': ['🟢 Current', '🟢 Current', '🟡 Stale', '🟢 Current'],
                'Records': ['1,234', '1,234', '1,180', '567']
            })
            
            st.dataframe(data_sources_status, use_container_width=True, hide_index=True)
            
            # Real-time query example
            st.markdown("**Live Query Execution**")
            st.code("""
# Execute live queries with automatic refresh
@st.cache_data(ttl=60)
def get_current_headcount():
    return session.sql('''
        SELECT 
            department,
            COUNT(*) as current_count,
            COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY snapshot_date) as change
        FROM employee_snapshot 
        WHERE snapshot_date = CURRENT_DATE()
        GROUP BY department
    ''').to_pandas()

# Auto-refresh every minute
current_data = get_current_headcount()
            """, language="python")
        
        with col2:
            st.markdown("**Performance Optimization**")
            
            perf_metrics = pd.DataFrame({
                'Query Type': ['Dashboard Load', 'Filter Update', 'Export Report', 'Drill-down'],
                'Avg Response': ['1.2s', '0.3s', '4.5s', '0.8s'],
                'SLA Target': ['< 2s', '< 1s', '< 10s', '< 2s'],
                'Status': ['✅ Meeting', '✅ Meeting', '✅ Meeting', '✅ Meeting']
            })
            
            st.dataframe(perf_metrics, use_container_width=True, hide_index=True)
            
            # Optimization showcase
            st.markdown("**Query Optimization Example**")
            st.code("""
# Optimized for enterprise scale
CREATE OR REPLACE VIEW HR_METRICS_OPTIMIZED AS
SELECT 
    dept_id,
    emp_count,
    avg_tenure,
    turnover_rate
FROM HR_FACT_TABLE
CLUSTER BY (dept_id, effective_date)
SAMPLE (10000 ROWS);  -- For large datasets

# Streamlit implementation
@st.cache_data(ttl=300, max_entries=50)
def load_optimized_metrics(filters):
    return session.table('HR_METRICS_OPTIMIZED').filter(filters).to_pandas()
            """, language="sql")
    
    with tabs[3]:
        st.markdown("### Enterprise Deployment Ready")
        
        st.markdown("""
        #### Production Deployment Checklist
        
        This solution is enterprise-ready with the following capabilities:
        """)
        
        # Deployment readiness checklist
        deployment_features = [
            ("🔐 Security", "Role-based access control with Snowflake RBAC integration"),
            ("📊 Scalability", "Auto-scaling compute with Snowflake warehouses"),
            ("🔄 Real-time", "Sub-minute data refresh with automatic cache management"),
            ("📱 Responsive", "Mobile-friendly interface for executive access"),
            ("🚨 Monitoring", "Built-in performance monitoring and alerting"),
            ("📈 Analytics", "Advanced analytics with ML model integration"),
            ("🌐 Global", "Multi-region deployment with data residency compliance"),
            ("🔧 Maintenance", "Automated testing and deployment pipelines")
        ]
        
        for icon_title, description in deployment_features:
            st.markdown(f"**{icon_title}**: {description}")
        
        st.markdown("#### Deployment Commands")
        
        deployment_code = '''
-- 1. Create Streamlit App in Snowflake
CREATE STREAMLIT APP hr_custom_solution
    ROOT_LOCATION = '@hr_apps_stage'
    MAIN_FILE = 'custom_solution.py'
    QUERY_WAREHOUSE = 'HR_ANALYTICS_WH';

-- 2. Configure Security
GRANT USAGE ON STREAMLIT APP hr_custom_solution TO ROLE hr_analyst;
GRANT USAGE ON STREAMLIT APP hr_custom_solution TO ROLE hr_manager;
GRANT USAGE ON STREAMLIT APP hr_custom_solution TO ROLE executive;

-- 3. Set up Data Access
GRANT SELECT ON SCHEMA hr_warehouse.employee_data TO STREAMLIT APP hr_custom_solution;
GRANT SELECT ON SCHEMA hr_warehouse.analytics_views TO STREAMLIT APP hr_custom_solution;

-- 4. Deploy and Monitor
ALTER STREAMLIT APP hr_custom_solution SET 
    QUERY_WAREHOUSE = 'HR_ANALYTICS_WH',
    COMMENT = 'Production HR Analytics Solution - Version 1.0';
        '''
        
        st.code(deployment_code, language="sql")
        
        # Success metrics
        st.markdown("#### Expected Outcomes")
        
        outcome_col1, outcome_col2, outcome_col3 = st.columns(3)
        
        with outcome_col1:
            st.metric("Deployment Time", "< 30 minutes", help="From development to production")
        with outcome_col2:
            st.metric("User Training", "< 1 hour", help="Intuitive interface requires minimal training")
        with outcome_col3:
            st.metric("ROI Timeline", "< 3 months", help="Positive return on investment")


def generate_solution_code(solution_name):
    """Generate specific solution code based on template"""
    
    code_templates = {
        "Executive Dashboard": '''
# Executive Dashboard - C-Suite Ready
import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Executive HR Dashboard", layout="wide")

# Executive Summary Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Workforce", "1,234", "+2.3%")
with col2:
    st.metric("Employee Engagement", "87%", "+5%")
with col3:
    st.metric("Time to Fill", "32 days", "-8 days")
with col4:
    st.metric("Annual Turnover", "12.5%", "-2.1%")

# Executive-level visualizations
st.plotly_chart(create_executive_trend_chart(), use_container_width=True)
        ''',
        
        "Workforce Planning Tool": '''
# Workforce Planning Tool - Predictive Analytics
import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

# Scenario Planning Interface
st.subheader("Workforce Scenario Planning")

scenario_inputs = st.columns(3)
with scenario_inputs[0]:
    growth_rate = st.slider("Growth Rate %", -10, 25, 5)
with scenario_inputs[1]:
    attrition_rate = st.slider("Expected Attrition %", 5, 25, 12)
with scenario_inputs[2]:
    budget_change = st.slider("Budget Change %", -20, 30, 0)

# Predictive modeling results
forecast_results = generate_workforce_forecast(growth_rate, attrition_rate, budget_change)
st.plotly_chart(forecast_results, use_container_width=True)
        '''
    }
    
    if solution_name in code_templates:
        st.code(code_templates[solution_name], language="python")
        
        st.download_button(
            f"Download {solution_name} Code",
            code_templates[solution_name],
            file_name=f"{solution_name.lower().replace(' ', '_')}.py",
            mime="text/plain"
        )

def generate_feature_code(features):
    """Generate code for selected analytics features"""
    
    feature_implementations = {
        "Real-time Dashboards": '''
    # Real-time Dashboard Implementation
    @st.cache_data(ttl=60)
    def load_realtime_metrics():
        return session.sql("SELECT * FROM live_hr_metrics").to_pandas()
    
    metrics_data = load_realtime_metrics()
    create_realtime_dashboard(metrics_data)''',
        
        "Predictive Modeling": '''
    # Predictive Analytics Implementation
    from snowflake.ml.modeling import LinearRegression
    
    def build_turnover_prediction():
        model_data = session.table("employee_features").to_pandas()
        model = LinearRegression().fit(model_data)
        return model.predict(current_employee_data)''',
        
        "Automated Alerts": '''
    # Automated Alert System
    def check_alert_conditions():
        current_metrics = get_current_metrics()
        if current_metrics['turnover_rate'] > threshold:
            send_alert("High turnover alert", stakeholders)'''
    }
    
    code_blocks = []
    for feature in features:
        if feature in feature_implementations:
            code_blocks.append(feature_implementations[feature])
    
    return '\n\n'.join(code_blocks)

def generate_user_views(users):
    """Generate user-specific view code"""
    
    user_view_code = '''
    # User-specific Views
    current_user_role = session.get_current_role()
    
    if current_user_role in ['CHRO', 'EXECUTIVE']:
        display_executive_view()
    elif current_user_role == 'HR_PARTNER':
        display_hr_partner_view()
    elif current_user_role == 'MANAGER':
        display_manager_view()
    '''
    
    return user_view_code

def display_enterprise_deployment_guide():
    """Enterprise deployment showcase"""
    
    st.header("Enterprise Deployment & Architecture")
    
    st.markdown("""
    ### Production-Ready Deployment Architecture
    
    This section demonstrates enterprise-grade deployment capabilities, showcasing how custom HR solutions 
    can be rapidly deployed and scaled across global organizations.
    """)
    
    tabs = st.tabs(["Architecture Overview", "Security & Compliance", "Performance & Scale", "Governance"])
    
    with tabs[0]:
        st.markdown("#### Enterprise Architecture")
        
        # Architecture diagram (simplified representation)
        architecture_layers = pd.DataFrame({
            'Layer': ['Data Sources', 'Snowflake Data Cloud', 'Streamlit Applications', 'End Users'],
            'Components': [
                'HRIS, Payroll, ATS, Performance Systems',
                'Data Warehouse, Compute, Security, Governance',
                'Custom Apps, Dashboards, Analytics Tools',
                'HR Partners, Managers, Executives, Employees'
            ],
            'Key Features': [
                'Real-time integration, API connectivity',
                'Auto-scaling, Role-based access, Data sharing',
                'Interactive UI, Self-service analytics',
                'Mobile access, Personalized views'
            ]
        })
        
        st.dataframe(architecture_layers, use_container_width=True, hide_index=True)
        
        st.code('''
# Enterprise Deployment Configuration
# snowflake_apps_config.sql

-- Create dedicated warehouse for HR applications
CREATE WAREHOUSE HR_ANALYTICS_WH WITH
    WAREHOUSE_SIZE = 'LARGE'
    AUTO_SUSPEND = 60
    AUTO_RESUME = TRUE
    SCALING_POLICY = 'ECONOMY';

-- Create application database
CREATE DATABASE HR_APPLICATIONS;
CREATE SCHEMA HR_APPLICATIONS.STREAMLIT_APPS;

-- Set up staging area for app deployments
CREATE STAGE HR_APPLICATIONS.STREAMLIT_APPS.APP_STAGE;

-- Create role hierarchy
CREATE ROLE HR_APP_ADMIN;
CREATE ROLE HR_APP_USER;
CREATE ROLE HR_APP_VIEWER;

-- Grant permissions
GRANT USAGE ON WAREHOUSE HR_ANALYTICS_WH TO ROLE HR_APP_USER;
GRANT USAGE ON DATABASE HR_APPLICATIONS TO ROLE HR_APP_USER;
        ''', language="sql")
    
    with tabs[1]:
        st.markdown("#### Security & Compliance Framework")
        
        security_features = [
            ("🔐 Authentication", "SSO integration with SAML/OAuth", "Enterprise SSO"),
            ("🛡️ Authorization", "Role-based access control", "Snowflake RBAC"),
            ("🔒 Data Protection", "Column-level security", "Dynamic masking"),
            ("📊 Audit Logging", "Complete access tracking", "SOX compliance"),
            ("🌍 Data Residency", "Region-specific deployment", "GDPR compliance"),
            ("🔍 Privacy Controls", "PII detection and masking", "Automated compliance")
        ]
        

        
        st.markdown("#### Compliance Implementation")
        st.code('''
-- Row-level security implementation
CREATE ROW ACCESS POLICY employee_data_policy AS (
    user_department = current_user_department()
    OR current_role() IN ('HR_ADMIN', 'EXECUTIVE')
);

-- Apply policy to sensitive tables
ALTER TABLE employee_data ADD ROW ACCESS POLICY employee_data_policy ON (department);

-- Column-level masking for PII
CREATE MASKING POLICY ssn_mask AS (val string) RETURNS string ->
    CASE 
        WHEN current_role() IN ('HR_ADMIN', 'PAYROLL') THEN val
        ELSE 'XXX-XX-' || RIGHT(val, 4)
    END;

ALTER TABLE employee_data MODIFY COLUMN ssn SET MASKING POLICY ssn_mask;
        ''', language="sql")
    
    with tabs[2]:
        st.markdown("#### Performance & Scalability")
        
        # Performance metrics
        perf_col1, perf_col2, perf_col3 = st.columns(3)
        
        with perf_col1:
            st.metric("Concurrent Users", "1,000+", help="Tested concurrent user capacity")
        with perf_col2:
            st.metric("Query Response", "< 2 seconds", help="95th percentile response time")
        with perf_col3:
            st.metric("Data Volume", "10TB+", help="Tested data warehouse size")
        
        st.markdown("#### Auto-scaling Configuration")
        st.code('''
# Performance optimization strategies

# 1. Warehouse auto-scaling
CREATE WAREHOUSE HR_ANALYTICS_WH WITH
    WAREHOUSE_SIZE = 'MEDIUM'
    MIN_CLUSTER_COUNT = 1
    MAX_CLUSTER_COUNT = 10
    SCALING_POLICY = 'STANDARD'
    AUTO_SUSPEND = 60;

# 2. Query result caching
@st.cache_data(ttl=300, max_entries=1000)
def load_department_metrics(dept_id, date_range):
    query = f"""
    SELECT * FROM hr_metrics_materialized_view 
    WHERE department_id = '{dept_id}' 
    AND date BETWEEN '{date_range[0]}' AND '{date_range[1]}'
    """
    return session.sql(query).to_pandas()

# 3. Materialized views for complex calculations
CREATE MATERIALIZED VIEW employee_metrics_daily AS
SELECT 
    department,
    DATE_TRUNC('day', event_date) as metric_date,
    COUNT(*) as headcount,
    AVG(tenure_days) as avg_tenure,
    SUM(CASE WHEN termination_date IS NOT NULL THEN 1 ELSE 0 END) as terminations
FROM employee_events
GROUP BY department, DATE_TRUNC('day', event_date);
        ''', language="python")
    
    with tabs[3]:
        st.markdown("#### Data Governance & Quality")
        
        governance_areas = [
            ("📋 Data Lineage", "Track data from source to insight"),
            ("✅ Quality Monitoring", "Automated data quality checks"),
            ("📚 Data Catalog", "Self-documenting data dictionary"),
            ("🔄 Change Management", "Version control for all changes"),
            ("📊 Usage Analytics", "Monitor application adoption"),
            ("🚨 Alert Management", "Proactive issue detection")
        ]
        
        for icon_area, description in governance_areas:
            st.markdown(f"**{icon_area}**: {description}")
        
        st.markdown("#### Governance Implementation")
        st.code('''
-- Data quality monitoring
CREATE TASK data_quality_check
WAREHOUSE = 'HR_ANALYTICS_WH'
SCHEDULE = 'USING CRON 0 8 * * * UTC'
AS
$$
DECLARE
    quality_issues INTEGER;
BEGIN
    -- Check for data anomalies
    SELECT COUNT(*) INTO :quality_issues
    FROM hr_data_quality_checks
    WHERE check_date = CURRENT_DATE()
    AND status = 'FAILED';
    
    -- Alert if issues found
    IF (quality_issues > 0) THEN
        CALL send_alert('Data quality issues detected', :quality_issues);
    END IF;
END;
$$;

-- Data lineage tracking
CREATE VIEW data_lineage AS
SELECT 
    table_name,
    column_name,
    source_system,
    transformation_logic,
    last_updated
FROM information_schema.columns
JOIN data_governance.lineage_mapping USING (table_name, column_name);
        ''', language="sql")
        
        # Final call-to-action
        st.markdown("---")
        st.success("""
        🚀 **Ready for Enterprise Deployment**
        
        This HR Analytics platform demonstrates enterprise-ready capabilities including:
        - Real-time Snowflake integration
        - Role-based security and compliance
        - Auto-scaling performance
        - Comprehensive governance
        
        **Next Steps**: Contact IT or Data Engineering teams to begin deployment planning.
        """)

# Keep all existing dashboard functions (display_talent_acquisition_dashboard, etc.)
# [Previous functions remain unchanged - display_overview_dashboard, display_talent_acquisition_dashboard, 
#  display_employee_retention_dashboard, display_diversity_dashboard, and all data generation functions]
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



# [Include all the original data generation functions here - generate_employee_data, generate_recruitment_data, generate_turnover_data]
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