import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
from styles import apply_custom_styles, apply_page_config

# Apply page configuration and custom styling
apply_page_config()
# apply_custom_styles()

# Page configuration
st.set_page_config(
    page_title="Strategic Innovation Portfolio | Data & AI Enablement",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Sidebar navigation
st.sidebar.markdown("""
<div class="sidebar-section">
    <h3>Strategic Navigation</h3>
    <p>Explore our data & AI enablement expertise</p>
</div>
""", unsafe_allow_html=True)

# Main navigation
page = st.sidebar.selectbox(
    "Select Focus Area",
    ["Executive Overview", "Data Strategy Framework", "AI Strategy & Implementation", 
     "Change Management", "Analytics Solutions", "Innovation Culture", "Project Portfolio"]
)

# Helper functions
def create_maturity_chart():
    categories = ['Data Governance', 'Analytics Capability', 'AI/ML Adoption', 'Change Readiness', 'Innovation Culture']
    current = [3.2, 3.8, 2.9, 3.5, 3.1]
    target = [4.5, 4.7, 4.3, 4.6, 4.8]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=current, theta=categories, fill='toself', name='Current State',
        fillcolor='rgba(42, 82, 152, 0.3)', line=dict(color='#2a5298')
    ))
    fig.add_trace(go.Scatterpolar(
        r=target, theta=categories, fill='toself', name='Target State',
        fillcolor='rgba(102, 126, 234, 0.3)', line=dict(color='#667eea')
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        showlegend=True, height=500,
        title="Data & AI Maturity Assessment"
    )
    return fig

def create_innovation_pipeline():
    stages = ['Ideation', 'Proof of Concept', 'Pilot', 'Scale', 'Production']
    projects = [24, 12, 8, 5, 3]
    
    fig = px.funnel(x=projects, y=stages, title="Innovation Project Pipeline")
    fig.update_traces(marker_color=['#667eea', '#764ba2', '#2a5298', '#1e3c72', '#0f2452'])
    fig.update_layout(height=400)
    return fig

# PAGE CONTENT
if page == "Executive Overview":
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Strategic Innovation Portfolio</h1>
        <h3>Data & AI Enablement Excellence</h3>
        <p>Transforming organizations through strategic data initiatives and AI-powered innovation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Projects", "47", "↗️ 23%")
    with col2:
        st.metric("AI Models Deployed", "23", "↗️ 156%")
    with col3:
        st.metric("Data Sources Integrated", "127", "↗️ 34%")
    with col4:
        st.metric("ROI Generated", "$4.2M", "↗️ 89%")
    
    # Strategic overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Strategic Value Proposition")
        st.markdown("""
        **Our mission is to accelerate organizational transformation through data and AI enablement:**
        
        - **Data Strategy Leadership**: Comprehensive frameworks for data governance, architecture, and analytics
        - **AI Implementation Excellence**: From proof-of-concept to enterprise-scale AI deployment
        - **Change Management**: Proven methodologies for technology adoption and cultural transformation
        - **Innovation Acceleration**: Building learning cultures that thrive in rapidly evolving tech landscapes
        """)
        
        st.subheader("📈 Current Impact")
        
        # Create sample impact data
        impact_data = pd.DataFrame({
            'Quarter': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024'],
            'Projects Completed': [8, 12, 15, 18],
            'Value Generated ($M)': [0.8, 1.2, 1.8, 2.4],
            'Teams Enabled': [15, 23, 31, 42]
        })
        
        fig = px.line(impact_data, x='Quarter', y=['Projects Completed', 'Teams Enabled'], 
                     title="Quarterly Progress Metrics")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Innovation Highlights")
        
        highlights = [
            {"title": "AI-Powered Analytics Platform", "impact": "340% faster insights", "icon": "🤖"},
            {"title": "Automated Data Pipeline", "impact": "85% reduction in processing time", "icon": "⚡"},
            {"title": "ML-Driven Forecasting", "impact": "23% improvement in accuracy", "icon": "🎯"},
            {"title": "Real-time Dashboard Suite", "impact": "100% executive adoption", "icon": "📊"}
        ]
        
        for highlight in highlights:
            st.markdown(f"""
            <div class="innovation-card">
                <h4>{highlight['icon']} {highlight['title']}</h4>
                <p><strong>{highlight['impact']}</strong></p>
            </div>
            """, unsafe_allow_html=True)

elif page == "Data Strategy Framework":
    st.markdown("""
    <div class="main-header">
        <h1>Data Strategy Framework</h1>
        <p>Comprehensive approach to data governance, architecture, and value creation</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Architecture", "Governance", "Value Framework"])
    
    with tab1:
        st.subheader("Data Architecture Blueprint")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🏢 Modern Data Stack Components:**
            
            **Data Sources & Ingestion:**
            - Streaming data pipelines (Kafka, Kinesis)
            - Batch processing frameworks (Spark, Airflow)
            - API integrations and connectors
            - Real-time CDC (Change Data Capture)
            
            **Storage & Processing:**
            - Data Lake architecture (Delta Lake, Iceberg)
            - Cloud data warehouses (Snowflake, BigQuery)
            - Feature stores for ML operations
            - Vector databases for AI applications
            """)
        
        with col2:
            # Architecture maturity assessment
            fig = create_maturity_chart()
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Implementation Roadmap")
        
        roadmap_data = pd.DataFrame({
            'Phase': ['Foundation', 'Integration', 'Analytics', 'AI/ML', 'Innovation'],
            'Duration (Months)': [3, 4, 3, 6, 12],
            'Investment ($K)': [150, 300, 200, 500, 800],
            'Expected ROI': [1.5, 2.3, 3.1, 4.2, 6.8]
        })
        
        st.dataframe(roadmap_data, use_container_width=True)
    
    with tab2:
        st.subheader("Data Governance Excellence")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            **Governance Pillars:**
            
            **Data Quality Management:**
            - Automated data quality monitoring
            - Data lineage and impact analysis
            - Quality scorecards and SLAs
            - Continuous improvement processes
            
            **Privacy & Compliance:**
            - GDPR/CCPA compliance frameworks
            - Data classification and cataloging
            - Access controls and audit trails
            - Privacy by design implementation
            
            **Metadata Management:**
            - Business glossary and data dictionary
            - Automated metadata discovery
            - Data stewardship workflows
            - Self-service data discovery
            """)
        
        with col2:
            # Governance metrics
            governance_metrics = pd.DataFrame({
                'Metric': ['Data Quality Score', 'Compliance Rate', 'Catalog Coverage', 'User Adoption'],
                'Current': [87, 94, 76, 82],
                'Target': [95, 98, 90, 90]
            })
            
            fig = px.bar(governance_metrics, x='Metric', y=['Current', 'Target'], 
                        title="Governance KPIs", barmode='group')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Data Value Framework")
        
        st.markdown("""
        **💰 Value Creation Model:**
        
        Our systematic approach to measuring and maximizing data value across the organization.
        """)
        
        # Value framework visualization
        col1, col2 = st.columns(2)
        
        with col1:
            value_categories = ['Cost Reduction', 'Revenue Growth', 'Risk Mitigation', 'Innovation']
            value_amounts = [1200000, 2800000, 800000, 1500000]
            
            fig = px.pie(values=value_amounts, names=value_categories, 
                        title="Data Value Distribution ($)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            **Value Drivers:**
            
            **Cost Reduction** ($1.2M)
            - Process automation
            - Resource optimization
            - Operational efficiency
            
            **Revenue Growth** ($2.8M)
            - Data-driven insights
            - Customer analytics
            - Market intelligence
            
            **Risk Mitigation** ($800K)
            - Fraud detection
            - Compliance automation
            - Predictive maintenance
            
            **Innovation** ($1.5M)
            - New product development
            - Service enhancement
            - Market expansion
            """)

