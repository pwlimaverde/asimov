import pandas as pd
import pytest

from asimov.projetos.streamlit_fifa.app.features.features_presenter import (
    FeaturesPresenter,
)
from asimov.projetos.streamlit_fifa.app.utils.erros import LoadCsvFifaError


@pytest.fixture
def mock_fifa_data():
    return {
        "ID": [209658, 212198, 192985],
        "Name": ["L. Goretzka", "Bruno Fernandes", "K. De Bruyne"],
        "Age": [27, 27, 31],
        "Photo": ["https://cdn.sofifa.net/players/209/658/23_60.png"] * 3,
        "Nationality": ["Germany", "Portugal", "Belgium"],
        "Flag": ["https://cdn.sofifa.net/flags/de.png"] * 3,
        "Overall": [87, 86, 91],
        "Potential": [88, 87, 91],
        "Club": ["FC Bayern München", "Manchester United", "Manchester City"],
        "Club Logo": ["https://cdn.sofifa.net/teams/21/30.png"] * 3,
        "Value(£)": [91000000.0, 78500000.0, 107500000.0],
        "Wage(£)": [115000.0, 190000.0, 350000.0],
        "Special": [2312, 2305, 2303],
        "Preferred Foot": ["Right"] * 3,
        "International Reputation": [4.0, 3.0, 4.0],
        "Weak Foot": [4.0, 3.0, 5.0],
        "Skill Moves": [3.0, 4.0, 4.0],
        "Work Rate": ["High/ Medium", "High/ High", "High/ High"],
        "Body Type": ["Unique"] * 3,
        "Real Face": ["Yes"] * 3,
        "Position": ["SUB", "LCM", "RCM"],
        "Joined": ["2018-07-01", "2020-01-30", "2015-08-30"],
        "Loaned From": ["None"] * 3,
        "Contract Valid Until": [2026.0, 2026.0, 2025.0],
        "Height(cm.)": [189.0, 179.0, 181.0],
        "Weight(lbs.)": [180.81, 152.145, 154.35],
        "Release Clause(£)": [157000000.0, 155000000.0, 198900000.0],
        "Kit Number": [8.0, 8.0, 17.0],
        "Best Overall Rating": [0.0] * 3,
        "Year_Joined": [2018, 2020, 2015]
    }


@pytest.fixture
def mock_csv_path(tmp_path, mock_fifa_data):
    # Criar DataFrame
    df = pd.DataFrame(mock_fifa_data)

    # Criar arquivo CSV no diretório temporário
    csv_file = tmp_path / "test.csv"
    df.to_csv(csv_file, index=False)

    # Retornar o path como string
    return str(csv_file)


def test_features_presenter_with_mock_data(mock_csv_path):
    # Arrange
    presenter = FeaturesPresenter()

    teste = presenter.ler_csv_fifa(mock_csv_path)

    assert len(teste) == 3
    assert teste[0].name == 'L. Goretzka'
    assert teste[1].name == 'Bruno Fernandes'
    assert teste[2].name == 'K. De Bruyne'


def test_features_presenter_file_not_found():
    # Arrange
    presenter = FeaturesPresenter()
    invalid_path = "invalid/path/file.csv"

    # Act/Assert
    with pytest.raises(FileNotFoundError) as exc_info:
        presenter.ler_csv_fifa(invalid_path)
    assert str(exc_info.value) == f"Arquivo não encontrado: {invalid_path}"


def test_features_presenter_invalid_csv_data(tmp_path):
    # Arrange
    presenter = FeaturesPresenter()
    invalid_csv = tmp_path / "invalid.csv"

    # Create invalid CSV file with missing required columns
    invalid_data = {
        'Column1': [1, 2, 3],
        'Column2': ['A', 'B', 'C']
    }
    df = pd.DataFrame(invalid_data)
    df.to_csv(invalid_csv, index=False)

    # Act/Assert
    try:
        presenter.ler_csv_fifa(str(invalid_csv))
        assert False, "Esperava-se um erro LoadCsvFifaError"
    except LoadCsvFifaError as exc:
        assert str(exc) == 'LoadCsvFifaError - Erro ao carregar o arquivo CSV'
