

from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

from asimov.projetos.streamlit_fifa.app.features.ler_csv_fifa.datasource.load_csv_pandas_datasource import (
    LoadCsvPandasDatasource, )
from asimov.projetos.streamlit_fifa.app.utils.erros import LoadCsvFifaError
from asimov.projetos.streamlit_fifa.app.utils.parameters import LoadCsvParameters


@pytest.fixture
def mock_fifa_csv():
    """Cria arquivo CSV temporário com dados de teste"""
    data = {
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

    df = pd.DataFrame(data)
    temp_csv = Path("mock_test.csv")
    df.to_csv(temp_csv, index=False)
    yield temp_csv
    temp_csv.unlink()  # Remove arquivo após teste


def test_load_csv_pandas_datasource_with_mock_data(mock_fifa_csv):
    # Arrange
    error = LoadCsvFifaError()
    parameters = LoadCsvParameters(file_path=mock_fifa_csv, error=error)

    # Act
    datasource = LoadCsvPandasDatasource()
    result = datasource(parameters)

    # Assert
    assert len(result) == 3
    assert result[0].name == 'L. Goretzka'
    assert result[0].age == 27
    assert result[0].overall == 87
    assert result[1].name == 'Bruno Fernandes'
    assert result[2].name == 'K. De Bruyne'


def test_load_csv_pandas_datasource_with_empty_data():
    # Arrange
    mock_df = pd.DataFrame()
    error = LoadCsvFifaError()
    parameters = LoadCsvParameters(file_path='dummy_path', error=error)

    # Act
    with patch('pandas.read_csv', return_value=mock_df):
        datasource = LoadCsvPandasDatasource()
        result = datasource(parameters)

    # Assert
    assert len(result) == 0


def test_load_csv_pandas_datasource_file_not_found():
    # Arrange
    error = LoadCsvFifaError()
    parameters = LoadCsvParameters(
        file_path='non_existent_file.csv', error=error)

    # Act & Assert
    with pytest.raises(FileNotFoundError):
        datasource = LoadCsvPandasDatasource()
        datasource(parameters)