elif page == "AI Strategy & Implementation":
    st.markdown("""
    <div class="main-header">
        <h1>AI Strategy & Implementation</h1>
        <p>Enterprise AI adoption roadmap and implementation excellence</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Strategy", "Implementation", "Use Cases", "Innovation Lab"])
    
    with tab1:
        st.subheader("AI Strategic Framework")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **AI Vision & Objectives:**
            
            **Strategic Priorities:**
            1. **Augment Human Intelligence**: Enhance decision-making with AI insights
            2. **Automate Routine Processes**: Free up human capital for strategic work
            3. **Accelerate Innovation**: Use AI to discover new opportunities
            4. **Optimize Operations**: Improve efficiency across all business functions
            
            **Implementation Approach:**
            - **Crawl**: Pilot projects and proof of concepts
            - **Walk**: Scaled implementations with clear ROI
            - **Run**: Enterprise-wide AI transformation
            
            **Key Focus Areas:**
            - Natural Language Processing for customer insights
            - Computer Vision for quality assurance
            - Predictive Analytics for forecasting
            - Recommendation engines for personalization
            - Process automation with intelligent workflows
            """)
        
        with col2:
            # AI maturity progression
            maturity_data = pd.DataFrame({
                'Stage': ['Basic Analytics', 'Predictive Models', 'AI Applications', 'AI-First Culture'],
                'Progress': [95, 78, 45, 23]
            })
            
            fig = px.bar(maturity_data, x='Stage', y='Progress', 
                        title="AI Maturity Progression (%)")
            fig.update_traces(marker_color=['#2a5298', '#667eea', '#764ba2', '#b093d3'])
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Implementation Excellence")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🛠️ MLOps Framework:**
            
            **Development Pipeline:**
            - Data versioning and lineage tracking
            - Automated model training and validation
            - A/B testing for model performance
            - Continuous integration/deployment
            
            **Production Management:**
            - Model monitoring and alerting
            - Performance drift detection
            - Automated retraining workflows
            - Rollback and recovery procedures
            
            **Governance & Ethics:**
            - Bias detection and mitigation
            - Explainability and transparency
            - Ethical AI review processes
            - Regulatory compliance monitoring
            """)
        
        with col2:
            st.markdown("""
            **🔧 Technology Stack:**
            
            **ML Platforms:**
            - MLflow for experiment tracking
            - Kubeflow for workflow orchestration
            - TensorFlow/PyTorch for model development
            - Weights & Biases for collaboration
            
            **Infrastructure:**
            - Kubernetes for container orchestration
            - Docker for model packaging
            - Cloud GPUs for training
            - Edge deployment for real-time inference
            
            **Monitoring & Observability:**
            - Prometheus for metrics collection
            - Grafana for visualization
            - Custom dashboards for business metrics
            - Automated alerting systems
            """)
    
    with tab3:
        st.subheader("AI Use Cases Portfolio")
        
        use_cases = pd.DataFrame({
            'Use Case': ['Customer Churn Prediction', 'Demand Forecasting', 'Quality Control', 
                        'Fraud Detection', 'Recommendation Engine', 'Process Optimization'],
            'Business Unit': ['Sales', 'Operations', 'Manufacturing', 'Finance', 'Marketing', 'Operations'],
            'ROI ($K)': [450, 320, 680, 890, 540, 380],
            'Implementation Status': ['Production', 'Pilot', 'Production', 'Production', 'Development', 'Pilot'],
            'Complexity': ['Medium', 'High', 'Medium', 'High', 'Medium', 'High']
        })
        
        st.dataframe(use_cases, use_container_width=True)
        
        # ROI visualization
        fig = px.bar(use_cases, x='Use Case', y='ROI ($K)', 
                    color='Implementation Status',
                    title="AI Use Cases ROI Analysis")
        if fig is not None:
            fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("AI Innovation Lab")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Emerging Technology Exploration:**
            
            🧠 **Generative AI Initiatives:**
            - Large Language Model fine-tuning
            - Code generation assistants
            - Creative content automation
            - Intelligent document processing
            
            🔮 **Future Technologies:**
            - Quantum machine learning research
            - Federated learning implementations
            - Edge AI optimization
            - Neuromorphic computing exploration
            """)
        
        with col2:
            # Innovation pipeline
            fig = create_innovation_pipeline()
            st.plotly_chart(fig, use_container_width=True)

