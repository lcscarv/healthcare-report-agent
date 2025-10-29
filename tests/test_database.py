import pandas as pd
import pytest
import sqlalchemy

from app.databases.database_manager import create_database
from app.data.data_manager import DataManager

data_manager = DataManager()


@pytest.fixture
def mock_data() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "EVOLUCAO": [1, 2, 1],
            "DT_SIN_PRI": pd.to_datetime(
                ["2025-05-01", "2024-12-15", pd.NaT], errors="coerce", format="%Y-%m-%d"
            ),
            "SEM_PRI": [20, 21, 23],
            "UTI": [1, 2, 1],
            "HOSPITAL": [1, 1, 1],
            "VACINA": [1, 1, 2],
        }
    )
    return df


@pytest.fixture
def db_engine():
    engine = sqlalchemy.create_engine("sqlite:///tests/test_healthcare_reports.db")
    yield engine
    engine.dispose()


def test_database_creation(db_engine):
    create_database(db_engine)
    inspector = sqlalchemy.inspect(db_engine)
    tables = inspector.get_table_names()
    assert "srag_features" in tables


def test_database_connection(db_engine):
    with db_engine.connect() as conn:
        result = conn.execute(sqlalchemy.text("SELECT 1"))
        assert result.scalar() == 1


def test_insert_and_read_data(db_engine, mock_data):
    data_manager.load_to_database(mock_data, db_engine)
    with db_engine.connect() as conn:
        df_read = pd.read_sql_table("srag_features", conn, parse_dates=["DT_SIN_PRI"])
    assert not df_read.empty
    assert df_read.shape == mock_data.shape
    assert set(mock_data.columns) == set(df_read.columns)
