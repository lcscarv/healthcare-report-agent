from langchain_openai import ChatOpenAI

from app.agents.report_workflow import graph
from app.agents.state import AgentState
from app.config.settings import load_settings

settings = load_settings()


class ReportAgent:
    def __init__(self, initial_state: AgentState):
        self.state = initial_state

    def run(self) -> AgentState:
        final_state = graph.invoke(self.state)
        return final_state