elif page == "Change Management":
    st.markdown("""
    <div class="main-header">
        <h1>🔄 Change Management Excellence</h1>
        <p>Proven methodologies for successful technology adoption and transformation</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Framework", "👥 Stakeholder Engagement", "📊 Success Metrics"])
    
    with tab1:
        st.subheader("Change Management Framework")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            **🎯 ADKAR-Based Approach:**
            
            **Awareness** - Creating understanding of why change is needed
            - Executive communications and town halls
            - Change impact assessments
            - Benefits and risks communication
            - Success story sharing
            
            **Desire** - Fostering motivation to support and engage
            - Stakeholder analysis and engagement
            - Resistance management strategies
            - Incentive alignment
            - Cultural readiness assessment
            
            **Knowledge** - Developing skills and understanding
            - Comprehensive training programs
            - Hands-on workshops and labs
            - Certification pathways
            - Knowledge sharing communities
            
            **Ability** - Implementing new behaviors and processes
            - Process redesign and optimization
            - Tool and technology enablement
            - Performance support systems
            - Coaching and mentoring programs
            
            **Reinforcement** - Sustaining change over time
            - Performance metrics and feedback
            - Continuous improvement processes
            - Recognition and reward systems
            - Change champion networks
            """)
        
        with col2:
            # Change readiness assessment
            readiness_data = pd.DataFrame({
                'Factor': ['Leadership Support', 'Resource Availability', 'Change Capability', 
                          'Culture Alignment', 'Communication Effectiveness'],
                'Score': [4.2, 3.8, 3.5, 3.2, 4.0]
            })
            
            fig = px.bar(readiness_data, x='Score', y='Factor', orientation='h',
                        title="Change Readiness Assessment")
            fig.update_layout(xaxis_range=[0, 5])
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Stakeholder Engagement Strategy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🎭 Stakeholder Personas:**
            
            **Champions (25%)**
            - Early adopters and influencers
            - High engagement and advocacy
            - Strategic: Leverage as change agents
            
            **Supporters (35%)**
            - Positive but passive attitude
            - Need activation and enablement
            - Strategic: Convert to active champions
            
            **Neutral (25%)**
            - Wait-and-see approach
            - Information seekers
            - Strategic: Education and demonstration
            
            **Resisters (15%)**
            - Concerned about change impact
            - May actively oppose
            - Strategic: Address concerns, provide support
            """)
        
        with col2:
            # Stakeholder engagement plan
            engagement_data = pd.DataFrame({
                'Week': range(1, 13),
                'Champions': [85, 87, 89, 91, 93, 94, 95, 96, 97, 98, 98, 99],
                'Supporters': [45, 52, 58, 65, 71, 76, 80, 83, 86, 88, 90, 92],
                'Neutral': [20, 28, 35, 42, 48, 54, 60, 65, 70, 74, 78, 82],
                'Resisters': [5, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48]
            })
            
            fig = px.line(engagement_data, x='Week', y=['Champions', 'Supporters', 'Neutral', 'Resisters'],
                         title="Stakeholder Engagement Progress")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Success Metrics & KPIs")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("User Adoption Rate", "78%", "↗️ +23%")
            st.metric("Training Completion", "92%", "↗️ +15%")
            
        with col2:
            st.metric("Change Satisfaction", "4.1/5", "↗️ +0.8")
            st.metric("Process Efficiency", "+34%", "↗️ +12%")
            
        with col3:
            st.metric("Support Tickets", "-45%", "↘️ -67")
            st.metric("Time to Proficiency", "2.3 weeks", "↘️ -40%")
        
        st.subheader("Change Impact Analysis")
        
        impact_data = pd.DataFrame({
            'Metric': ['Productivity', 'Employee Satisfaction', 'Process Efficiency', 'Quality Scores', 'Innovation Index'],
            'Before': [100, 100, 100, 100, 100],
            'After': [134, 118, 142, 126, 156],
            'Target': [130, 115, 140, 125, 150]
        })
        
        fig = px.bar(impact_data, x='Metric', y=['Before', 'After', 'Target'], 
                    title="Change Impact Results", barmode='group')
        st.plotly_chart(fig, use_container_width=True)

elif page == "Analytics Solutions":
    st.markdown("""
    <div class="main-header">
        <h1>📈 Analytics Solutions Portfolio</h1>
        <p>Comprehensive analytics capabilities driving data-driven decision making</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboards", "🔍 Advanced Analytics", "🤖 Predictive Models", "📱 Self-Service"])
    
    with tab1:
        st.subheader("Executive Dashboard Suite")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sample KPI dashboard
            st.markdown("**🎯 Key Performance Indicators**")
            
            kpi_data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'Revenue ($M)': [12.3, 13.1, 14.2, 13.8, 15.4, 16.2],
                'Customer Acquisition': [1250, 1380, 1420, 1390, 1560, 1680],
                'Conversion Rate (%)': [3.2, 3.4, 3.7, 3.5, 3.9, 4.1]
            })
            
            fig = px.line(kpi_data, x='Month', y='Revenue ($M)', title="Revenue Trend")
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("**📈 Business Metrics**")
            
            fig2 = px.bar(kpi_data, x='Month', y='Customer Acquisition', 
                         title="Customer Acquisition")
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("""
        **Dashboard Features:**
        
        **Real-time Monitoring:**
        - Live data refresh every 15 minutes
        - Alert system for threshold breaches
        - Mobile-responsive design
        - Role-based access control
        
        **Interactive Analytics:**
        - Drill-down capabilities
        - Filter and slice functionality
        - Export and sharing options
        - Collaborative annotations
        """)
    
    with tab2:
        st.subheader("Advanced Analytics Capabilities")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **🔬 Statistical Analysis:**
            
            **Customer Segmentation:**
            - RFM analysis for customer value
            - Behavioral clustering algorithms
            - Lifetime value prediction
            - Churn risk modeling
            
            **Market Analysis:**
            - Price elasticity modeling
            - Competitive intelligence
            - Market basket analysis
            - Seasonal trend decomposition
            
            **Operational Analytics:**
            - Supply chain optimization
            - Inventory forecasting
            - Resource allocation modeling
            - Performance benchmarking
            """)
            
            # Create sample segmentation visualization
            np.random.seed(42)
            n_customers = 1000
            segmentation_data = pd.DataFrame({
                'Customer_ID': range(n_customers),
                'Recency': np.random.exponential(30, n_customers),
                'Frequency': np.random.poisson(5, n_customers),
                'Monetary': np.random.lognormal(4, 1, n_customers),
                'Segment': np.random.choice(['Champions', 'Loyal Customers', 'Potential Loyalists', 
                                           'At Risk', 'Cannot Lose Them'], n_customers)
            })
            
            fig = px.scatter(segmentation_data, x='Frequency', y='Monetary', 
                           color='Segment', title="Customer Segmentation Analysis")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("""
            **🧮 Advanced Techniques:**
            
            **Time Series Analysis:**
            - ARIMA modeling
            - Prophet forecasting
            - Anomaly detection
            - Seasonality analysis
            
            **Statistical Modeling:**
            - Regression analysis
            - A/B testing framework
            - Survival analysis
            - Causal inference
            
            **Optimization:**
            - Linear programming
            - Monte Carlo simulation
            - Genetic algorithms
            - Network analysis
            """)
    
    with tab3:
        st.subheader("Predictive Models Portfolio")
        
        models_data = pd.DataFrame({
            'Model Name': ['Customer Churn Predictor', 'Demand Forecasting', 'Price Optimization', 
                          'Fraud Detection', 'Recommendation Engine', 'Quality Predictor'],
            'Business Area': ['Customer Success', 'Supply Chain', 'Pricing', 'Risk', 'Marketing', 'Operations'],
            'Accuracy (%)': [87, 92, 85, 94, 78, 89],
            'ROI ($K/month)': [125, 200, 180, 300, 95, 140],
            'Status': ['Production', 'Production', 'Testing', 'Production', 'Development', 'Production']
        })
        
        st.dataframe(models_data, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(models_data, x='Model Name', y='Accuracy (%)', 
                        title="Model Performance Comparison")
            fig.update_xaxis(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(models_data, x='Accuracy (%)', y='ROI ($K/month)', 
                           color='Status', size='ROI ($K/month)',
                           title="Model Performance vs ROI")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Self-Service Analytics Platform")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            **🔧 Platform Capabilities:**
            
            **Data Discovery:**
            - Centralized data catalog
            - Automated metadata discovery
            - Data lineage visualization
            - Smart search and recommendations
            
            **Drag-and-Drop Analytics:**
            - Visual query builder
            - Pre-built visualization templates
            - Automated insights generation
            - Natural language queries
            
            **Collaboration Features:**
            - Shared workspaces
            - Comment and annotation system
            - Version control for analyses
            - Scheduled report delivery
            
            **Governance & Security:**
            - Row-level security
            - Data masking capabilities
            - Audit trails and monitoring
            - Certification workflows
            """)
        
        with col2:
            # Usage metrics
            usage_data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'Active Users': [145, 167, 189, 201, 234, 278],
                'Reports Created': [89, 112, 145, 167, 198, 234],
                'Data Sources Connected': [23, 27, 31, 35, 42, 48]
            })
            
            fig = px.line(usage_data, x='Month', y=['Active Users', 'Reports Created'], 
                         title="Platform Adoption Metrics")
            st.plotly_chart(fig, use_container_width=True)
            
            st.metric("User Satisfaction", "4.6/5", "↗️ +0.3")
            st.metric("Time to Insight", "67% faster", "↗️ +23%")

