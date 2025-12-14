import streamlit as st
from analytics import phishing_trend,cyber_time_series


st.title('Cybersecurity Dashboard')
st.plotly_chart(phishing_trend())

st.subheader("Incident Trend Over Time")
st.plotly_chart(cyber_time_series(), use_container_width=True)
