from typing import Any

import pandas as pd
from langchain_core.tools import BaseTool


class MetricsTool(BaseTool):
    name = "metrics_tool"
    description = "A tool to compute various metrics for data analysis."

    def _get_previous_month(self, year: int, month: int) -> tuple[int, int]:
        if month == 1:
            return year - 1, 12
        else:
            return year, month - 1

    def get_month_data(
        self, data: pd.DataFrame, year: int, month: int, cutoff_day: int
    ) -> pd.DataFrame:
        filter_mask = (
            (data["DT_SIN_PRI"].dt.year == year)
            & (data["DT_SIN_PRI"].dt.month == month)
            & (data["DT_SIN_PRI"].dt.day <= cutoff_day)
        )
        return data[filter_mask]

    def _generate_last_month_data(
        self, data: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        if data.DT_SIN_PRI.dtype != "datetime64[ns]":
            data["DT_SIN_PRI"] = pd.to_datetime(
                data["DT_SIN_PRI"], errors="coerce", format="%Y-%m-%d"
            )
        last_date = data.DT_SIN_PRI.max()
        cutoff_day = last_date.day
        year, month = last_date.year, last_date.month
        prev_month_year, prev_month = self._get_previous_month(year, month)

        previous_month_data = self.get_month_data(
            data, prev_month_year, prev_month, cutoff_day
        )
        current_month_data = self.get_month_data(data, year, month, cutoff_day)

        return previous_month_data, current_month_data

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
        month_counts = last_month_data.MONTH.value_counts().sort_index()
        return month_counts.pct_change().iloc[-1] * 100

    def _calculate_uti_admission_rate(self, data: pd.DataFrame) -> float:
        last_month_data = self._generate_last_month_data(data)
        uti_admission_counts = (
            last_month_data[last_month_data.UTI == 1]["UTI"].value_counts().sort_index()
        )
        return uti_admission_counts.pct_change().iloc[-1] * 100

    def _run(self, data: pd.DataFrame) -> dict[str, Any]:
        metrics = {
            "total_mortality_rate": self._calculate_total_mortality_rate(data),
            "last_month_mortality_rate": self._calculate_last_month_mortality_rate(
                data
            ),
            "case_increase_rate": self._calculate_case_increase_rate(data),
        }
        return metrics
