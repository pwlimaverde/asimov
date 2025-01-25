import streamlit as st


def teams():
    st.title("Teams")


st.write(teams())

df_data = st.session_state.data
st.write(df_data)
