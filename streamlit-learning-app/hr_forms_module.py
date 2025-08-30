import streamlit as st
import pandas as pd
import numpy as np
import datetime
import json
import time

def hr_forms_module():
    st.title("HR Forms & Data Collection in Streamlit")
    
    # Module introduction with context
    st.markdown("""
    ## Making Magic Company: People Insights
    
    Forms and data collection tools are essential for gathering employee feedback, conducting surveys,
    and collecting structured HR data. This module covers how to create effective HR forms and surveys using Streamlit.
    """)
    
    # Section 1: Basic HR Forms
    st.header("1. Basic HR Forms")
    
    # Use tabs for the learning components
    tab1, tab2, tab3 = st.tabs(["🔍 Live Example", "💻 Code", "📚 Explanation"])
    
    with tab1:
        st.subheader("Employee Information Form")
        
        # Create a simple employee information form
        with st.form("employee_info_form"):
            st.markdown("### Employee Information")
            
            # Employee basic information
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name*")
                last_name = st.text_input("Last Name*")
                employee_id = st.text_input("Employee ID", 
                                          help="Enter the employee ID if already assigned")
            
            with col2:
                email = st.text_input("Email Address*", 
                                    placeholder="name@makingmagic.com")
                phone = st.text_input("Phone Number", 
                                    placeholder="(555) 555-5555")
                hire_date = st.date_input("Hire Date*", 
                                        value=datetime.datetime.now().date())
            
            # Department and role information
            st.markdown("### Department and Role")
            
            col1, col2 = st.columns(2)
            with col1:
                department = st.selectbox(
                    "Department*",
                    options=[
                        "Engineering", 
                        "Product", 
                        "Marketing", 
                        "Sales", 
                        "Customer Support", 
                        "Finance", 
                        "HR", 
                        "Operations", 
                        "Research", 
                        "Legal"
                    ]
                )
                
                job_title = st.text_input("Job Title*")
            
            with col2:
                job_level = st.selectbox(
                    "Job Level*",
                    options=[
                        "Entry", 
                        "Associate", 
                        "Mid-Level", 
                        "Senior", 
                        "Manager", 
                        "Director", 
                        "VP", 
                        "Executive"
                    ]
                )
                
                manager = st.text_input("Manager Name")
            
            # Additional information
            st.markdown("### Additional Information")
            
            location = st.selectbox(
                "Location",
                options=[
                    "Orlando", 
                    "New York", 
                    "San Francisco", 
                    "Chicago", 
                    "Austin", 
                    "Remote"
                ]
            )
            
            notes = st.text_area("Notes", 
                               placeholder="Add any additional information about the employee")
            
            # Required field notice
            st.markdown("**Fields marked with * are required**")
            
            # Submit button
            submitted = st.form_submit_button("Submit")
        
        # Handle form submission
        if submitted:
            # Validate required fields
            if not first_name or not last_name or not email:
                st.error("Please fill in all required fields.")
            elif not email.endswith("@makingmagic.com"):
                st.error("Please use a valid Making Magic company email address.")
            else:
                # Normally, this would save to a database or file
                # For demonstration, we'll just display the submitted data
                st.success("Employee information submitted successfully!")
                
                # Display the submitted data
                employee_data = {
                    "First Name": first_name,
                    "Last Name": last_name,
                    "Employee ID": employee_id if employee_id else "To be assigned",
                    "Email": email,
                    "Phone": phone,
                    "Hire Date": hire_date.strftime("%Y-%m-%d"),
                    "Department": department,
                    "Job Title": job_title,
                    "Job Level": job_level,
                    "Manager": manager,
                    "Location": location,
                    "Notes": notes
                }
                
                # Create two columns for display
                col1, col2 = st.columns(2)
                
                # Display the data nicely formatted
                with col1:
                    st.markdown("### Employee Details")
                    for key, value in list(employee_data.items())[:6]:
                        st.markdown(f"**{key}:** {value}")
                
                with col2:
                    st.markdown("### Role Details")
                    for key, value in list(employee_data.items())[6:]:
                        st.markdown(f"**{key}:** {value}")
    
    with tab2:
        # Store code snippets in variables
        form_code = """
# Create a simple employee information form
with st.form("employee_info_form"):
    st.markdown("### Employee Information")
    
    # Employee basic information
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name*")
        last_name = st.text_input("Last Name*")
        employee_id = st.text_input("Employee ID", 
                                  help="Enter the employee ID if already assigned")
    
    with col2:
        email = st.text_input("Email Address*", 
                            placeholder="name@makingmagic.com")
        phone = st.text_input("Phone Number", 
                            placeholder="(555) 555-5555")
        hire_date = st.date_input("Hire Date*", 
                                value=datetime.datetime.now().date())
    
    # Department and role information
    st.markdown("### Department and Role")
    
    col1, col2 = st.columns(2)
    with col1:
        department = st.selectbox(
            "Department*",
            options=[
                "Engineering", 
                "Product", 
                "Marketing", 
                "Sales", 
                "Customer Support", 
                "Finance", 
                "HR", 
                "Operations", 
                "Research", 
                "Legal"
            ]
        )
        
        job_title = st.text_input("Job Title*")
    
    with col2:
        job_level = st.selectbox(
            "Job Level*",
            options=[
                "Entry", 
                "Associate", 
                "Mid-Level", 
                "Senior", 
                "Manager", 
                "Director", 
                "VP", 
                "Executive"
            ]
        )
        
        manager = st.text_input("Manager Name")
    
    # Required field notice
    st.markdown("**Fields marked with * are required**")
    
    # Submit button
    submitted = st.form_submit_button("Submit")
"""
        
        validation_code = """
# Handle form submission
if submitted:
    # Validate required fields
    if not first_name or not last_name or not email:
        st.error("Please fill in all required fields.")
    elif not email.endswith("@makingmagic.com"):
        st.error("Please use a valid Making Magic company email address.")
    else:
        # Normally, this would save to a database or file
        # For demonstration, we'll just display the submitted data
        st.success("Employee information submitted successfully!")
        
        # Display the submitted data
        employee_data = {
            "First Name": first_name,
            "Last Name": last_name,
            "Email": email,
            # ... other fields ...
        }
        
        # Create two columns for display
        col1, col2 = st.columns(2)
        
        # Display the data nicely formatted
        with col1:
            st.markdown("### Employee Details")
            for key, value in list(employee_data.items())[:6]:
                st.markdown(f"**{key}:** {value}")
"""
        
        # Display code snippets
        st.subheader("Form Creation Code")
        st.code(form_code)
        
        st.subheader("Form Validation and Submission Code")
        st.code(validation_code)
    
    with tab3:
        st.subheader("HR Form Best Practices")
        
        with st.expander("Form Design Principles", expanded=True):
            st.markdown("""
            **HR Form Design Best Practices:**
            
            1. **Organize Logically**
               - Group related fields together
               - Use clear section headers
               - Present fields in a natural progression
               - Place most important fields first
            
            2. **Provide Clear Instructions**
               - Mark required fields (e.g., with asterisks)
               - Add help text for complex fields
               - Use placeholder text for format examples
               - Include overall form instructions if needed
            
            3. **Optimize Layout**
               - Use columns to save vertical space
               - Balance form density vs. readability
               - Ensure sufficient spacing between fields
               - Make forms mobile-friendly with responsive layout
            
            4. **Design for Accessibility**
               - Use descriptive labels for all fields
               - Ensure sufficient color contrast
               - Make error messages clear and actionable
               - Test with screen readers if possible
            
            5. **Streamline Completion**
               - Minimize the number of required fields
               - Use appropriate input types (select, radio, etc.)
               - Pre-fill fields when possible
               - Save progress for long forms
            """)
            
        with st.expander("Form Validation Strategies"):
            st.markdown("""
            **Effective Form Validation in Streamlit:**
            
            1. **Client-side Validation**
               - Check required fields are completed
               - Validate email formats, phone numbers, etc.
               - Verify numeric ranges are appropriate
               - Ensure date fields have valid dates
            
            2. **Validation Timing**
               - Validate on form submission (most common)
               - Consider real-time validation for complex fields
               - Use `st.session_state` for cross-field validation
            
            3. **Error Messaging**
               - Use `st.error()` for validation failures
               - Provide specific, actionable error messages
               - Position error messages near the problematic fields
               - Use friendly, non-technical language
            
            4. **Advanced Validation**
               - Check for duplicate entries
               - Validate against existing data
               - Implement business rule validations
               - Consider data type conversions
            
            5. **Success Feedback**
               - Confirm successful submission with `st.success()`
               - Show summary of submitted data
               - Provide next steps after submission
               - Consider clearing form after submission
            """)
    
    # Add a divider between sections
    st.divider()
    
    # Section 2: Employee Surveys and Feedback Forms
    st.header("2. Employee Surveys and Feedback Forms")
    
    # Use tabs for the learning components
    tab1, tab2, tab3 = st.tabs(["🔍 Live Example", "💻 Code", "📚 Explanation"])
    
    with tab1:
        st.subheader("Employee Engagement Survey")
        
        # Create an employee engagement survey
        with st.form("engagement_survey"):
            st.markdown("### Making Magic Company - Employee Engagement Survey")
            st.markdown("""
            Please provide your honest feedback to help us improve our workplace. 
            Your responses will be kept confidential and used only in aggregate form.
            """)
            
            # Basic information (anonymous but with some categorization)
            st.markdown("### About You")
            
            col1, col2 = st.columns(2)
            
            with col1:
                department = st.selectbox(
                    "Department",
                    options=[
                        "Select Department...",
                        "Engineering", 
                        "Product", 
                        "Marketing", 
                        "Sales", 
                        "Customer Support", 
                        "Finance", 
                        "HR", 
                        "Operations", 
                        "Research", 
                        "Legal",
                        "Prefer not to say"
                    ],
                    key="survey_department"
                )
            
            with col2:
                tenure = st.selectbox(
                    "Tenure at Making Magic",
                    options=[
                        "Select Tenure...",
                        "Less than 1 year",
                        "1-2 years",
                        "3-5 years",
                        "6-10 years",
                        "More than 10 years",
                        "Prefer not to say"
                    ]
                )
            
            # Engagement questions with Likert scale
            st.markdown("### Engagement Questions")
            st.markdown("Please rate your agreement with the following statements:")
            
            # Define the questions
            engagement_questions = [
                "I am proud to work at Making Magic Company",
                "I would recommend Making Magic as a great place to work",
                "My work gives me a sense of purpose and meaning",
                "I have the resources I need to do my job well",
                "I receive recognition when I do good work",
                "I see opportunities for career growth at Making Magic",
                "My manager provides me with regular, constructive feedback",
                "I feel included and valued as a team member"
            ]
            
            # Create the Likert scale
            likert_scale = [
                "Strongly Disagree",
                "Disagree",
                "Neutral",
                "Agree",
                "Strongly Agree"
            ]
            
            # Store responses
            responses = {}
            
            # Create radio buttons for each question
            for i, question in enumerate(engagement_questions):
                responses[f"q{i+1}"] = st.radio(
                    question,
                    options=likert_scale,
                    horizontal=True,
                    key=f"engagement_q{i+1}"
                )
                st.markdown("---")
            
            # Work-life balance section
            st.markdown("### Work-Life Balance")
            
            workload = st.slider(
                "How manageable is your current workload?",
                min_value=1,
                max_value=10,
                value=5,
                help="1 = Too light, 5 = Just right, 10 = Too heavy"
            )
            
            work_hours = st.number_input(
                "On average, how many hours do you work per week?",
                min_value=0,
                max_value=80,
                value=40,
                step=1
            )
            
            # Open-ended questions
            st.markdown("### Open-Ended Feedback")
            
            strengths = st.text_area(
                "What do you like most about working at Making Magic?",
                height=100,
                key="strengths"
            )
            
            improvements = st.text_area(
                "What could Making Magic do better to improve your work experience?",
                height=100,
                key="improvements"
            )
            
            # Submit button
            submitted_survey = st.form_submit_button("Submit Survey")
        
        # Handle survey submission
        if submitted_survey:
            # Check if department and tenure are selected
            if department == "Select Department..." or tenure == "Select Tenure...":
                st.error("Please select your department and tenure.")
            else:
                # Show loading spinner (simulating submission)
                with st.spinner("Submitting your feedback..."):
                    time.sleep(1)  # Simulate processing time
                
                # Success message
                st.success("Thank you for your feedback! Your responses have been recorded.")
                
                # Show a summary of the quantitative responses
                st.markdown("### Response Summary")
                
                # Calculate engagement score (1-5 scale)
                engagement_score = 0
                for i in range(len(engagement_questions)):
                    question_score = likert_scale.index(responses[f"q{i+1}"]) + 1  # 1-5 scale
                    engagement_score += question_score
                
                avg_engagement = engagement_score / len(engagement_questions)
                
                # Create metrics display
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Overall Engagement Score",
                        f"{avg_engagement:.1f}/5.0"
                    )
                
                with col2:
                    st.metric(
                        "Workload Score",
                        f"{workload}/10",
                        help="1 = Too light, 5 = Just right, 10 = Too heavy"
                    )
                
                with col3:
                    st.metric(
                        "Work Hours",
                        f"{work_hours} hrs/week",
                        help="Self-reported average weekly hours"
                    )
                
                # Provide a visual representation of responses
                st.markdown("### Engagement Question Responses")
                
                # Convert responses to a dataframe for visualization
                response_data = []
                for i, question in enumerate(engagement_questions):
                    shortened_question = question[:30] + "..." if len(question) > 30 else question
                    response_value = likert_scale.index(responses[f"q{i+1}"]) + 1  # Convert to 1-5 scale
                    response_data.append({
                        "Question": shortened_question,
                        "Score": response_value
                    })
                
                response_df = pd.DataFrame(response_data)
                
                # Display as a horizontal bar chart
                st.bar_chart(response_df.set_index("Question"))
    
    with tab2:
        # Store code snippets in variables
        survey_form_code = """
# Create an employee engagement survey
with st.form("engagement_survey"):
    st.markdown("### Making Magic Company - Employee Engagement Survey")
    st.markdown(\"\"\"
    Please provide your honest feedback to help us improve our workplace. 
    Your responses will be kept confidential and used only in aggregate form.
    \"\"\")
    
    # Basic information (anonymous but with some categorization)
    st.markdown("### About You")
    
    col1, col2 = st.columns(2)
    
    with col1:
        department = st.selectbox(
            "Department",
            options=[
                "Select Department...",
                "Engineering", 
                "Product", 
                "Marketing", 
                # ... other departments ...
                "Prefer not to say"
            ],
            key="survey_department"
        )
    
    with col2:
        tenure = st.selectbox(
            "Tenure at Making Magic",
            options=[
                "Select Tenure...",
                "Less than 1 year",
                "1-2 years",
                "3-5 years",
                "6-10 years",
                "More than 10 years",
                "Prefer not to say"
            ]
        )
    
    # Engagement questions with Likert scale
    st.markdown("### Engagement Questions")
    st.markdown("Please rate your agreement with the following statements:")
    
    # Define the questions
    engagement_questions = [
        "I am proud to work at Making Magic Company",
        "I would recommend Making Magic as a great place to work",
        # ... other questions ...
    ]
    
    # Create the Likert scale
    likert_scale = [
        "Strongly Disagree",
        "Disagree",
        "Neutral",
        "Agree",
        "Strongly Agree"
    ]
    
    # Store responses
    responses = {}
    
    # Create radio buttons for each question
    for i, question in enumerate(engagement_questions):
        responses[f"q{i+1}"] = st.radio(
            question,
            options=likert_scale,
            horizontal=True,
            key=f"engagement_q{i+1}"
        )
        st.markdown("---")
"""
        
        survey_processing_code = """
# Handle survey submission
if submitted_survey:
    # Check if department and tenure are selected
    if department == "Select Department..." or tenure == "Select Tenure...":
        st.error("Please select your department and tenure.")
    else:
        # Show loading spinner (simulating submission)
        with st.spinner("Submitting your feedback..."):
            time.sleep(1)  # Simulate processing time
        
        # Success message
        st.success("Thank you for your feedback! Your responses have been recorded.")
        
        # Calculate engagement score (1-5 scale)
        engagement_score = 0
        for i in range(len(engagement_questions)):
            question_score = likert_scale.index(responses[f"q{i+1}"]) + 1  # 1-5 scale
            engagement_score += question_score
        
        avg_engagement = engagement_score / len(engagement_questions)
        
        # Create metrics display
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Overall Engagement Score",
                f"{avg_engagement:.1f}/5.0"
            )
        
        # Convert responses to a dataframe for visualization
        response_data = []
        for i, question in enumerate(engagement_questions):
            shortened_question = question[:30] + "..." if len(question) > 30 else question
            response_value = likert_scale.index(responses[f"q{i+1}"]) + 1  # Convert to 1-5 scale
            response_data.append({
                "Question": shortened_question,
                "Score": response_value
            })
        
        response_df = pd.DataFrame(response_data)
        
        # Display as a horizontal bar chart
        st.bar_chart(response_df.set_index("Question"))
"""
        
        # Display code snippets
        st.subheader("Survey Form Creation Code")
        st.code(survey_form_code)
        
        st.subheader("Survey Processing Code")
        st.code(survey_processing_code)
    
    with tab3:
        st.subheader("Survey Design Best Practices")
        
        with st.expander("HR Survey Design Principles", expanded=True):
            st.markdown("""
            **Effective HR Survey Design:**
            
            1. **Start with Clear Objectives**
               - Define what you want to learn
               - Focus questions on actionable insights
               - Align with organizational priorities
               - Consider how results will be used
            
            2. **Structure Your Survey Effectively**
               - Begin with simple, engaging questions
               - Group related questions together
               - Place sensitive questions later in the survey
               - End with open-ended questions for qualitative feedback
            
            3. **Write Clear Questions**
               - Use simple, direct language
               - Ask only one thing per question
               - Avoid leading or biased questions
               - Define any technical terms or jargon
            
            4. **Choose Appropriate Response Formats**
               - Likert scales for agreement statements
               - Numeric scales for ratings
               - Multiple choice for categorical data
               - Text areas for open-ended feedback
            
            5. **Ensure Anonymity and Confidentiality**
               - Clearly communicate privacy protections
               - Collect minimal demographic data
               - Use aggregate reporting
               - Consider allowing "prefer not to say" options
            """)
            
        with st.expander("Survey Data Analysis Techniques"):
            st.markdown("""
            **Analyzing HR Survey Data in Streamlit:**
            
            1. **Quantitative Analysis**
               - Calculate average scores for each question
               - Segment results by department, tenure, etc.
               - Track trends over time if historical data exists
               - Identify outliers and areas for improvement
            
            2. **Visualization Approaches**
               - Bar charts for comparing question scores
               - Heatmaps for identifying patterns across questions
               - Line charts for trend analysis
               - Radar charts for comparing multiple dimensions
            
            3. **Qualitative Analysis**
               - Categorize open-ended responses by theme
               - Identify recurring feedback patterns
               - Highlight representative quotes
               - Correlate themes with quantitative scores
            
            4. **Actionable Reporting**
               - Focus on insights, not just data
               - Highlight top strengths and opportunities
               - Compare against benchmarks when available
               - Make specific recommendations based on findings
            
            5. **Dashboard Creation**
               - Create interactive filters for exploring results
               - Design for different stakeholder needs
               - Include both high-level and detailed views
               - Enable drill-down capabilities for deeper exploration
            """)
    
    # Add a divider between sections
    st.divider()
    
    # Section 3: Advanced Form Techniques
    st.header("3. Advanced Form Techniques")
    
    # Use tabs for the learning components
    tab1, tab2, tab3 = st.tabs(["🔍 Live Example", "💻 Code", "📚 Explanation"])
    
    with tab1:
        st.subheader("Performance Review Form")
        
        # Set up a session state for multi-step form
        if "step" not in st.session_state:
            st.session_state.step = 1
        
        if "form_data" not in st.session_state:
            st.session_state.form_data = {}
        
        # Create a multi-step performance review form
        st.markdown("### Annual Performance Review")
        
        # Display progress indicator
        progress_value = (st.session_state.step - 1) / 3  # 3 steps total
        st.progress(progress_value)
        
        # Step 1: Employee and Review Information
        if st.session_state.step == 1:
            with st.form("review_step1"):
                st.markdown("#### Step 1: Review Information")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    employee_name = st.text_input(
                        "Employee Name*",
                        value=st.session_state.form_data.get("employee_name", "")
                    )
                    
                    employee_id = st.text_input(
                        "Employee ID*",
                        value=st.session_state.form_data.get("employee_id", "")
                    )
                
                with col2:
                    review_period = st.selectbox(
                        "Review Period*",
                        options=[
                            "2025 Annual Review",
                            "2024 Annual Review",
                            "2025 Mid-Year Review",
                            "2024 Mid-Year Review",
                            "90-Day Review"
                        ],
                        index=0 if "review_period" not in st.session_state.form_data else 
                             ["2025 Annual Review", "2024 Annual Review", "2025 Mid-Year Review", 
                              "2024 Mid-Year Review", "90-Day Review"].index(st.session_state.form_data["review_period"])
                    )
                    
                    reviewer = st.text_input(
                        "Reviewer Name*",
                        value=st.session_state.form_data.get("reviewer", "")
                    )
                
                review_date = st.date_input(
                    "Review Date*",
                    value=datetime.datetime.strptime(st.session_state.form_data.get("review_date", datetime.datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
                )
                
                # Submit button for step 1
                next_step = st.form_submit_button("Next: Performance Assessment")
                
                if next_step:
                    # Validate required fields
                    if not employee_name or not employee_id or not reviewer:
                        st.error("Please fill in all required fields.")
                    else:
                        # Save data to session state
                        st.session_state.form_data["employee_name"] = employee_name
                        st.session_state.form_data["employee_id"] = employee_id
                        st.session_state.form_data["review_period"] = review_period
                        st.session_state.form_data["reviewer"] = reviewer
                        st.session_state.form_data["review_date"] = review_date.strftime("%Y-%m-%d")
                        
                        # Move to next step
                        st.session_state.step = 2
                        st.experimental_rerun()
        
        # Step 2: Performance Assessment
        elif st.session_state.step == 2:
            with st.form("review_step2"):
                st.markdown("#### Step 2: Performance Assessment")
                
                # Define performance categories
                performance_categories = [
                    "Quality of Work",
                    "Productivity",
                    "Job Knowledge",
                    "Reliability",
                    "Communication",
                    "Teamwork",
                    "Problem Solving",
                    "Initiative"
                ]
                
                # Rating scale
                rating_scale = [
                    "1 - Below Expectations",
                    "2 - Partially Meets Expectations",
                    "3 - Meets Expectations",
                    "4 - Exceeds Expectations",
                    "5 - Far Exceeds Expectations"
                ]
                
                # Create ratings for each category
                st.markdown("Please rate the employee in the following categories:")
                
                ratings = {}
                for category in performance_categories:
                    ratings[category] = st.select_slider(
                        category,
                        options=rating_scale,
                        value=st.session_state.form_data.get(f"rating_{category}", "3 - Meets Expectations")
                    )
                    
                    # Add comments for each category
                    ratings[f"{category}_comments"] = st.text_area(
                        f"Comments on {category}",
                        value=st.session_state.form_data.get(f"rating_{category}_comments", ""),
                        height=100
                    )
                    
                    st.markdown("---")
                
                # Navigation buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    back_button = st.form_submit_button("Back")
                
                with col2:
                    next_button = st.form_submit_button("Next: Overall Assessment")
                
                if back_button:
                    st.session_state.step = 1
                    st.experimental_rerun()
                
                if next_button:
                    # Save ratings to session state
                    for category in performance_categories:
                        st.session_state.form_data[f"rating_{category}"] = ratings[category]
                        st.session_state.form_data[f"rating_{category}_comments"] = ratings[f"{category}_comments"]
                    
                    # Move to next step
                    st.session_state.step = 3
                    st.experimental_rerun()
        
        # Step 3: Overall Assessment and Goals
        elif st.session_state.step == 3:
            with st.form("review_step3"):
                st.markdown("#### Step 3: Overall Assessment and Development Goals")
                
                # Overall performance rating
                overall_rating = st.select_slider(
                    "Overall Performance Rating",
                    options=[
                        "1 - Below Expectations",
                        "2 - Partially Meets Expectations",
                        "3 - Meets Expectations",
                        "4 - Exceeds Expectations",
                        "5 - Far Exceeds Expectations"
                    ],
                    value=st.session_state.form_data.get("overall_rating", "3 - Meets Expectations")
                )
                
                # Summary assessment
                st.markdown("### Performance Summary")
                
                strengths = st.text_area(
                    "Key Strengths",
                    value=st.session_state.form_data.get("strengths", ""),
                    height=100
                )
                
                areas_for_improvement = st.text_area(
                    "Areas for Improvement",
                    value=st.session_state.form_data.get("areas_for_improvement", ""),
                    height=100
                )
                
                # Development goals
                st.markdown("### Development Goals")
                
                goals = st.text_area(
                    "Development Goals for Next Period",
                    value=st.session_state.form_data.get("goals", ""),
                    height=150,
                    help="List specific, measurable goals for the next review period"
                )
                
                # Employee comments section
                st.markdown("### Employee Comments")
                
                employee_comments = st.text_area(
                    "Employee Feedback on Review",
                    value=st.session_state.form_data.get("employee_comments", ""),
                    height=150,
                    help="To be completed by the employee after discussing the review"
                )
                
                # Navigation buttons
                col1, col2 = st.columns(2)
                
                with col1:
                    back_button = st.form_submit_button("Back")
                
                with col2:
                    submit_button = st.form_submit_button("Submit Review")
                
                if back_button:
                    st.session_state.step = 2
                    st.experimental_rerun()
                
                if submit_button:
                    # Save final data to session state
                    st.session_state.form_data["overall_rating"] = overall_rating
                    st.session_state.form_data["strengths"] = strengths
                    st.session_state.form_data["areas_for_improvement"] = areas_for_improvement
                    st.session_state.form_data["goals"] = goals
                    st.session_state.form_data["employee_comments"] = employee_comments
                    
                    # Process the complete form submission
                    # In a real app, this would save to a database or file
                    st.success("Performance review submitted successfully!")
                    
                    # Show a summary of the review
                    st.markdown("### Performance Review Summary")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"**Employee:** {st.session_state.form_data['employee_name']}")
                        st.markdown(f"**ID:** {st.session_state.form_data['employee_id']}")
                        st.markdown(f"**Review Period:** {st.session_state.form_data['review_period']}")
                    
                    with col2:
                        st.markdown(f"**Reviewer:** {st.session_state.form_data['reviewer']}")
                        st.markdown(f"**Date:** {st.session_state.form_data['review_date']}")
                        st.markdown(f"**Overall Rating:** {overall_rating}")
                    
                    # Show the performance ratings
                    st.markdown("#### Performance Ratings")
                    
                    # Extract just the performance ratings
                    performance_categories = [
                        "Quality of Work",
                        "Productivity",
                        "Job Knowledge",
                        "Reliability",
                        "Communication",
                        "Teamwork",
                        "Problem Solving",
                        "Initiative"
                    ]
                    
                    rating_data = []
                    for category in performance_categories:
                        rating = st.session_state.form_data[f"rating_{category}"]
                        # Extract numeric value (first character of the rating)
                        rating_value = int(rating[0])
                        rating_data.append({
                            "Category": category,
                            "Rating": rating_value
                        })
                    
                    rating_df = pd.DataFrame(rating_data)
                    
                    # Display as a bar chart
                    st.bar_chart(rating_df.set_index("Category"))
                    
                    # Add a button to start a new review
                    if st.button("Start New Review"):
                        # Reset form data and step
                        st.session_state.form_data = {}
                        st.session_state.step = 1
                        st.experimental_rerun()
    
    with tab2:
        # Store code snippets in variables
        multi_step_form_code = """
# Set up a session state for multi-step form
if "step" not in st.session_state:
    st.session_state.step = 1

if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# Create a multi-step performance review form
st.markdown("### Annual Performance Review")

# Display progress indicator
progress_value = (st.session_state.step - 1) / 3  # 3 steps total
st.progress(progress_value)

# Step 1: Employee and Review Information
if st.session_state.step == 1:
    with st.form("review_step1"):
        st.markdown("#### Step 1: Review Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            employee_name = st.text_input(
                "Employee Name*",
                value=st.session_state.form_data.get("employee_name", "")
            )
            
            # More fields...
        
        # Submit button for step 1
        next_step = st.form_submit_button("Next: Performance Assessment")
        
        if next_step:
            # Validate required fields
            if not employee_name or not employee_id or not reviewer:
                st.error("Please fill in all required fields.")
            else:
                # Save data to session state
                st.session_state.form_data["employee_name"] = employee_name
                # Save other fields...
                
                # Move to next step
                st.session_state.step = 2
                st.experimental_rerun()
"""
        
        form_state_management_code = """
# Step 2: Performance Assessment
elif st.session_state.step == 2:
    with st.form("review_step2"):
        st.markdown("#### Step 2: Performance Assessment")
        
        # Define performance categories
        performance_categories = [
            "Quality of Work",
            "Productivity",
            "Job Knowledge",
            # More categories...
        ]
        
        # Rating scale
        rating_scale = [
            "1 - Below Expectations",
            "2 - Partially Meets Expectations",
            "3 - Meets Expectations",
            "4 - Exceeds Expectations",
            "5 - Far Exceeds Expectations"
        ]
        
        # Create ratings for each category
        ratings = {}
        for category in performance_categories:
            ratings[category] = st.select_slider(
                category,
                options=rating_scale,
                value=st.session_state.form_data.get(f"rating_{category}", "3 - Meets Expectations")
            )
            
            # Add comments for each category
            ratings[f"{category}_comments"] = st.text_area(
                f"Comments on {category}",
                value=st.session_state.form_data.get(f"rating_{category}_comments", ""),
                height=100
            )
            
            st.markdown("---")
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        
        with col1:
            back_button = st.form_submit_button("Back")
        
        with col2:
            next_button = st.form_submit_button("Next: Overall Assessment")
        
        if back_button:
            st.session_state.step = 1
            st.experimental_rerun()
        
        if next_button:
            # Save ratings to session state
            for category in performance_categories:
                st.session_state.form_data[f"rating_{category}"] = ratings[category]
                st.session_state.form_data[f"rating_{category}_comments"] = ratings[f"{category}_comments"]
            
            # Move to next step
            st.session_state.step = 3
            st.experimental_rerun()
"""
        
        # Display code snippets
        st.subheader("Multi-Step Form Setup Code")
        st.code(multi_step_form_code)
        
        st.subheader("Form State Management Code")
        st.code(form_state_management_code)
    
    with tab3:
        st.subheader("Advanced Form Techniques")
        
        with st.expander("Multi-Step Forms", expanded=True):
            st.markdown("""
            **Implementing Multi-Step Forms in Streamlit:**
            
            1. **Why Use Multi-Step Forms**
               - Break long forms into manageable sections
               - Reduce cognitive load for users
               - Organize related fields together
               - Provide a sense of progress
            
            2. **Implementation Approach**
               - Use `st.session_state` to track current step
               - Store form data between steps
               - Validate each step before proceeding
               - Allow navigation between steps
            
            3. **Progress Indicators**
               - Use `st.progress()` to show completion percentage
               - Add step numbers and titles
               - Highlight the current step
               - Show estimated time to complete
            
            4. **Navigation Controls**
               - Provide clear next/back buttons
               - Allow saving progress for later
               - Consider adding a step overview
               - Enable jumping to specific steps (if appropriate)
            
            5. **Data Handling**
               - Preserve entered data when moving between steps
               - Validate data at each step and on final submission
               - Submit complete data only on the final step
               - Consider storing drafts automatically
            """)
            
        with st.expander("Form State Management Techniques"):
            st.markdown("""
            **Managing Form State in Streamlit:**
            
            1. **Using Session State**
               - Store form data in `st.session_state`
               - Initialize state variables at the beginning
               - Update state when form values change
               - Persist values between page reloads
            
            2. **Handling Default Values**
               - Set default values from session state or initial values
               - Example: `value=st.session_state.get("field_name", "default_value")`
               - Ensure consistent state across form resubmissions
            
            3. **Form Validation Strategies**
               - Validate data before updating session state
               - Store validation errors in session state
               - Display errors next to relevant fields
               - Clear errors when issues are resolved
            
            4. **Advanced State Patterns**
               - Use nested dictionaries for complex forms
               - Implement form versioning for revisions
               - Create form templates for repeated structures
               - Use callbacks for dynamic form behaviors
            
            5. **Persisting Data Beyond Session**
               - Save form data to file or database
               - Implement draft saving functionality
               - Create form retrieval mechanisms
               - Handle form history and versioning
            """)
    
    # Add a practical challenge
    st.divider()
    st.header("🧩 Practice Challenge")
    
    challenge_description = """
    **Challenge**: Create a Training Request Form
    
    Build a form for employees to request training or professional development opportunities:
    
    1. Capture essential information (employee details, training requested, costs, etc.)
    2. Include validation to ensure all required fields are completed
    3. Add a confirmation screen that summarizes the request details
    4. Implement at least one advanced feature (multi-step form, dynamic fields, etc.)
    
    Bonus: Make the form responsive to different types of training requests.
    """
    
    st.info(challenge_description)
    
    # Provide a hint
    with st.expander("See Hint"):
        hint_code = """
# Training Request Form

with st.form("training_request"):
    st.markdown("### Training Request Form")
    
    # Employee Information
    st.markdown("#### Employee Information")
    
    col1, col2 = st.columns(2)
    with col1:
        employee_name = st.text_input("Employee Name*")
        employee_id = st.text_input("Employee ID*")
    
    with col2:
        department = st.selectbox(
            "Department*",
            options=["Engineering", "Product", "Marketing", "Sales", "HR", "Finance", "Other"]
        )
        manager = st.text_input("Manager Name*")
    
    # Training Information
    st.markdown("#### Training Details")
    
    training_type = st.selectbox(
        "Type of Training*",
        options=["Conference", "Course", "Workshop", "Certification", "Online Learning", "Other"]
    )
    
    # Show different fields based on training type
    if training_type == "Conference":
        training_name = st.text_input("Conference Name*")
        location = st.text_input("Conference Location*")
        start_date = st.date_input("Start Date*")
        end_date = st.date_input("End Date*")
        
        # Conference-specific fields
        st.checkbox("Requires Travel")
        st.checkbox("Presenting at Conference")
    
    elif training_type == "Certification":
        training_name = st.text_input("Certification Name*")
        provider = st.text_input("Certification Provider*")
        exam_date = st.date_input("Expected Exam Date*")
        
        # Certification-specific fields
        st.number_input("Study Hours Required", min_value=0, value=40)
        st.checkbox("Requires Renewal")
    
    # Common fields for all training types
    estimated_cost = st.number_input("Estimated Cost ($)*", min_value=0)
    
    business_justification = st.text_area(
        "Business Justification*",
        height=100,
        placeholder="Explain how this training will benefit your role and the company"
    )
    
    # Submit button
    submitted = st.form_submit_button("Submit Request")

if submitted:
    # Validate required fields
    if not employee_name or not employee_id or not manager or not training_name:
        st.error("Please fill in all required fields.")
    else:
        st.success("Training request submitted successfully!")
        
        # Display confirmation
        st.markdown("### Request Summary")
        st.markdown(f"**Employee:** {employee_name} ({employee_id})")
        st.markdown(f"**Department:** {department}")
        st.markdown(f"**Training:** {training_type} - {training_name}")
        st.markdown(f"**Estimated Cost:** ${estimated_cost}")
"""
        st.code(hint_code)
    
    # Next steps
    st.divider()
    st.markdown("**Next Module**: [HR Data Connections](placeholder)")