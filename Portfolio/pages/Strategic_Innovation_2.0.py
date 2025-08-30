import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
#from styles import apply_custom_styles, apply_page_config


# Apply page configuration and custom styling
#apply_page_config()
#apply_custom_styles()

# Page configuration
st.set_page_config(
    page_title="Strategic Innovation Portfolio | Data & AI Enablement",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for help tools and styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .help-tip {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ff6b6b;
        margin: 1rem 0;
        color: white;
    }
    
    .implementation-tip {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #00a8ff;
        margin: 1rem 0;
        color: white;
    }
    
    .leadership-insight {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #26d0ce;
        margin: 1rem 0;
        color: white;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ff6b6b;
        margin: 1rem 0;
        color: #2c3e50;
    }
    
    .innovation-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .help-icon {
        display: inline-block;
        background: #667eea;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        text-align: center;
        font-size: 12px;
        line-height: 20px;
        margin-left: 5px;
        cursor: pointer;
    }
    
    .quick-start {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
    }
    
    .roi-highlight {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-weight: bold;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Help functions
def show_help_tip(title, content, tip_type="help"):
    if tip_type == "implementation":
        css_class = "implementation-tip"
        icon = "💡"
    elif tip_type == "leadership":
        css_class = "leadership-insight"
        icon = "🎯"
    elif tip_type == "warning":
        css_class = "warning-box"
        icon = "⚠️"
    else:
        css_class = "help-tip"
        icon = "ℹ️"
    
    st.markdown(f"""
    <div class="{css_class}">
        <h4>{icon} {title}</h4>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

def create_expandable_help(title, content):
    with st.expander(f"ℹ️ {title}", expanded=False):
        st.markdown(content)

# Sidebar with enhanced navigation
st.sidebar.markdown("""
<div class="quick-start">
    <h3>🚀 Quick Start Guide</h3>
    <p><strong>For Leadership:</strong> Start with Executive Overview to see high-level impact and ROI</p>
    <p><strong>For Technical Teams:</strong> Explore Data Strategy and AI Implementation sections</p>
    <p><strong>For Project Managers:</strong> Check Change Management and Project Portfolio</p>
</div>
""", unsafe_allow_html=True)

# Main navigation
page = st.sidebar.selectbox(
    "Select Focus Area",
    ["Executive Overview", "Data Strategy Framework", "AI Strategy & Implementation", 
     "Change Management", "Analytics Solutions", "Innovation Culture", "Project Portfolio"]
)

# Help sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Help & Resources")

if st.sidebar.button("💬 Implementation Guidance"):
    st.sidebar.success("Check the tip boxes throughout each section for specific implementation guidance!")

if st.sidebar.button("📈 ROI Calculator"):
    st.sidebar.info("Use the metrics in each section to build your business case. Look for the green ROI highlight boxes!")

if st.sidebar.button("🎯 Leadership Tips"):
    st.sidebar.warning("Look for blue leadership insight boxes for executive-level guidance!")

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
    # Header with help
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Strategic Innovation Portfolio</h1>
        <h3>Data & AI Enablement Excellence</h3>
        <p>Transforming organizations through strategic data initiatives and AI-powered innovation</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_help_tip("For Leadership Teams", 
                  "This dashboard provides executive-level insights into our data and AI capabilities. Use these metrics to understand current impact and plan strategic investments. Each metric includes growth trends to show momentum.", 
                  "leadership")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Projects", "47", "↗️ 23%")
        create_expandable_help("Active Projects Explained", 
                              "**What this means:** Number of concurrent data/AI initiatives across all business units.\n\n**Why it matters:** Shows organizational commitment and resource allocation to data-driven innovation.\n\n**Industry benchmark:** Leading companies typically run 30-60 concurrent data projects.")
    
    with col2:
        st.metric("AI Models Deployed", "23", "↗️ 156%")
        create_expandable_help("AI Models in Production", 
                              "**What this means:** Machine learning models actively running in production systems.\n\n**Why it matters:** Demonstrates successful AI implementation beyond pilots.\n\n**Success factors:** Each model requires ongoing monitoring, maintenance, and performance tracking.")
    
    with col3:
        st.metric("Data Sources Integrated", "127", "↗️ 34%")
        create_expandable_help("Data Integration Success", 
                              "**What this means:** Connected data systems feeding our analytics platform.\n\n**Why it matters:** More integrated data sources = better insights and decision-making.\n\n**Next steps:** Focus on data quality and real-time integration capabilities.")
    
    with col4:
        st.metric("ROI Generated", "$4.2M", "↗️ 89%")
        create_expandable_help("Return on Investment", 
                              "**How calculated:** Cost savings + revenue generation + risk mitigation value.\n\n**Breakdown:** 45% cost reduction, 40% revenue growth, 15% risk mitigation.\n\n**Payback period:** Average of 14 months for data/AI projects.")
    
    st.markdown("""
    <div class="roi-highlight">
        💰 Key Leadership Insight: Every $1 invested in data/AI initiatives generates $3.80 in measurable business value
    </div>
    """, unsafe_allow_html=True)
    
    # Strategic overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Strategic Value Proposition")
        
        show_help_tip("Implementation Roadmap", 
                      "Start with Data Strategy Framework to establish foundation, then move to AI Strategy for advanced capabilities. Change Management is critical throughout the journey.", 
                      "implementation")
        
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
        
        create_expandable_help("How to Read This Chart", 
                              "**Projects Completed:** Successfully delivered initiatives generating measurable value\n\n**Teams Enabled:** Business units actively using new data/AI capabilities\n\n**Growth trend:** Shows accelerating adoption and organizational capability building")
    
    with col2:
        st.subheader("Innovation Highlights")
        
        show_help_tip("Quick Wins for Leadership", 
                      "These represent 'lighthouse' projects that demonstrate value quickly and build momentum for larger initiatives. Each took 3-6 months to implement.", 
                      "leadership")
        
        highlights = [
            {"title": "AI-Powered Analytics Platform", "impact": "340% faster insights", "icon": "🤖", 
             "tip": "Automated report generation saves 15 hours/week per analyst"},
            {"title": "Automated Data Pipeline", "impact": "85% reduction in processing time", "icon": "⚡",
             "tip": "Real-time data availability enables faster decision-making"},
            {"title": "ML-Driven Forecasting", "impact": "23% improvement in accuracy", "icon": "🎯",
             "tip": "Better predictions reduce inventory costs and improve customer satisfaction"},
            {"title": "Real-time Dashboard Suite", "impact": "100% executive adoption", "icon": "📊",
             "tip": "Self-service analytics reduces dependence on IT for basic reporting"}
        ]
        
        for highlight in highlights:
            with st.expander(f"{highlight['icon']} {highlight['title']}", expanded=False):
                st.markdown(f"**Impact:** {highlight['impact']}")
                st.markdown(f"💡 **Leadership Tip:** {highlight['tip']}")

elif page == "Data Strategy Framework":
    st.markdown("""
    <div class="main-header">
        <h1>Data Strategy Framework</h1>
        <p>Comprehensive approach to data governance, architecture, and value creation</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_help_tip("Strategic Context", 
                  "Data strategy is the foundation for AI success. Without proper data governance and architecture, AI initiatives will struggle. This framework shows the pathway from data chaos to data-driven decision making.", 
                  "leadership")
    
    tab1, tab2, tab3 = st.tabs(["🏗️ Architecture", "🛡️ Governance", "💰 Value Framework"])
    
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
            
            show_help_tip("Technology Selection Guide", 
                          "Start with cloud-native solutions for faster implementation. Prioritize platforms that support both traditional analytics and AI/ML workloads to avoid future migration costs.", 
                          "implementation")
        
        with col2:
            # Architecture maturity assessment
            fig = create_maturity_chart()
            st.plotly_chart(fig, use_container_width=True)
            
            create_expandable_help("Understanding the Maturity Chart", 
                                  "**Current State (Blue):** Where we are today based on assessments\n\n**Target State (Purple):** Industry best practices and organizational goals\n\n**Gap Analysis:** Larger gaps indicate priority areas for investment\n\n**Timeline:** Typically 12-18 months to achieve target state with proper resourcing")
        
        st.subheader("Implementation Roadmap")
        
        show_help_tip("Executive Decision Point", 
                      "This roadmap requires sustained executive commitment. Each phase builds on the previous, so skipping phases leads to failure. Budget for both technology and change management.", 
                      "leadership")
        
        roadmap_data = pd.DataFrame({
            'Phase': ['Foundation', 'Integration', 'Analytics', 'AI/ML', 'Innovation'],
            'Duration (Months)': [3, 4, 3, 6, 12],
            'Investment ($K)': [150, 300, 200, 500, 800],
            'Expected ROI': [1.5, 2.3, 3.1, 4.2, 6.8],
            'Key Activities': [
                'Data governance, basic infrastructure',
                'Source system integration, data quality',
                'Self-service analytics, dashboards',
                'ML models, automation, AI applications',
                'Advanced AI, innovation culture'
            ]
        })
        
        st.dataframe(roadmap_data, use_container_width=True)
        
        create_expandable_help("Roadmap Success Factors", 
                              "**Critical Success Factors:**\n\n1. **Executive Sponsorship:** Sustained leadership support throughout journey\n\n2. **Cross-functional Teams:** Include business, IT, and data teams from day one\n\n3. **Change Management:** Invest 20-30% of budget in people and process change\n\n4. **Quick Wins:** Deliver value every 3-6 months to maintain momentum")
    
    with tab2:
        st.subheader("Data Governance Excellence")
        
        show_help_tip("Why Governance Matters", 
                      "Poor data governance is the #1 reason AI projects fail. Invest in governance early to avoid costly rework and ensure regulatory compliance.", 
                      "warning")
        
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
            
            show_help_tip("Getting Started with Governance", 
                          "Begin with data cataloging and classification. Establish clear ownership and stewardship roles. Implement automated monitoring before adding complex compliance rules.", 
                          "implementation")
        
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
            
            create_expandable_help("Governance KPI Benchmarks", 
                                  "**Industry Standards:**\n\n• Data Quality: 90%+ for tier-1 data\n\n• Compliance: 98%+ for regulated industries\n\n• Catalog Coverage: 85%+ of active data assets\n\n• User Adoption: 80%+ of target users actively using self-service tools")
    
    with tab3:
        st.subheader("Data Value Framework")
        
        st.markdown("""
        **💰 Value Creation Model:**
        
        Our systematic approach to measuring and maximizing data value across the organization.
        """)
        
        show_help_tip("Building Your Business Case", 
                      "Use this framework to quantify data initiatives. Start with cost reduction (easier to measure), then progress to revenue generation and innovation value.", 
                      "leadership")
        
        # Value framework visualization
        col1, col2 = st.columns(2)
        
        with col1:
            value_categories = ['Cost Reduction', 'Revenue Growth', 'Risk Mitigation', 'Innovation']
            value_amounts = [1200000, 2800000, 800000, 1500000]
            
            fig = px.pie(values=value_amounts, names=value_categories, 
                        title="Data Value Distribution ($)")
            st.plotly_chart(fig, use_container_width=True)
            
            create_expandable_help("Value Measurement Tips", 
                                  "**Cost Reduction:** Process automation, resource optimization\n\n**Revenue Growth:** Customer insights, market intelligence\n\n**Risk Mitigation:** Fraud detection, compliance automation\n\n**Innovation:** New products, services, market opportunities")
        
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
            
            st.markdown("""
            <div class="roi-highlight">
                🎯 Total Annual Value: $6.3M<br>
                ROI: 380% over 2 years
            </div>
            """, unsafe_allow_html=True)

elif page == "AI Strategy & Implementation":
    st.markdown("""
    <div class="main-header">
        <h1>AI Strategy & Implementation</h1>
        <p>Enterprise AI adoption roadmap and implementation excellence</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_help_tip("AI Implementation Reality Check", 
                  "80% of AI projects fail due to poor data foundation or lack of change management. Success requires strong data strategy, clear use cases, and organizational readiness.", 
                  "warning")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Strategy", "⚙️ Implementation", "🎪 Use Cases", "🔬 Innovation Lab"])
    
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
            
            show_help_tip("AI Strategy Success Factors", 
                          "Focus on business outcomes, not technology. Start with high-impact, low-complexity use cases. Build internal AI literacy before attempting complex implementations.", 
                          "implementation")
        
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
            
            create_expandable_help("AI Maturity Stages Explained", 
                                  "**Basic Analytics (95%):** Descriptive reporting, dashboards\n\n**Predictive Models (78%):** Forecasting, classification models\n\n**AI Applications (45%):** NLP, computer vision, automation\n\n**AI-First Culture (23%):** Organization-wide AI adoption, continuous innovation")
    
    with tab2:
        st.subheader("Implementation Excellence")
        
        show_help_tip("MLOps Best Practice", 
                      "Treat AI models like software products. Implement proper DevOps practices including version control, testing, monitoring, and automated deployment pipelines.", 
                      "implementation")
        
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
            
            create_expandable_help("MLOps Implementation Timeline", 
                                  "**Month 1-3:** Basic CI/CD setup\n\n**Month 4-6:** Monitoring and alerting\n\n**Month 7-9:** Automated retraining\n\n**Month 10-12:** Advanced governance and ethics framework")
        
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
            
            show_help_tip("Technology Investment Strategy", 
                          "Invest in cloud-native, open-source solutions where possible. Avoid vendor lock-in by choosing platforms with strong ecosystem support and migration paths.", 
                          "implementation")
    
    with tab3:
        st.subheader("AI Use Cases Portfolio")
        
        show_help_tip("Use Case Selection Criteria", 
                      "Prioritize use cases with: 1) Clear business value, 2) Available quality data, 3) Stakeholder buy-in, 4) Measurable success metrics. Avoid 'science projects' without clear ROI.", 
                      "leadership")
        
        use_cases = pd.DataFrame({
            'Use Case': ['Customer Churn Prediction', 'Demand Forecasting', 'Quality Control', 
                        'Fraud Detection', 'Recommendation Engine', 'Process Optimization'],
            'Business Unit': ['Sales', 'Operations', 'Manufacturing', 'Finance', 'Marketing', 'Operations'],
            'ROI ($K)': [450, 320, 680, 890, 540, 380],
            'Implementation Status': ['Production', 'Pilot', 'Production', 'Production', 'Development', 'Pilot'],
            'Complexity': ['Medium', 'High', 'Medium', 'High', 'Medium', 'High'],
            'Timeline (Months)': [4, 6, 5, 8, 4, 7]
        })
        
        st.dataframe(use_cases, use_container_width=True)
        
        # Interactive use case explorer
        st.subheader("Use Case Details")
        selected_use_case = st.selectbox("Select use case for detailed breakdown:", use_cases['Use Case'].tolist())
        
        if selected_use_case:
            case_details = {
                'Customer Churn Prediction': {
                    'description': 'Predict which customers are likely to cancel subscriptions',
                    'benefits': 'Reduce churn by 15%, increase customer lifetime value',
                    'requirements': 'Customer behavior data, transaction history, support interactions',
                    'success_metrics': 'Churn rate reduction, retention campaign effectiveness'
                },
                'Demand Forecasting': {
                    'description': 'Predict future demand for products and services',
                    'benefits': 'Optimize inventory, reduce waste, improve customer satisfaction',
                    'requirements': 'Historical sales data, market trends, external factors',
                    'success_metrics': 'Forecast accuracy, inventory turnover, stockout reduction'
                }
                # Add more case details as needed
            }
            
            if selected_use_case in case_details:
                details = case_details[selected_use_case]
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Description:** {details['description']}")
                    st.markdown(f"**Business Benefits:** {details['benefits']}")
                
                with col2:
                    st.markdown(f"**Data Requirements:** {details['requirements']}")
                    st.markdown(f"**Success Metrics:** {details['success_metrics']}")
        
        # ROI visualization
        fig = px.bar(use_cases, x='Use Case', y='ROI ($K)', 
                    color='Implementation Status',
                    title="AI Use Cases ROI Analysis")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        create_expandable_help("ROI Calculation Methodology", 
                              "**ROI Components:**\n\n• Direct cost savings from automation\n\n• Revenue increase from better decisions\n\n• Risk reduction value\n\n• Productivity gains from augmented intelligence\n\n**Timeline:** ROI calculated over 24-month period post-implementation")
    
    with tab4:
        st.subheader("AI Innovation Lab")
        
        show_help_tip("Innovation Lab Purpose", 
                      "The innovation lab explores emerging technologies and validates new use cases. It's designed for rapid experimentation with controlled risk and clear success criteria.", 
                      "leadership")
        
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
            
            show_help_tip("Innovation Lab Operations", 
                          "Allocate 10-15% of AI budget to innovation lab. Set 90-day experiment cycles with clear go/no-go criteria. Focus on technologies 6-18 months from mainstream adoption.", 
                          "implementation")
        
        with col2:
            # Innovation pipeline
            fig = create_innovation_pipeline()
            st.plotly_chart(fig, use_container_width=True)
            
            create_expandable_help("Innovation Pipeline Explained", 
                                  "**Ideation (24):** Raw ideas from employees, customers, market research\n\n**Proof of Concept (12):** Technical validation in controlled environment\n\n**Pilot (8):** Real-world testing with limited scope\n\n**Scale (5):** Broader implementation across business units\n\n**Production (3):** Full deployment with operational support")

elif page == "Change Management":
    st.markdown("""
    <div class="main-header">
        <h1>🔄 Change Management Excellence</h1>
        <p>Proven methodologies for successful technology adoption and transformation</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_help_tip("Change Management Critical Success Factor", 
                  "Technical implementation is only 30% of transformation success. The other 70% is people, process, and cultural change. Invest accordingly.", 
                  "leadership")
    
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
            
            show_help_tip("ADKAR Implementation Tips", 
                          "Address each ADKAR element sequentially. Don't move to 'Knowledge' training until 'Awareness' and 'Desire' are established. Each element requires different tactics and timelines.", 
                          "implementation")
        
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
            
            create_expandable_help("Readiness Assessment Guide", 
                                  "**Scores below 3.0:** High risk - address before major initiatives\n\n**Scores 3.0-3.5:** Moderate risk - targeted interventions needed\n\n**Scores 3.5+:** Good readiness - proceed with confidence\n\n**Leadership Support is critical:** All other factors depend on this")
    
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
            
            show_help_tip("Managing Resistance", 
                          "Resistance is normal and often contains valuable insights. Listen to concerns, address root causes, and provide extra support. Never ignore or dismiss resistance.", 
                          "implementation")
        
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
            
            create_expandable_help("Engagement Strategy Tips", 
                                  "**Weeks 1-4:** Focus on building awareness and initial support\n\n**Weeks 5-8:** Intensive education and skill building\n\n**Weeks 9-12:** Reinforcement and sustainability measures\n\n**Key milestone:** 80% supporter + champion rate by week 10")
    
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
        
        show_help_tip("Measuring Change Success", 
                      "Track both leading indicators (training completion, engagement) and lagging indicators (productivity, satisfaction). Leading indicators predict success 6-8 weeks in advance.", 
                      "implementation")
        
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
        
        create_expandable_help("Impact Measurement Methodology", 
                              "**Baseline:** Pre-change measurements across all key metrics\n\n**Progress:** Monthly tracking during implementation\n\n**Target:** Industry benchmarks and organizational goals\n\n**Success criteria:** Achieve or exceed targets within 12 months")

elif page == "Analytics Solutions":
    st.markdown("""
    <div class="main-header">
        <h1>📈 Analytics Solutions</h1>
        <p>Enterprise analytics platform and self-service capabilities</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_help_tip("Analytics Strategy Overview", 
                  "Self-service analytics reduces IT bottlenecks by 70% and accelerates decision-making. Focus on user experience and data literacy alongside technical capabilities.", 
                  "leadership")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Dashboard", "🔍 Advanced Analytics", "🤖 Predictive Models", "🛠️ Self-Service Platform"])
    
    with tab1:
        st.subheader("Executive Dashboard Suite")
        
        # Sample executive metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Monthly Revenue", "$2.4M", "↗️ 12%")
        with col2:
            st.metric("Customer Satisfaction", "4.2/5", "↗️ 0.3")
        with col3:
            st.metric("Operational Efficiency", "87%", "↗️ 5%")
        with col4:
            st.metric("Market Share", "23.4%", "↗️ 1.2%")
        with col5:
            st.metric("Innovation Rate", "156", "↗️ 34")
        
        show_help_tip("Executive Dashboard Best Practices", 
                      "Limit to 5-7 key metrics that directly tie to strategic objectives. Update frequency should match decision-making cycles. Include context and benchmarks for each metric.", 
                      "implementation")
        
        # Revenue trend analysis
        revenue_data = pd.DataFrame({
            'Month': pd.date_range('2024-01-01', periods=12, freq='M'),
            'Revenue': np.random.normal(2400000, 200000, 12).cumsum() / 12,
            'Target': [2200000] * 12,
            'Forecast': np.linspace(2400000, 2800000, 12)
        })
        
        fig = px.line(revenue_data, x='Month', y=['Revenue', 'Target', 'Forecast'],
                     title="Revenue Performance vs Target vs Forecast")
        st.plotly_chart(fig, use_container_width=True)
        
        create_expandable_help("Dashboard Design Principles", 
                              "**Visual Hierarchy:** Most important metrics prominently displayed\n\n**Actionable Insights:** Include context that enables decision-making\n\n**Real-time Updates:** Critical metrics update automatically\n\n**Mobile Optimization:** Executives access dashboards on mobile devices")
    
    with tab2:
        st.subheader("Advanced Analytics Capabilities")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🔬 Analytical Techniques:**
            
            **Customer Analytics:**
            - Segmentation and persona development
            - Lifetime value modeling
            - Behavior pattern analysis
            - Journey mapping and optimization
            
            **Operational Analytics:**
            - Process mining and optimization
            - Resource utilization analysis
            - Quality metrics and control charts
            - Performance benchmarking
            
            **Financial Analytics:**
            - Profitability analysis by segment
            - Cost driver identification
            - Budget variance analysis
            - Risk assessment modeling
            """)
            
            show_help_tip("Advanced Analytics Implementation", 
                          "Start with descriptive analytics (what happened), then diagnostic (why), predictive (what will happen), and finally prescriptive (what should we do). Each level builds on the previous.", 
                          "implementation")
        
        with col2:
            # Sample customer segmentation
            segment_data = pd.DataFrame({
                'Segment': ['High Value', 'Growth Potential', 'At Risk', 'Cost Focused'],
                'Customers': [1250, 3400, 2100, 4800],
                'Avg Value': [5200, 1800, 2400, 800],
                'Retention': [94, 87, 62, 78]
            })
            
            fig = px.scatter(segment_data, x='Customers', y='Avg Value', size='Retention',
                           text='Segment', title="Customer Segment Analysis")
            st.plotly_chart(fig, use_container_width=True)
            
            create_expandable_help("Customer Segmentation Insights", 
                                  "**High Value:** Focus on retention and upselling\n\n**Growth Potential:** Investment in relationship building\n\n**At Risk:** Immediate intervention required\n\n**Cost Focused:** Automation and efficiency focus")
    
    with tab3:
        st.subheader("Predictive Models Portfolio")
        
        show_help_tip("Model Performance Standards", 
                      "Establish minimum performance thresholds before deployment. Monitor model drift monthly. Retrain when performance drops below 85% of baseline accuracy.", 
                      "implementation")
        
        models_data = pd.DataFrame({
            'Model Name': ['Churn Prediction', 'Sales Forecast', 'Demand Planning', 'Price Optimization', 'Risk Assessment'],
            'Business Impact': ['High', 'High', 'Medium', 'High', 'Medium'],
            'Accuracy (%)': [87, 92, 78, 83, 89],
            'Status': ['Production', 'Production', 'Testing', 'Production', 'Development'],
            'Last Updated': ['2024-08-15', '2024-08-20', '2024-08-10', '2024-08-18', '2024-08-25'],
            'Monthly Predictions': [15000, 5000, 12000, 8000, 3000]
        })
        
        st.dataframe(models_data, use_container_width=True)
        
        # Model performance visualization
        fig = px.scatter(models_data, x='Monthly Predictions', y='Accuracy (%)', 
                        color='Business Impact', size='Monthly Predictions',
                        title="Model Performance vs Usage")
        st.plotly_chart(fig, use_container_width=True)
        
        create_expandable_help("Model Governance Framework", 
                              "**Performance Monitoring:** Automated alerts when accuracy drops\n\n**Business Impact Tracking:** Measure actual value generated\n\n**Model Lifecycle Management:** Regular review and retirement process\n\n**Explainability Requirements:** All production models must be interpretable")
    
    with tab4:
        st.subheader("Self-Service Analytics Platform")
        
        show_help_tip("Self-Service Success Strategy", 
                      "Democratize data access while maintaining governance. Provide guided analytics experiences for business users. Invest heavily in training and support during rollout.", 
                      "leadership")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🛠️ Platform Capabilities:**
            
            **No-Code Analytics:**
            - Drag-and-drop report builder
            - Automated insight generation
            - Natural language query interface
            - Template library for common analyses
            
            **Data Exploration:**
            - Interactive data visualization
            - Statistical analysis tools
            - Data profiling and quality checks
            - Export and sharing capabilities
            
            **Collaboration Features:**
            - Shared workspaces and projects
            - Comment and annotation tools
            - Version control for analyses
            - Publishing and distribution workflows
            """)
        
        with col2:
            # Platform usage metrics
            usage_data = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'Active Users': [45, 67, 89, 124, 156, 203],
                'Reports Created': [120, 180, 245, 320, 410, 520],
                'Data Queries': [890, 1200, 1650, 2100, 2800, 3500]
            })
            
            fig = px.line(usage_data, x='Month', y=['Active Users', 'Reports Created'],
                         title="Self-Service Platform Adoption")
            st.plotly_chart(fig, use_container_width=True)
            
            create_expandable_help("Usage Growth Patterns", 
                                  "**Typical Adoption Curve:**\n\n• Month 1-2: Early adopters (15%)\n\n• Month 3-6: Early majority (35%)\n\n• Month 7-12: Late majority (35%)\n\n• Month 12+: Laggards (15%)")

elif page == "Innovation Culture":
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Innovation Culture</h1>
        <p>Building learning organizations that thrive with emerging technologies</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_help_tip("Culture as Competitive Advantage", 
                  "Organizations with strong data/AI cultures are 5x more likely to be top performers. Culture change takes 18-24 months but provides sustainable competitive advantage.", 
                  "leadership")
    
    tab1, tab2, tab3 = st.tabs(["🏛️ Cultural Framework", "📚 Learning & Development", "🤝 Communities of Practice"])
    
    with tab1:
        st.subheader("Innovation Culture Framework")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            **🎯 Cultural Pillars:**
            
            **Data-Driven Decision Making:**
            - Evidence-based reasoning as default
            - Hypothesis-driven experimentation
            - Metrics and KPIs for all initiatives
            - Data literacy across all roles
            
            **Continuous Learning:**
            - Dedicated time for skill development
            - Failure tolerance and learning from mistakes
            - Knowledge sharing and collaboration
            - External learning and conference participation
            
            **Innovation Mindset:**
            - Curiosity and questioning status quo
            - Rapid prototyping and iteration
            - Customer-centric thinking
            - Cross-functional collaboration
            
            **Technology Adoption:**
            - Openness to new tools and methods
            - Early adoption of proven technologies
            - User feedback and iterative improvement
            - Change as opportunity, not threat
            """)
            
            show_help_tip("Building Innovation Culture", 
                          "Culture change requires consistent leadership behavior, clear expectations, and reward systems that reinforce desired behaviors. Celebrate both successes and intelligent failures.", 
                          "implementation")
        
        with col2:
            # Culture assessment
            culture_metrics = pd.DataFrame({
                'Dimension': ['Data Literacy', 'Innovation Mindset', 'Collaboration', 'Learning Agility', 'Tech Adoption'],
                'Current Score': [3.4, 3.8, 4.1, 3.6, 3.2],
                'Industry Average': [2.8, 3.2, 3.5, 3.1, 2.9]
            })
            
            fig = px.bar(culture_metrics, x='Dimension', y=['Current Score', 'Industry Average'],
                        title="Cultural Assessment vs Industry", barmode='group')
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
            
            create_expandable_help("Culture Measurement", 
                                  "**Assessment Method:** Annual survey + behavioral observation\n\n**Benchmark:** Industry data from 500+ companies\n\n**Target:** Top quartile performance (4.0+ on 5-point scale)\n\n**Frequency:** Quarterly pulse surveys, annual deep dive")
    
    with tab2:
        st.subheader("Learning & Development Programs")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📚 Curriculum Overview:**
            
            **Data Literacy Track (All Employees):**
            - Data fundamentals and terminology
            - Basic statistics and analysis
            - Data visualization principles
            - Critical thinking with data
            
            **Analytics Professional Track:**
            - Advanced statistical methods
            - Data science tools and techniques
            - Machine learning fundamentals
            - Business intelligence platforms
            
            **AI Leadership Track (Managers):**
            - AI strategy and governance
            - Ethical AI considerations
            - Change management for AI adoption
            - AI project management
            
            **Technical Specialist Track:**
            - Advanced ML/AI techniques
            - Platform engineering and MLOps
            - Data engineering and architecture
            - Research and innovation methods
            """)
            
            show_help_tip("L&D Investment Strategy", 
                          "Allocate 3-5% of total budget to learning and development. Mix internal training, external courses, conferences, and hands-on projects. Track skill development with competency assessments.", 
                          "implementation")
        
        with col2:
            # Learning metrics
            learning_data = pd.DataFrame({
                'Program': ['Data Literacy', 'Analytics Pro', 'AI Leadership', 'Technical Specialist'],
                'Participants': [450, 120, 45, 35],
                'Completion Rate': [92, 87, 96, 89],
                'Satisfaction': [4.3, 4.1, 4.6, 4.2],
                'Skill Improvement': [78, 85, 82, 91]
            })
            
            fig = px.scatter(learning_data, x='Participants', y='Satisfaction', 
                           size='Skill Improvement', color='Program',
                           title="Learning Program Performance")
            st.plotly_chart(fig, use_container_width=True)
            
            create_expandable_help("Program Success Metrics", 
                                  "**Completion Rate:** Target >85% for mandatory programs\n\n**Satisfaction:** Target >4.0 on 5-point scale\n\n**Skill Improvement:** Pre/post assessments showing knowledge gain\n\n**Business Impact:** Application of skills in real projects")
    
    with tab3:
        st.subheader("Communities of Practice")
        
        show_help_tip("Communities Drive Innovation", 
                      "Communities of practice accelerate learning by 40% and increase innovation by 25%. They're essential for scaling data/AI capabilities across large organizations.", 
                      "leadership")
        
        col1, col2 = st.columns(2)
        
        with col1:
            communities_data = pd.DataFrame({
                'Community': ['Data Scientists', 'Business Analysts', 'AI Ethics', 'Data Engineers', 'Citizen Developers'],
                'Members': [45, 120, 35, 28, 89],
                'Monthly Sessions': [4, 6, 2, 3, 8],
                'Knowledge Artifacts': [23, 45, 12, 18, 34],
                'Cross-Collaboration Score': [4.2, 3.8, 4.5, 3.9, 4.1]
            })
            
            st.dataframe(communities_data, use_container_width=True)
            
            show_help_tip("Community Activation Strategy", 
                          "Provide dedicated time, physical/virtual spaces, and executive sponsorship. Measure impact through knowledge artifacts created and cross-team collaborations initiated.", 
                          "implementation")
        
        with col2:
            # Community engagement metrics
            fig = px.bar(communities_data, x='Community', y='Members',
                        title="Community Membership Growth")
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
            
            create_expandable_help("Community Health Indicators", 
                                  "**Healthy Growth:** 15-20% monthly membership increase\n\n**Active Participation:** 60%+ attending monthly sessions\n\n**Knowledge Creation:** 1+ artifact per member per quarter\n\n**Cross-Pollination:** Regular collaboration between communities")

elif page == "Project Portfolio":
    st.markdown("""
    <div class="main-header">
        <h1>📋 Project Portfolio</h1>
        <p>Strategic project management and portfolio optimization</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_help_tip("Portfolio Management Strategy", 
                  "Balance quick wins (20%), core capabilities (60%), and breakthrough innovations (20%). This ensures continuous value delivery while building long-term competitive advantage.", 
                  "leadership")
    
    tab1, tab2, tab3 = st.tabs(["📊 Portfolio Overview", "⚡ Performance Analytics", "🎯 Resource Management"])
    
    with tab1:
        st.subheader("Active Project Portfolio")
        
        # Enhanced project data
        projects_data = pd.DataFrame({
            'Project Name': [
                'Customer 360 Platform', 'AI Chatbot Implementation', 'Predictive Maintenance',
                'Real-time Analytics Dashboard', 'Data Lake Migration', 'ML Recommendation Engine',
                'Process Automation Suite', 'Advanced Forecasting Model', 'Data Quality Framework'
            ],
            'Business Unit': ['Sales', 'Customer Service', 'Operations', 'Executive', 'IT', 'Marketing', 'Finance', 'Operations', 'Data Office'],
            'Status': ['In Progress', 'Testing', 'Production', 'In Progress', 'Planning', 'Development', 'Production', 'Testing', 'In Progress'],
            'Budget ($K)': [450, 180, 320, 220, 680, 280, 520, 150, 200],
            'Actual Spend ($K)': [380, 165, 310, 200, 120, 210, 485, 140, 150],
            'Expected ROI': [3.2, 4.1, 2.8, 5.2, 1.8, 3.9, 2.5, 3.6, 2.2],
            'Completion (%)': [75, 90, 100, 60, 20, 70, 95, 85, 45],
            'Risk Level': ['Medium', 'Low', 'Low', 'Medium', 'High', 'Medium', 'Low', 'Medium', 'Medium'],
            'Strategic Priority': ['High', 'Medium', 'High', 'High', 'Medium', 'Medium', 'High', 'Medium', 'High']
        })
        
        st.dataframe(projects_data, use_container_width=True)
        
        show_help_tip("Portfolio Filtering", 
                      "Use the interactive elements below to filter and analyze projects by different criteria. This helps identify patterns and optimization opportunities.", 
                      "implementation")
        
        # Interactive filtering
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.multiselect("Filter by Status", 
                                         projects_data['Status'].unique(),
                                         default=projects_data['Status'].unique())
        
        with col2:
            priority_filter = st.multiselect("Filter by Priority",
                                           projects_data['Strategic Priority'].unique(),
                                           default=projects_data['Strategic Priority'].unique())
        
        with col3:
            risk_filter = st.multiselect("Filter by Risk Level",
                                       projects_data['Risk Level'].unique(),
                                       default=projects_data['Risk Level'].unique())
        
        # Apply filters
        filtered_data = projects_data[
            (projects_data['Status'].isin(status_filter)) &
            (projects_data['Strategic Priority'].isin(priority_filter)) &
            (projects_data['Risk Level'].isin(risk_filter))
        ]
        
        # Portfolio summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Projects", len(filtered_data))
        with col2:
            st.metric("Total Budget", f"${filtered_data['Budget ($K)'].sum()}K")
        with col3:
            st.metric("Avg Completion", f"{filtered_data['Completion (%)'].mean():.0f}%")
        with col4:
            st.metric("Avg Expected ROI", f"{filtered_data['Expected ROI'].mean():.1f}x")
    
    with tab2:
        st.subheader("Performance Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Project status distribution
            status_counts = projects_data['Status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index,
                        title="Project Status Distribution")
            st.plotly_chart(fig, use_container_width=True)
            
            create_expandable_help("Portfolio Health Indicators", 
                                  "**Healthy Portfolio:**\n\n• 60-70% projects in progress/testing\n\n• 20-30% in production\n\n• 10-20% in planning\n\n• <10% projects stalled or cancelled")
        
        with col2:
            # ROI vs Budget analysis
            fig = px.scatter(projects_data, x='Budget ($K)', y='Expected ROI',
                           color='Risk Level', size='Completion (%)',
                           title="ROI vs Investment Analysis")
            st.plotly_chart(fig, use_container_width=True)
            
            show_help_tip("Investment Optimization", 
                          "Look for high ROI, low risk projects in upper left quadrant. These are your best opportunities for quick wins and momentum building.", 
                          "implementation")
    
    with tab3:
        st.subheader("Resource Allocation Analysis")
        
        # Resource allocation by business unit
        resource_data = projects_data.groupby('Business Unit').agg({
            'Budget ($K)': 'sum',
            'Expected ROI': 'mean',
            'Project Name': 'count'
        }).rename(columns={'Project Name': 'Project Count'}).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(resource_data, x='Business Unit', y='Budget ($K)',
                        title="Budget Allocation by Business Unit")
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(resource_data, x='Project Count', y='Expected ROI',
                           size='Budget ($K)', color='Business Unit',
                           title="Projects vs ROI by Business Unit")
            st.plotly_chart(fig, use_container_width=True)
        
        show_help_tip("Resource Optimization Strategy", 
                      "Balance investments across business units while prioritizing areas with highest strategic impact. Ensure each unit has at least one success story to build momentum.", 
                      "leadership")
        
        create_expandable_help("Resource Planning Best Practices", 
                              "**Portfolio Balance:**\n\n• 40% sustaining projects (maintain current capabilities)\n\n• 40% growth projects (expand capabilities)\n\n• 20% transformational projects (breakthrough innovation)\n\n**Risk Management:** No more than 30% of portfolio in high-risk projects")

# Footer with action items
st.markdown("---")
st.markdown("""
<div class="quick-start">
    <h3>🎯 Next Steps for Leadership</h3>
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
        <div>
            <h4>📅 Immediate (30 days)</h4>
            <ul>
                <li>Review current data maturity assessment</li>
                <li>Identify quick win opportunities</li>
                <li>Establish executive sponsorship</li>
                <li>Begin stakeholder engagement</li>
            </ul>
        </div>
        <div>
            <h4>⚡ Short-term (90 days)</h4>
            <ul>
                <li>Develop detailed implementation roadmap</li>
                <li>Secure budget and resources</li>
                <li>Launch pilot projects</li>
                <li>Begin training programs</li>
            </ul>
        </div>
        <div>
            <h4>🚀 Long-term (12 months)</h4>
            <ul>
                <li>Scale successful pilots</li>
                <li>Measure and optimize ROI</li>
                <li>Build innovation culture</li>
                <li>Plan next transformation wave</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Contact and support information
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📞 Implementation Support

**Ready to get started?**

🎯 **Strategy Consultation:** Executive workshops and roadmap development

📊 **Assessment Services:** Current state analysis and gap identification  

🚀 **Quick Start Package:** 90-day implementation accelerator

💡 **Training Programs:** Custom learning paths for your organization

Use this portfolio to build your business case and secure stakeholder buy-in for data and AI initiatives.
""")

if st.sidebar.button("📧 Schedule Leadership Briefing"):
    st.sidebar.success("Contact your data strategy team to schedule an executive briefing session!")

if st.sidebar.button("💼 Download Business Case Template"):
    st.sidebar.info("Business case templates available in the Project Portfolio section!")