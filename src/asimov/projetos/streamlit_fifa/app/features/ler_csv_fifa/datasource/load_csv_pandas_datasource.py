from typing import List

import pandas as pd

from asimov.projetos.streamlit_fifa.app.features.ler_csv_fifa.domain.models.fifa_player import (
    FifaPlayer, )
from asimov.projetos.streamlit_fifa.app.utils.parameters import LoadCsvParameters
from asimov.projetos.streamlit_fifa.app.utils.types import LCFData


class LoadCsvPandasDatasource(LCFData):
    def __call__(self, parameters: LoadCsvParameters) -> List[FifaPlayer]:
        """Carrega um arquivo CSV com dados de jogadores do FIFA 23"""
        df = pd.read_csv(parameters.file_path, index_col=0)
        players = [
            FifaPlayer.from_csv_row(row)
            for row in df.to_dict('records')
        ]

        return players
