from typing import Any

import pandas as pd
import numpy as np
from langchain_core.tools import BaseTool


class MetricsTool(BaseTool):
    name: str = "metrics_tool"
    description: str = "A tool to compute various metrics for data analysis."

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

    def _generate_last_month_data(self, data: pd.DataFrame) -> pd.DataFrame:
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

        return pd.concat([previous_month_data, current_month_data], axis=0)

    def _calculate_total_mortality_rate(self, data: pd.DataFrame) -> float:
        total_cases = len(data)
        deaths = data[data.EVOLUCAO == 3]["EVOLUCAO"].sum()
        mortality_rate = (deaths / total_cases) * 100 if total_cases > 0 else 0
        return mortality_rate

    def _metric_calculation_function(
        self, data: pd.DataFrame, mask: pd.Series
    ) -> float:
        filtered_data = data[mask]
        filtered_data.MONTH = pd.to_datetime(filtered_data.DT_SIN_PRI).dt.month
        metric_agg_data = filtered_data.MONTH.value_counts().sort_index()
        return (
            metric_agg_data.pct_change().iloc[-1] * 100
            if len(metric_agg_data) > 1
            else np.nan
        )

    def _calculate_last_month_mortality_rate(self, data: pd.DataFrame) -> float:
        month_comparison_data = self._generate_last_month_data(data)

        month_compared_mortality_rate = self._metric_calculation_function(
            month_comparison_data, (month_comparison_data.EVOLUCAO == 3)
        )

        return month_compared_mortality_rate

    def _calculate_case_increase_rate(self, data: pd.DataFrame) -> float:
        last_month_data = self._generate_last_month_data(data)

        month_compared_case_growth_rate = self._metric_calculation_function(
            last_month_data, last_month_data.DT_SIN_PRI.notna()
        )
        return month_compared_case_growth_rate

    def _calculate_icu_admission_rate(self, data: pd.DataFrame) -> float:
        last_month_data = self._generate_last_month_data(data)

        month_compared_uti_admission_rate = self._metric_calculation_function(
            last_month_data, (last_month_data.UTI == 1)
        )
        return month_compared_uti_admission_rate

    def _run(self, data: pd.DataFrame) -> dict[str, Any]:
        metrics = {
            "total_mortality_rate": self._calculate_total_mortality_rate(data),
            "last_month_mortality_rate": self._calculate_last_month_mortality_rate(
                data
            ),
            "case_increase_rate": self._calculate_case_increase_rate(data),
            "icu_admission_rate": self._calculate_icu_admission_rate(data),
        }

        formatted_metrics = {
            k: (round(float(v), 1) if isinstance(v, float) else v)
            for k, v in metrics.items()
        }
        return formatted_metrics

    def run(self, tool_input: pd.DataFrame) -> dict[str, Any]:
        """
        Override the run method to accept a DataFrame as input.

        Args:
            tool_input (pd.DataFrame): The input data for metrics calculation.

        Returns:
            dict[str, Any]: The calculated metrics.
        """
        return self._run(tool_input)