elif page == "Innovation Culture":
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Cultivating Innovation Culture</h1>
        <p>Building learning organizations that thrive in rapidly evolving technology landscapes</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🌱 Culture Framework", "📚 Learning Programs", "🤝 Communities", "📊 Culture Metrics"])
    
    with tab1:
        st.subheader("Innovation Culture Framework")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **🌟 Cultural Pillars:**
            
            **Psychological Safety**
            - Encourage experimentation and learning from failure
            - Open communication and diverse perspectives
            - Support for calculated risk-taking
            - Constructive feedback culture
            
            **Continuous Learning**
            - Growth mindset development
            - Skill-building and upskilling programs
            - Knowledge sharing and mentorship
            - External learning opportunities
            
            **Agile Mindset**
            - Rapid prototyping and iteration
            - Customer-centric approach
            - Cross-functional collaboration
            - Adaptive planning and execution
            
            **Innovation Processes**
            - Structured innovation methodologies
            - Idea management systems
            - Innovation time allocation (20% time)
            - Recognition and reward systems
            """)
        
        with col2:
            # Culture assessment
            culture_scores = pd.DataFrame({
                'Dimension': ['Psychological Safety', 'Learning Orientation', 'Agility', 'Innovation Process'],
                'Score': [3.8, 4.1, 3.5, 3.2],
                'Industry Avg': [3.2, 3.4, 3.1, 2.8]
            })
            
            fig = px.bar(culture_scores, x='Dimension', y=['Score', 'Industry Avg'], 
                        title="Culture Assessment vs Industry", barmode='group')
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Learning & Development Programs")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📖 Core Programs:**
            
            **Data Science Academy**
            - 12-week intensive program
            - Hands-on projects and mentorship
            - Industry certifications
            - 95% completion rate
            
            **AI/ML Bootcamp**
            - Weekend workshops series
            - Real-world case studies
            - Guest expert sessions
            - Capstone project presentation
            
            **Leadership in Digital Age**
            - Executive education program
            - Digital transformation strategies
            - Change leadership skills
            - Innovation management
            """)
        
        with col2:
            st.markdown("""
            **🎯 Specialized Tracks:**
            
            **Technical Skills:**
            - Cloud platform certifications
            - Programming languages (Python, R, SQL)
            - Data visualization tools
            - MLOps and DevOps practices
            
            **Business Skills:**
            - Data storytelling
            - Strategic thinking
            - Project management
            - Customer experience design
            
            **Soft Skills:**
            - Communication and presentation
            - Collaboration and teamwork
            - Creative problem solving
            - Emotional intelligence
            """)
        
        # Learning engagement metrics
        learning_data = pd.DataFrame({
            'Program': ['Data Science Academy', 'AI/ML Bootcamp', 'Leadership Program', 'Technical Certifications'],
            'Participants': [45, 89, 23, 156],
            'Completion Rate (%)': [95, 87, 91, 78],
            'Satisfaction Score': [4.7, 4.5, 4.8, 4.2]
        })
        
        st.dataframe(learning_data, use_container_width=True)
    
    with tab3:
        st.subheader("Communities of Practice")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🤝 Active Communities:**
            
            **Data Science Guild** (127 members)
            - Weekly tech talks and demos
            - Code review sessions
            - Research paper discussions
            - Kaggle competition teams
            
            **AI Ethics Circle** (45 members)
            - Bias detection workshops
            - Fairness in AI discussions
            - Policy and governance reviews
            - Industry trend analysis
            
            **Innovation Champions** (68 members)
            - Idea incubation support
            - Cross-team collaboration
            - Innovation methodology training
            - Success story sharing
            """)
        
        with col2:
            # Community engagement
            community_data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'Active Members': [189, 201, 223, 245, 267, 289],
                'Events Hosted': [12, 15, 18, 21, 24, 27],
                'Knowledge Artifacts': [34, 41, 48, 55, 63, 71]
            })
            
            fig = px.line(community_data, x='Month', y=['Active Members', 'Events Hosted'], 
                         title="Community Engagement Growth")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **🎪 Innovation Events:**
        
        - **Quarterly Hackathons**: 48-hour innovation challenges
        - **Innovation Showcase**: Monthly demo sessions
        - **Tech Talks**: Weekly expert presentations
        - **Cross-Pollination Sessions**: Inter-department collaboration
        """)
    
    with tab4:
        st.subheader("Culture & Innovation Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Innovation Index", "4.2/5", "↗️ +0.6")
            st.metric("Employee NPS", "+67", "↗️ +23")
        
        with col2:
            st.metric("Learning Hours/Employee", "42.5", "↗️ +18.3")
            st.metric("Internal Mobility Rate", "23%", "↗️ +8%")
        
        with col3:
            st.metric("Ideas Generated", "347", "↗️ +156")
            st.metric("Ideas Implemented", "89", "↗️ +78%")
        
        with col4:
            st.metric("Time to Market", "-35%", "↘️ -15%")
            st.metric("Innovation ROI", "4.8x", "↗️ +1.2x")
        
        # Innovation pipeline
        col1, col2 = st.columns(2)
        
        with col1:
            pipeline_data = pd.DataFrame({
                'Stage': ['Ideas', 'Concept', 'Prototype', 'Pilot', 'Scale'],
                'Count': [347, 89, 34, 12, 5],
                'Success Rate (%)': [100, 26, 38, 35, 42]
            })
            
            fig = px.funnel(pipeline_data, x='Count', y='Stage', 
                           title="Innovation Pipeline")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Innovation impact
            impact_data = pd.DataFrame({
                'Quarter': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024'],
                'Ideas Implemented': [12, 18, 25, 34],
                'Revenue Impact ($M)': [0.5, 0.8, 1.2, 1.8],
                'Cost Savings ($M)': [0.3, 0.5, 0.7, 1.1]
            })
            
            fig = px.bar(impact_data, x='Quarter', y=['Revenue Impact ($M)', 'Cost Savings ($M)'],
                        title="Innovation Financial Impact")
            st.plotly_chart(fig, use_container_width=True)

