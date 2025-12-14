import streamlit as st


st.set_page_config(page_title='Multi-Domain Intelligence Platform')


if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:
    st.switch_page('pages/login.py')