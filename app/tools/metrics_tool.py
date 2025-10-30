from typing import Any

import pandas as pd
from langchain_core.tools import BaseTool


class MetricsTool(BaseTool):
    name = "metrics_tool"
    description = "A tool to compute various metrics for data analysis."

    def _calculate_total_mortality_rate(self, data: pd.DataFrame) -> float:
        total_cases = len(data)
        deaths = data[data.EVOLUCAO == 3]["EVOLUCAO"].sum()
        mortality_rate = (deaths / total_cases) * 100 if total_cases > 0 else 0
        return mortality_rate

    def _calculate_last_month_mortality_rate(self, data: pd.DataFrame) -> float:
        most_recent_date = data["DT_SIN_PRI"].max()
        last_month_date = most_recent_date - pd.DateOffset(months=1)
        last_month_data = data[
            (data["DT_SIN_PRI"] > last_month_date)
            & (data["DT_SIN_PRI"] <= most_recent_date)
        ]
        total_cases_last_month = len(last_month_data)
        deaths_last_month = last_month_data[last_month_data.EVOLUCAO == 3][
            "EVOLUCAO"
        ].sum()
        mortality_rate_last_month = (
            (deaths_last_month / total_cases_last_month) * 100
            if total_cases_last_month > 0
            else 0
        )
        return mortality_rate_last_month

    def _run(self, data: pd.DataFrame) -> dict[str, Any]:
        metrics = {
            "total_mortality_rate": self._calculate_total_mortality_rate(data),
            "last_month_mortality_rate": self._calculate_last_month_mortality_rate(
                data
            ),
        }
        return metrics
