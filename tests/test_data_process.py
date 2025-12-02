import pandas as pd
import pytest
import numpy as np

from app.data.data_manager import DataManager

manager = DataManager()


@pytest.fixture
def sample_srag_data():
    return pd.DataFrame(
        {
            "EVOLUCAO": [1.0, 2.0, None, 1.0],
            "DT_SIN_PRI": ["2025-05-01", "2024-12-15", "2025-06-01", "2025-13-30"],
            "SEM_PRI": [20.0, 21.0, 22.0, 23.0],
            "UTI": [1.0, None, 2.0, 1.0],
            "HOSPITAL": [1.0, 1.0, 9.0, 9.0],
            "VACINA": [1.0, 1.0, 1.0, 2.0],
        }
    )


@pytest.fixture
def processed_srag_data():
    df = pd.DataFrame(
        {
            "EVOLUCAO": [1, 2, 1],
            "DT_SIN_PRI": ["2025-05-01", "2024-12-15", np.nan],
            "SEM_PRI": [20, 21, 23],
            "UTI": [1, 2, 1],
            "HOSPITAL": [1, 1, 1],
            "VACINA": [1, 1, 2],
        }
    )
    df["DT_SIN_PRI"] = pd.to_datetime(
        df["DT_SIN_PRI"], errors="coerce", format="%Y-%m-%d"
    )
    return df


def test_preprocess_data(sample_srag_data, processed_srag_data):
    preprocessed_data = manager.preprocess_data(sample_srag_data)
    pd.testing.assert_frame_equal(
        preprocessed_data.reset_index(drop=True),
        processed_srag_data.reset_index(drop=True),
    )


def test_obtain_url():
    file_pattern = "INFLUD\d{2}-\d{2}-\d{2}-\d{4}\.csv"
    url = manager.get_latest_file_url(file_pattern)
    assert url.endswith(".csv")
