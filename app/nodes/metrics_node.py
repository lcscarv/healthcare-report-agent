import pandas as pd
from app.tools.metrics_tool import MetricsTool


def metrics_node(srag_data: pd.DataFrame) -> str:
    tool = MetricsTool()
    return tool.run(srag_data)  # type: ignore
