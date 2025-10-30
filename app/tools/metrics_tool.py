from typing import Any

import pandas as pd
from langchain_core.tools import BaseTool


class MetricsTool(BaseTool):
    name = "metrics_tool"
    description = "A tool to compute various metrics for data analysis."

    def _generate_last_month_data(self, data: pd.DataFrame) -> pd.DataFrame:
        if data.DT_SIN_PRI.dtype != "datetime64[ns]":
            data["DT_SIN_PRI"] = pd.to_datetime(
                data["DT_SIN_PRI"], errors="coerce", format="%Y-%m-%d"
            )
        last_date = data.DT_SIN_PRI.max()
        last_month_data = data[
            pd.to_datetime(data.DT_SIN_PRI)
            >= (pd.to_datetime(last_date) - pd.DateOffset(months=1))
        ]
        return last_month_data

    def _calculate_total_mortality_rate(self, data: pd.DataFrame) -> float:
        total_cases = len(data)
        deaths = data[data.EVOLUCAO == 3]["EVOLUCAO"].sum()
        mortality_rate = (deaths / total_cases) * 100 if total_cases > 0 else 0
        return mortality_rate

    def _calculate_last_month_mortality_rate(self, data: pd.DataFrame) -> float:
        last_month_data = self._generate_last_month_data(data)
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

    def _calculate_case_increase_rate(self, data: pd.DataFrame) -> float:
        last_month_data = self._generate_last_month_data(data)
        last_month_data.MONTH = pd.to_datetime(last_month_data.DT_SIN_PRI).dt.month
        month_counts = last_month_data.MONTH.value_counts().sort_index()
        return month_counts.pct_change().iloc[-1] * 100

    def _run(self, data: pd.DataFrame) -> dict[str, Any]:
        metrics = {
            "total_mortality_rate": self._calculate_total_mortality_rate(data),
            "last_month_mortality_rate": self._calculate_last_month_mortality_rate(
                data
            ),
            "case_increase_rate": self._calculate_case_increase_rate(data),
        }
        return metrics
