import pandas as pd
import streamlit as st


def players():
    st.title("Players")

    df_data = pd.DataFrame(st.session_state.data)

    # filtered_data = [
    #         clube for clube in df_data
    #         if clube['club'] >= 2023
    #     ]

    clubes = df_data['club'].unique()
    club = st.sidebar.selectbox('Selecione um clube', clubes)
    df_players_club = df_data[(df_data['club'] == club)]

    players = df_players_club['name'].unique()
    player = st.sidebar.selectbox('Selecione um jogador', players)

    player_stats = df_data[df_data['name'] == player]

    st.write(player_stats)


players()
