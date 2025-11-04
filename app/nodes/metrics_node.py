from app.agents.state import AgentState
from app.tools.metrics_tool import MetricsTool


def metrics_node(state: AgentState) -> AgentState:
    srag_data = state["data"]
    tool = MetricsTool()
    metrics = tool.run(srag_data)
    state["metrics"] = metrics
    return state
