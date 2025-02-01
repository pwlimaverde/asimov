from dataclasses import dataclass

from py_return_success_or_error import ParametersReturnResult

from asimov.projetos.streamlit_fifa.app.utils.erros import LoadCsvFifaError


@dataclass
class LoadCsvParameters(ParametersReturnResult):
    """Parâmetros para carregar um arquivo CSV"""
    file_path: str
    error: LoadCsvFifaError

    def __str__(self) -> str:
        return self.__repr__()
