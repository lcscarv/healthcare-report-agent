from typing import Any
from app.agents.state import AgentState


def context_builder_node(state: AgentState) -> dict[str, dict]:
    news_content = state.news_content
    metrics = state.metrics
    plot_insights = state.plot_insights
    context: dict[str, Any] = metrics.copy()
    context["news_content"] = news_content
    context["plot_insights"] = plot_insights.content if plot_insights else None
    return {"context": context}
