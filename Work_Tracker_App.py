#Work_Tracker_App.py
import streamlit as st
import pandas as pd
import altair as alt

# --- SIMULATED DATABASE SETUP ---
# This DataFrame will act as our in-memory "database"
# It is reset every time the app is re-run.
if 'tasks_df' not in st.session_state:
    st.session_state.tasks_df = pd.DataFrame(
        columns=[
            'WORKSTREAM', 'SPRINT_DATE', 'DESCRIPTION_OF_TASK', 
            'HOURS_ESTIMATED', 'USERID', 'STATUS', 'SUMMARY'
        ]
    )

def add_task(workstream, sprint_date, description, hours_estimated, user_id, status, summary):
    """Adds a new task to the simulated database (DataFrame)."""
    new_task = {
        'WORKSTREAM': workstream,
        'SPRINT_DATE': sprint_date,
        'DESCRIPTION_OF_TASK': description,
        'HOURS_ESTIMATED': hours_estimated,
        'USERID': user_id,
        'STATUS': status,
        'SUMMARY': summary
    }
    st.session_state.tasks_df = pd.concat(
        [st.session_state.tasks_df, pd.DataFrame([new_task])],
        ignore_index=True
    )

# --- STREAMLIT APP LOGIC ---

def create_task_form():
    """Creates the data entry form and handles submission."""
    st.header("Enter Your Work Task")
    with st.form("task_form"):
        workstream = st.text_input("Workstream")
        sprint_date = st.date_input("Sprint Date")
        description = st.text_area("Description of Task")
        hours_estimated = st.number_input("Hours Estimated", min_value=0)
        user_id = st.text_input("UserID")
        status = st.selectbox(
            "Status",
            ("Not Started", "In Progress", "On Hold", "Blocked", "Done")
        )
        submitted = st.form_submit_button("Submit Task")

    if submitted:
        if not all([workstream, description, user_id]):
            st.warning("Please fill out all required fields.")
        else:
            # Simulate the Cortex summary
            simulated_summary = f"Simulated Summary: The task is related to '{workstream}' and was estimated to take {hours_estimated} hours. It involves a key description related to '{description[:20]}...'."
            
            # Add the task to our in-memory DataFrame
            add_task(workstream, sprint_date, description, hours_estimated, user_id, status, simulated_summary)
            
            st.success("Task submitted and summarized successfully!")

def display_dashboard():
    """Displays the interactive dashboard with tables and charts."""
    df = st.session_state.tasks_df
    
    if df.empty:
        st.info("No work tasks have been submitted yet.")
        return

    st.header("Team Work for the Week")
    st.dataframe(df)
    
    # User-level time visualization
    st.header("Individual Time by Workstream")
    user_filter = st.selectbox("Select User to View", ['All'] + sorted(df['USERID'].unique()))
    
    filtered_df = df if user_filter == 'All' else df[df['USERID'] == user_filter]

    if not filtered_df.empty:
        workstream_hours = filtered_df.groupby('WORKSTREAM')['HOURS_ESTIMATED'].sum().reset_index()
        
        # Create an Altair bar chart for individual hours by workstream
        chart = alt.Chart(workstream_hours).mark_bar().encode(
            x=alt.X('WORKSTREAM', sort='-y', title='Workstream'),
            y=alt.Y('HOURS_ESTIMATED', title='Hours'),
            tooltip=['WORKSTREAM', 'HOURS_ESTIMATED']
        ).properties(
            title=f"Time Spent by Workstream for {user_filter}"
        )
        st.altair_chart(chart, use_container_width=True)
    
    # Team-level status visualization
    st.header("Team Status Overview")
    team_status_counts = df.groupby('STATUS')['STATUS'].count().reset_index(name='Count')

    # Create an Altair bar chart for team status
    status_chart = alt.Chart(team_status_counts).mark_bar().encode(
        x=alt.X('STATUS', sort=['Not Started', 'In Progress', 'On Hold', 'Blocked', 'Done']),
        y=alt.Y('Count', title='Number of Tasks'),
        tooltip=['STATUS', 'Count']
    ).properties(
        title="Current Team Task Status"
    )
    st.altair_chart(status_chart, use_container_width=True)

def main():
    """Main function to run the Streamlit app."""
    st.title("Reporting Team Work Tracker")
    create_task_form()
    st.divider()
    display_dashboard()

if __name__ == "__main__":
    main()