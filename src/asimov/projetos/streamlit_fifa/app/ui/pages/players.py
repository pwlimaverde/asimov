import streamlit as st

def players():
    st.title("Players")
    
st.write(players())

df_data = st.session_state.data
st.write(df_data)
