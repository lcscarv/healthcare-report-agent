from typing import Any

import pandas as pd
import pytest
import numpy as np

from app.tools.metrics_tool import MetricsTool

metrics_tool = MetricsTool()


@pytest.fixture
def mock_data() -> pd.DataFrame:
    df = pd.read_csv("tests/data/metrics_data.csv")
    return df


@pytest.fixture
def mock_metrics() -> dict[str, Any]:
    return {
        "last_month_mortality_rate": np.nan,
        "case_increase_rate": -41.7,
        "icu_admission_rate": 0.0,
        "vaccination_rate": -20.0,
    }


def test_metrics(mock_data, mock_metrics):
    metrics = metrics_tool.run(mock_data)
    for key, value in mock_metrics.items():
        if np.isnan(value):
            assert np.isnan(metrics[key])
        else:
            assert metrics[key] == value
