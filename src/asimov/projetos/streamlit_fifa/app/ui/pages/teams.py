import streamlit as st


def teams():
    st.title("Teams")

    df_data = st.session_state.data
    st.dataframe(df_data)


teams()
