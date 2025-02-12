
from datetime import datetime
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
            id=1,
            name="L. Goretzka",
            age=27,
            photo="https://cdn.sofifa.net/players/209/658/23_60.png",
            nationality="Germany",
            flag="https://cdn.sofifa.net/flags/de.png",
            overall=75,
            potential=88,
            club="FC Bayern München",
            club_logo="https://cdn.sofifa.net/teams/21/30.png",
            value=91000000.0,
            wage=115000.0,
            special=2312,
            preferred_foot="Right",
            international_reputation=4.0,
            weak_foot=4.0,
            skill_moves=3.0,
            work_rate="High/ Medium",
            body_type="Unique",
            real_face="Yes",
            position="SUB",
            joined=datetime.strptime("2018-07-01", "%Y-%m-%d").date(),
            loaned_from="None",
            contract_valid_until=2026.0,
            height_m=1.890,
            weight_kg=(180.81 * 0.453),
            release_clause=157000000.0,
            kit_number=8.0,
            best_overall_rating=0.0,
            year_joined=2018
        ),
        FifaPlayer(
            id=2,
            name="Bruno Fernandes",
            age=27,
            photo="https://cdn.sofifa.net/players/212/198/23_60.png",
            nationality="Portugal",
            flag="https://cdn.sofifa.net/flags/pt.png",
            overall=86,
            potential=87,
            club="Manchester United",
            club_logo="https://cdn.sofifa.net/teams/11/30.png",
            value=78500000.0,
            wage=190000.0,
            special=2305,
            preferred_foot="Right",
            international_reputation=3.0,
            weak_foot=3.0,
            skill_moves=4.0,
            work_rate="High/ High",
            body_type="Unique",
            real_face="Yes",
            position="LCM",
            joined=datetime.strptime("2020-01-30", "%Y-%m-%d").date(),
            loaned_from="None",
            contract_valid_until=2026.0,
            height_m=.1790,
            weight_kg=(152.145 * 0.453),
            release_clause=155000000.0,
            kit_number=8.0,
            best_overall_rating=0.0,
            year_joined=2020
        ),
        FifaPlayer(
            id=3,
            name="K. De Bruyne",
            age=31,
            photo="https://cdn.sofifa.net/players/192/985/23_60.png",
            nationality="Belgium",
            flag="https://cdn.sofifa.net/flags/be.png",
            overall=91,
            potential=91,
            club="Manchester City",
            club_logo="https://cdn.sofifa.net/teams/10/30.png",
            value=107500000.0,
            wage=350000.0,
            special=2303,
            preferred_foot="Right",
            international_reputation=4.0,
            weak_foot=5.0,
            skill_moves=4.0,
            work_rate="High/ High",
            body_type="Unique",
            real_face="Yes",
            position="RCM",
            joined=datetime.strptime("2015-08-30", "%Y-%m-%d").date(),
            loaned_from="None",
            contract_valid_until=2025.0,
            height_m=1.810,
            weight_kg=(154.35 * 0.453),
            release_clause=198900000.0,
            kit_number=17.0,
            best_overall_rating=0.0,
            year_joined=2015
        )
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
    # Assert
    assert isinstance(teste, SuccessReturn)
    assert len(teste.result) == 3
    assert teste.result[0]['name'] == "K. De Bruyne"
    assert teste.result[1]['name'] == "Bruno Fernandes"
    assert teste.result[2]['name'] == "L. Goretzka"
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


def test_ler_csv_fifa_usecase_custom_data_exception():
    # Arrange
    error = LoadCsvFifaError()
    parameters = LoadCsvParameters(
        file_path="test.csv",
        error=error
    )

    mock_result_datasource = Mock(
        side_effect=Exception())

    usecase = LerCsvFifaUseCase(
        datasource=mock_result_datasource,
    )

    # Act
    result = usecase(parameters)

    # Assert
    assert isinstance(result, ErrorReturn)
    assert isinstance(result.result, LoadCsvFifaError)
    assert result.result.message == "Erro ao carregar o arquivo CSV"
    assert str(
        result.result) == "LoadCsvFifaError - Erro ao carregar o arquivo CSV"


def test_ler_csv_fifa_usecase_excecao(monkeypatch):
    error = LoadCsvFifaError()
    mock_result_datasource = Mock(
        side_effect=Exception())
    usecase = LerCsvFifaUseCase(datasource=mock_result_datasource)
    parameters = LoadCsvParameters(
        file_path="test.csv",
        error=error
    )

    def mock_result(*args, **kwargs):
        raise Exception("Erro simulado")

    monkeypatch.setattr(usecase, '_resultDatasource', mock_result)

    result = usecase(parameters)
    assert isinstance(result, ErrorReturn)
    assert isinstance(result.result, LoadCsvFifaError)
    assert "Erro simulado" in str(result.result.message)
