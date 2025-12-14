import streamlit as st
from auth import login_user, register_user


st.title('Login / Register')


username = st.text_input('Username')
password = st.text_input('Password', type='password')
role = st.selectbox('Role', ['Cybersecurity','DataScience','ITOps'])


if st.button('Register'):
    if register_user(username, password, role):
        st.success('Registered successfully')


if st.button('Login'):
    r = login_user(username, password)
    if r:
        st.session_state.logged_in = True
        st.session_state.role = r
        st.success('Logged in')
        st.rerun()
    else:
        st.error("Invalid credentials")
