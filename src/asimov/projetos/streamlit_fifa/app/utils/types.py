from typing import List, TypeAlias

from py_return_success_or_error import (
    Datasource,
    UsecaseBaseCallData,
)

from asimov.projetos.streamlit_fifa.app.features.ler_csv_fifa.domain.models.fifa_player import (
    FifaPlayer, )
from asimov.projetos.streamlit_fifa.app.utils.parameters import LoadCsvParameters

LCFUsecase: TypeAlias = UsecaseBaseCallData[
    List[dict],
    List[FifaPlayer],
    LoadCsvParameters
]

LCFData: TypeAlias = Datasource[List[FifaPlayer], LoadCsvParameters]
