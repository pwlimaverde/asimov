from typing import List

import pandas as pd
from py_return_success_or_error import (
    Datasource,
)

from asimov.projetos.streamlit_fifa.app.features.ler_csv_fifa.domain.models.fifa_player import (
    FifaPlayer, )
from asimov.projetos.streamlit_fifa.app.utils.parameters import LoadCsvParameters


class LoadCsvPandasDatasource(Datasource[List[FifaPlayer], LoadCsvParameters]):
    def __call__(self, parameters: LoadCsvParameters) -> List[FifaPlayer]:
        """Carrega um arquivo CSV com dados de jogadores do FIFA 23"""
        df = pd.read_csv(parameters.file_path)
        players = [FifaPlayer.from_csv_row(row)
                   for row in df.to_dict('records')]
        return players
