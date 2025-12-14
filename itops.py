import streamlit as st
from analytics import ticket_delay,it_ticket_trend


st.title('ITOps Dashboard')
st.plotly_chart(ticket_delay())

st.subheader("Ticket Volume Over Time")
st.plotly_chart(it_ticket_trend(), use_container_width=True)
