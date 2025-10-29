from typing import Any

import pandas as pd
from langchain_core.tools import BaseTool


class MetricsTool(BaseTool):
    name = "metrics_tool"
    description = "A tool to compute various metrics for data analysis."

    def _calculate_mortality_rate(self, data: pd.DataFrame) -> float:
        total_cases = len(data)
        deaths = data[data.EVOLUCAO == 3]["EVOLUCAO"].sum()
        mortality_rate = (deaths / total_cases) * 100 if total_cases > 0 else 0
        return mortality_rate

    def _run(self, data: pd.DataFrame) -> dict[str, Any]:
        metrics = {
            "mortality_rate": self._calculate_mortality_rate(data),
        }
        return metrics
