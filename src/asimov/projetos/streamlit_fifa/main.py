from datetime import datetime

import pandas as pd
import streamlit as st

paginas = st.navigation(
    [
        st.Page(
            "app/ui/pages/home.py",
            title="Home",
            icon=":material/home:"),
        st.Page(
            "app/ui/pages/players.py",
            title="Players",
            icon=":material/folder_shared:"),
        st.Page(
            "app/ui/pages/teams.py",
            title="Teams",
            icon=":material/sports_and_outdoors:"),
    ])

if __name__ == '__main__':
    if 'data' not in st.session_state:
        df_data = pd.read_csv(
            'src/asimov/projetos/streamlit_fifa/app/datasets/CLEAN_FIFA23_official_data.csv',
            index_col=0)
        df_data = df_data[df_data['Contract Valid Until']
                          >= datetime.today().year]
        df_data = df_data[df_data['Value(£)'] > 0]
        df_data = df_data.sort_values(by='Overall', ascending=False)
        st.session_state.data = df_data
    paginas.run()
    st.sidebar.markdown(
        'Desenvolvideo por [pwlimaverde](https://github.com/pwlimaverde)')
