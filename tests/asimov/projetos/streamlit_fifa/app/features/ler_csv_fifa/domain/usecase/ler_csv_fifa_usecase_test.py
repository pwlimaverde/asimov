
from unittest.mock import Mock

import pytest
from py_return_success_or_error import ErrorReturn, SuccessReturn

from asimov.projetos.streamlit_fifa.app.features.ler_csv_fifa.domain.models.fifa_player import (
    FifaPlayer, )
from asimov.projetos.streamlit_fifa.app.features.ler_csv_fifa.domain.usecase.ler_csv_fifa_usecase import (
    LerCsvFifaUseCase, )
from asimov.projetos.streamlit_fifa.app.utils.erros import LoadCsvFifaError
from asimov.projetos.streamlit_fifa.app.utils.parameters import LoadCsvParameters


@pytest.fixture
def mock_fifa_players():
    return [
        FifaPlayer(
            name="R. Santos",
            full_name="Roberto Carlos Santos",
            age=24,
            height_cm=178,
            weight_kg=75,
            nationality="Brazil",
            club="Flamengo",
            position="CAM",
            overall=83,
            value_eur=35000000.0,
            wage_eur=65000.0,
            release_clause_eur=45000000.0,
            potential=88,
            preferred_foot="Right",
            attacking_work_rate="High",
            defensive_work_rate="Medium",
            pace=85,
            shooting=82,
            passing=84,
            dribbling=86,
            defending=45,
            physicality=72
        ),
        FifaPlayer(
            name="V. Silva",
            full_name="Victor Hugo Silva",
            age=28,
            height_cm=188,
            weight_kg=82,
            nationality="Brazil",
            club="Manchester City",
            position="CB",
            overall=86,
            value_eur=48000000.0,
            wage_eur=120000.0,
            release_clause_eur=65000000.0,
            potential=88,
            preferred_foot="Left",
            attacking_work_rate="Medium",
            defensive_work_rate="High",
            pace=76,
            shooting=45,
            passing=72,
            dribbling=68,
            defending=88,
            physicality=90
        ),
        FifaPlayer(
            name="M. Costa",
            full_name="Marcus Vinicius Costa",
            age=21,
            height_cm=175,
            weight_kg=68,
            nationality="Brazil",
            club="Borussia Dortmund",
            position="RW",
            overall=81,
            value_eur=28000000.0,
            wage_eur=75000.0,
            release_clause_eur=38000000.0,
            potential=89,
            preferred_foot="Right",
            attacking_work_rate="High",
            defensive_work_rate="Low",
            pace=93,
            shooting=78,
            passing=76,
            dribbling=89,
            defending=32,
            physicality=65
        ),
    ]


def test_ler_csv_fifa_usecase_success(mock_fifa_players):
    # Arrange
    error = LoadCsvFifaError()
    parameters = LoadCsvParameters(
        file_path="test.csv",
        error=error
    )

    mock_result_datasource = Mock(return_value=mock_fifa_players)

    usecase = LerCsvFifaUseCase(
        datasource=mock_result_datasource,
    )
    # Act
    teste = usecase(parameters)
    play1 = teste.result[0].to_dict()

    # Assert
    assert isinstance(teste, SuccessReturn)
    assert len(teste.result) == 3
    assert teste.result[0].name == "R. Santos"
    assert teste.result[1].name == "V. Silva"
    assert teste.result[2].name == "M. Costa"
    assert play1['Name'] == "R. Santos"
    assert str(parameters) == "LoadCsvParameters(error=LoadCsvFifaError(message='Erro ao carregar o arquivo CSV'), file_path='test.csv')"


def test_ler_csv_fifa_usecase_error():
    # Arrange
    error = LoadCsvFifaError()
    parameters = LoadCsvParameters(
        file_path="test.csv",
        error=error
    )

    mock_result_datasource = Mock(side_effect=FileNotFoundError)

    usecase = LerCsvFifaUseCase(
        datasource=mock_result_datasource,
    )

    # Act
    teste = usecase(parameters)

    assert isinstance(teste, ErrorReturn)
    assert teste.result == error
    assert teste.result.message == "Erro ao carregar o arquivo CSV"
    assert str(
        teste.result) == "LoadCsvFifaError - Erro ao carregar o arquivo CSV"
