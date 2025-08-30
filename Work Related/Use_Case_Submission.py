import streamlit as st
import snowflake.connector
import pandas as pd
import uuid
from datetime import datetime

# ---------------------------
# Snowflake Connection
# ---------------------------
## Automatic connection - no credentials needed!
from snowflake.snowpark.context import get_active_session

session = get_active_session()

# Query data directly
df = session.sql('''
    SELECT * FROM HR_DATA.METRICS.HEADCOUNT
    WHERE DATE >= '2024-01-01'
''').to_pandas()
            

def insert_submission(data):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            INSERT INTO {SNOWFLAKE_TABLE} (
                submission_id, timestamp, submitter_name, submitter_email,
                use_case_title, description, business_value, priority,
                impacted_team, dependencies, timeline, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['submission_id'],
            data['timestamp'],
            data['submitter_name'],
            data['submitter_email'],
            data['use_case_title'],
            data['description'],
            data['business_value'],
            data['priority'],
            data['impacted_team'],
            data['dependencies'],
            data['timeline'],
            data['status'],
        ))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Use Case Submission Tool", layout="centered")
st.title("📌 Use Case Submission Tool")
st.write("Submit your innovative ideas and opportunities for leadership review. Each entry helps us track, prioritize, and deliver value.")

with st.form("use_case_form", clear_on_submit=True):
    st.subheader("Submit a New Use Case")

    submitter_name = st.text_input("Your Name *")
    submitter_email = st.text_input("Your Email *")
    use_case_title = st.text_input("Use Case Title *")
    description = st.text_area("Description *", help="Briefly describe the problem, opportunity, or idea.")
    business_value = st.text_area("Business Value", help="Explain the expected benefit, efficiency gain, or impact.")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    impacted_team = st.text_input("Impacted Team(s)")
    dependencies = st.text_input("Dependencies", help="Any systems, approvals, or resources required.")
    timeline = st.text_input("Expected Timeline", help="E.g., Q3 2025, 6 weeks, etc.")

    submitted = st.form_submit_button("Submit Use Case")

    if submitted:
        if not submitter_name or not submitter_email or not use_case_title or not description:
            st.error("Please complete all required fields (*).")
        else:
            data = {
                "submission_id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow(),
                "submitter_name": submitter_name,
                "submitter_email": submitter_email,
                "use_case_title": use_case_title,
                "description": description,
                "business_value": business_value,
                "priority": priority,
                "impacted_team": impacted_team,
                "dependencies": dependencies,
                "timeline": timeline,
                "status": "New"
            }
            try:
                insert_submission(data)
                st.success("✅ Your use case has been submitted successfully!")
            except Exception as e:
                st.error(f"❌ Error submitting use case: {e}")

st.markdown("---")
st.caption("After submission, entries will be stored in Snowflake and reflected in the leadership Smartsheet dashboard.")
