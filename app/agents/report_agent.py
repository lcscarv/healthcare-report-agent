from typing import Any

import pandas as pd
from langchain.chat_models import BaseChatModel
from app.agents.report_workflow import graph
from app.agents.state import AgentState
from app.config.settings import load_settings

settings = load_settings()


class ReportAgent:
    def __init__(self, initial_state: AgentState):
        self.state = initial_state

    def run(self) -> dict[str, Any]:
        final_state = graph.invoke(self.state)
        return final_state

    @classmethod
    def from_data_and_llm(cls, data: pd.DataFrame, llm: BaseChatModel) -> "ReportAgent":
        state = AgentState.initialize_state(data, llm)
        return cls(state)
