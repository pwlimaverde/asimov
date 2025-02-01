import time
from typing import Optional

import pandas as pd
import streamlit as st

st.set_page_config(layout='wide', page_title='Spotify Songs')


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(
        "src/asimov/estudos/primeiro_dashboard/01 Spotify.csv")
    time.sleep(5)
    return df


df = load_data()

st.session_state['df_spotify'] = df

df.set_index('Track', inplace=True)

artsts = df['Artist'].value_counts().index
artist = st.sidebar.selectbox('Artista', artsts)

df_filtered_artist = df[df['Artist'] == artist]

albuns = df_filtered_artist['Album'].value_counts().index

album: Optional[str] = st.sidebar.selectbox(label='Album', options=albuns)

df_filtered_album = df[df['Album'] == album]

col1, col2 = st.columns([0.7, 0.3])

col1.bar_chart(df_filtered_album['Stream'])
col2.line_chart(df_filtered_album['Danceability'])