elif page == "Project Portfolio":
    st.markdown("""
    <div class="main-header">
        <h1>📋 Strategic Project Portfolio</h1>
        <p>Comprehensive overview of active initiatives and their strategic impact</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Project portfolio data
    portfolio_data = pd.DataFrame({
        'Project Name': [
            'Customer 360 Platform', 'Real-time Analytics Engine', 'AI-Powered Forecasting',
            'Data Governance Framework', 'ML Model Factory', 'Advanced Visualization Suite',
            'Automated Data Pipeline', 'Predictive Maintenance', 'Customer Churn Prevention',
            'Supply Chain Optimization', 'Fraud Detection System', 'Recommendation Engine'
        ],
        'Category': [
            'Data Platform', 'Analytics', 'AI/ML', 'Governance', 'AI/ML', 'Analytics',
            'Data Platform', 'AI/ML', 'AI/ML', 'Analytics', 'AI/ML', 'AI/ML'
        ],
        'Status': [
            'In Progress', 'Completed', 'In Progress', 'Planning', 'In Progress', 'Completed',
            'In Progress', 'Testing', 'Production', 'In Progress', 'Production', 'Development'
        ],
        'Priority': [
            'High', 'High', 'Medium', 'High', 'Medium', 'Low', 'High', 'Medium', 'High', 'Medium', 'High', 'Medium'
        ],
        'Budget ($K)': [450, 320, 280, 180, 350, 120, 280, 240, 190, 310, 420, 160],
        'ROI Expected': [3.2, 4.8, 3.9, 2.1, 4.2, 2.8, 5.1, 3.6, 6.2, 2.9, 7.8, 3.4],
        'Completion (%)': [65, 100, 45, 15, 70, 100, 80, 85, 100, 35, 100, 25],
        'Team Size': [8, 6, 5, 4, 7, 3, 6, 5, 4, 7, 6, 5]
    })
    
    tab1, tab2, tab3 = st.tabs(["📊 Portfolio Overview", "🎯 Project Details", "📈 Performance Analytics"])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_projects = len(portfolio_data)
            st.metric("Total Projects", total_projects)
        
        with col2:
            completed_projects = len(portfolio_data[portfolio_data['Status'] == 'Completed'])
            st.metric("Completed Projects", completed_projects, f"↗️ {completed_projects}/{total_projects}")
        
        with col3:
            total_budget = portfolio_data['Budget ($K)'].sum()
            st.metric("Total Budget", f"${total_budget}K")
        
        with col4:
            avg_roi = portfolio_data['ROI Expected'].mean()
            st.metric("Average ROI", f"{avg_roi:.1f}x")
        
        # Portfolio visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Project status distribution
            status_counts = portfolio_data['Status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index, 
                        title="Project Status Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Category breakdown
            category_counts = portfolio_data['Category'].value_counts()
            fig = px.bar(x=category_counts.index, y=category_counts.values, 
                        title="Projects by Category")
            st.plotly_chart(fig, use_container_width=True)
        
        # Portfolio matrix
        fig = px.scatter(portfolio_data, x='Budget ($K)', y='ROI Expected', 
                        color='Category', size='Team Size',
                        hover_data=['Project Name', 'Status', 'Completion (%)'],
                        title="Portfolio Risk/Return Matrix")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Project Portfolio Details")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category_filter = st.selectbox("Filter by Category", 
                                         ['All'] + list(portfolio_data['Category'].unique()))
        
        with col2:
            status_filter = st.selectbox("Filter by Status", 
                                       ['All'] + list(portfolio_data['Status'].unique()))
        
        with col3:
            priority_filter = st.selectbox("Filter by Priority", 
                                         ['All'] + list(portfolio_data['Priority'].unique()))
        
        # Apply filters
        filtered_data = portfolio_data.copy()
        
        if category_filter != 'All':
            filtered_data = filtered_data[filtered_data['Category'] == category_filter]
        
        if status_filter != 'All':
            filtered_data = filtered_data[filtered_data['Status'] == status_filter]
        
        if priority_filter != 'All':
            filtered_data = filtered_data[filtered_data['Priority'] == priority_filter]
        
        # Display filtered data
        st.dataframe(filtered_data, use_container_width=True)
        
        # Project timeline (simplified)
        st.subheader("Project Timeline Overview")
        
        timeline_data = pd.DataFrame({
            'Project': filtered_data['Project Name'],
            'Start': pd.date_range('2024-01-01', periods=len(filtered_data), freq='30D'),
            'Completion': filtered_data['Completion (%)'].values
        })
        
        fig = px.bar(timeline_data, x='Project', y='Completion', 
                    title="Project Completion Status")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Portfolio Performance Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Budget vs ROI analysis
            fig = px.scatter(portfolio_data, x='Budget ($K)', y='ROI Expected', 
                           color='Priority', size='Completion (%)',
                           title="Budget vs Expected ROI")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Completion progress by category
            completion_by_category = portfolio_data.groupby('Category')['Completion (%)'].mean().reset_index()
            fig = px.bar(completion_by_category, x='Category', y='Completion (%)', 
                        title="Average Completion by Category")
            st.plotly_chart(fig, use_container_width=True)
        
        # Resource allocation
        st.subheader("Resource Allocation Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Team size distribution
            fig = px.histogram(portfolio_data, x='Team Size', nbins=10,
                             title="Team Size Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Budget allocation by category
            budget_by_category = portfolio_data.groupby('Category')['Budget ($K)'].sum().reset_index()
            fig = px.pie(budget_by_category, values='Budget ($K)', names='Category',
                        title="Budget Allocation by Category")
            st.plotly_chart(fig, use_container_width=True)
        
        # Key insights
        st.subheader("📊 Key Portfolio Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🎯 High-Impact Projects:**
            - Customer Churn Prevention (6.2x ROI)
            - Fraud Detection System (7.8x ROI)
            - Automated Data Pipeline (5.1x ROI)
            """)
        
        with col2:
            st.markdown("""
            **⚠️ At-Risk Projects:**
            - ML Model Factory (70% complete, medium priority)
            - Supply Chain Optimization (35% complete)
            - Recommendation Engine (25% complete)
            """)
        
        with col3:
            st.markdown("""
            **🚀 Quick Wins:**
            - Real-time Analytics Engine (Completed, 4.8x ROI)
            - Advanced Visualization Suite (Completed, 2.8x ROI)
            - Predictive Maintenance (85% complete)
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Strategic Innovation Portfolio | Data & AI Enablement Excellence</p>
    <p>Transforming organizations through strategic data initiatives and AI-powered innovation</p>
</div>
""", unsafe_allow_html=True)