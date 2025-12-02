import pytest
import pandas as pd
from app.tools.plot_data_tool import PlotDataTool


@pytest.fixture
def mock_data() -> pd.DataFrame:
    df = pd.read_csv("tests/data/metrics_data.csv", parse_dates=["DT_SIN_PRI"])
    return df


def test_plot_data(mock_data: pd.DataFrame):
    plot_data_tool = PlotDataTool(mock_data)
    daily_data = plot_data_tool.get_daily_cases(mock_data)
    monthly_data = plot_data_tool.get_monthly_cases(mock_data)

    assert len(daily_data == 8)
    assert len(monthly_data == 2)
