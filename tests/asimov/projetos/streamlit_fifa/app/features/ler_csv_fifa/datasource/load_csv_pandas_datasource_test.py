from unittest.mock import patch

import pandas as pd
import pytest

from asimov.projetos.streamlit_fifa.app.features.ler_csv_fifa.datasource.load_csv_pandas_datasource import (
    LoadCsvPandasDatasource, )
from asimov.projetos.streamlit_fifa.app.utils.erros import LoadCsvFifaError
from asimov.projetos.streamlit_fifa.app.utils.parameters import LoadCsvParameters


@pytest.fixture
def mock_fifa_data():
    return {
        'ID': [209658, 212198, 224334],
        'Name': ['L. Goretzka', 'Bruno Fernandes', 'M. Acuña'],
        'Age': [27, 27, 30],
        'Photo': ['photo1.png', 'photo2.png', 'photo3.png'],
        'Nationality': ['Germany', 'Portugal', 'Argentina'],
        'Flag': ['flag1.png', 'flag2.png', 'flag3.png'],
        'Overall': [87, 86, 85],
        'Potential': [88, 87, 85],
        'Club': ['FC Bayern München', 'Manchester United', 'Sevilla FC'],
        'Club Logo': ['logo1.png', 'logo2.png', 'logo3.png'],
        'Value(£)': [91000000.0, 78500000.0, 46500000.0],
        'Wage(£)': [115000.0, 190000.0, 46000.0],
        'Position': ['SUB', 'LCM', 'LB']
    }


def test_load_csv_pandas_datasource_with_mock_data(mock_fifa_data):
    # Arrange
    mock_df = pd.DataFrame(mock_fifa_data)
    error = LoadCsvFifaError()
    parameters = LoadCsvParameters(file_path='dummy_path', error=error)

    # Act
    with patch('pandas.read_csv', return_value=mock_df):
        datasource = LoadCsvPandasDatasource()
        result = datasource(parameters)

    # Assert
    assert len(result) == 3
    assert result[0].name == 'L. Goretzka'
    assert result[0].age == 27
    assert result[0].overall == 87
    assert result[1].name == 'Bruno Fernandes'
    assert result[2].name == 'M. Acuña'


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
