from typing import List

from py_return_success_or_error import (
    ReturnSuccessOrError,
)

from asimov.projetos.streamlit_fifa.app.features.ler_csv_fifa.domain.models.fifa_player import (
    FifaPlayer, )
from asimov.projetos.streamlit_fifa.app.utils.parameters import LoadCsvParameters
from asimov.projetos.streamlit_fifa.app.utils.types import LCFUsecase


class LerCsvFifaUseCase(LCFUsecase):
    def __call__(
            self, parameters: LoadCsvParameters) -> ReturnSuccessOrError[List[FifaPlayer]]:
        """Carrega um arquivo CSV com dados de jogadores do FIFA 23"""
        result = self._resultDatasource(
            parameters=parameters, datasource=self._datasource)
        print()
        print('LerCsvFifaUseCase**********')
        print(result)
        return result
