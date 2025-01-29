

import streamlit as st

from asimov.projetos.streamlit_fifa.app.features.features_presenter import (
    FeaturesPresenter,
)


def main():
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
    # Configuração inicial
    presenter = FeaturesPresenter()

    # Carrega dados apenas uma vez
    if 'data' not in st.session_state:
        df_list = presenter.ler_csv_fifa(
            'src/asimov/projetos/streamlit_fifa/app/datasets/CLEAN_FIFA23_official_data.csv')

        st.session_state.data = df_list

    # Roteamento de páginas
    paginas.run()


if __name__ == '__main__':
    main()
