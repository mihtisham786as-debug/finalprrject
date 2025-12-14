import streamlit as st
from analytics import dataset_usage,dataset_growth


st.title('DataScience Dashboard')
st.plotly_chart(dataset_usage())

st.subheader("Dataset Growth Over Time")
st.plotly_chart(dataset_growth(), use_container_width=True)
