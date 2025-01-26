from pathlib import Path
from typing import List

from py_return_success_or_error import (
    ErrorReturn,
    SuccessReturn,
)

from asimov.projetos.streamlit_fifa.app.features.ler_csv_fifa.datasource.load_csv_pandas_datasource import (
    LoadCsvPandasDatasource, )
from asimov.projetos.streamlit_fifa.app.features.ler_csv_fifa.domain.models.fifa_player import (
    FifaPlayer, )
from asimov.projetos.streamlit_fifa.app.features.ler_csv_fifa.domain.usecase.ler_csv_fifa_usecase import (
    LerCsvFifaUseCase, )
from asimov.projetos.streamlit_fifa.app.utils.erros import LoadCsvFifaError
from asimov.projetos.streamlit_fifa.app.utils.parameters import LoadCsvParameters


class FeaturesPresenter:

    def ler_csv_fifa(self, file_path: str) -> List[FifaPlayer]:

        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        error = LoadCsvFifaError()
        parameters = LoadCsvParameters(error=error, file_path=str(path))
        dataSource = LoadCsvPandasDatasource()
        usecase = LerCsvFifaUseCase(dataSource)

        data = usecase(parameters)
        list_fifa_players: List[FifaPlayer] = []

        if isinstance(data, SuccessReturn):
            list_fifa_players = data.result

        if isinstance(data, ErrorReturn):
            raise data.result

        return list_fifa_players
