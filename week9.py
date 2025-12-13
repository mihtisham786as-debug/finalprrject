import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import bcrypt

DB_FILE = "intelligence_platform.db"

#  Database Functions 
def get_connection():
    return sqlite3.connect(DB_FILE)

def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password_hash, role FROM users WHERE username=?", (username,))
    result = cur.fetchone()
    conn.close()
    if result:
        stored_hash, role = result
        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            return True, role
    return False, None

def get_cyber_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM cyber_incidents", conn)
    conn.close()
    return df

def insert_cyber(incident_type, severity, resolution_time):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cyber_incidents (incident_type, severity, resolution_time) VALUES (?, ?, ?)",
        (incident_type, severity, resolution_time)
    )
    conn.commit()
    conn.close()

def update_cyber(row_id, incident_type, severity, resolution_time):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE cyber_incidents SET incident_type=?, severity=?, resolution_time=? WHERE id=?",
        (incident_type, severity, resolution_time, row_id)
    )
    conn.commit()
    conn.close()

def delete_cyber(row_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cyber_incidents WHERE id=?", (row_id,))
    conn.commit()
    conn.close()

#  Streamlit Setup 
st.set_page_config(page_title="Cybersecurity Dashboard", layout="wide")
st.title("🛡️ Cybersecurity Dashboard")

# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None

#  Login Page 
if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        success, role = login_user(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.success(f"✅ Login successful! Welcome {username} ({role})")
        else:
            st.error("❌ Login failed. Check your credentials.")

# Dashboard Page 
else:
    st.sidebar.write(f"Logged in as: {st.session_state.username} ({st.session_state.role})")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.experimental_rerun()

    # Load cyber incidents
    df = get_cyber_data()
    st.subheader("Cyber Incidents Table")
    st.dataframe(df)

    # Add new incident
    st.markdown("### ➕ Add New Incident")
    with st.form("add_incident"):
        incident_type = st.text_input("Incident Type")
        severity = st.selectbox("Severity", ["Low", "Medium", "High"])
        resolution_time = st.number_input("Resolution Time (hours)", min_value=0, value=24)
        submitted = st.form_submit_button("Add")
        if submitted:
            insert_cyber(incident_type, severity, resolution_time)
            st.success("Incident added successfully!")
            st.experimental_rerun()

    # Update / Delete
    st.markdown("### ✏️ Update / Delete Incident")
    if not df.empty:
        selected_id = st.selectbox("Select Incident ID", df["id"])
        row = df[df["id"] == selected_id].iloc[0]
        new_incident_type = st.text_input("Incident Type", value=row["incident_type"])
        new_severity = st.selectbox("Severity", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(row["severity"]))
        new_resolution_time = st.number_input("Resolution Time (hours)", min_value=0, value=row["resolution_time"])
        if st.button("Update"):
            update_cyber(selected_id, new_incident_type, new_severity, new_resolution_time)
            st.success("Incident updated successfully!")
            st.experimental_rerun()
        if st.button("Delete"):
            delete_cyber(selected_id)
            st.success("Incident deleted successfully!")
            st.experimental_rerun()

    # Visualization
    st.markdown("### 📊 Incidents by Severity")
    if not df.empty:
        fig = px.bar(df.groupby("severity").size().reset_index(name="count"), x="severity", y="count", color="severity")
        st.plotly_chart(fig, use_container_width=True)
