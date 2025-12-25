from langgraph.graph import StateGraph, START, END
from app.agents.state import AgentState
from app.nodes.plot_data_node import get_plot_data_node
from app.nodes.plot_data_insights_node import get_plot_insights_node
from app.nodes.build_context_node import context_builder_node
from app.nodes.metrics_node import metrics_node
from app.nodes.news_scrapping_node import web_search_node
from app.nodes.summarizer_node import summmarizer_node
from app.nodes.audit_summary_node import audit_summary_node


def should_continue(state: AgentState) -> str:
    if state.is_valid or state.iteration_count >= 3:
        return END
    return "summarizer_node"


workflow = StateGraph(state_schema=AgentState)

workflow.add_node("web_search_node", web_search_node)
workflow.add_node("metrics_node", metrics_node)
workflow.add_node("get_plot_data_node", get_plot_data_node)
workflow.add_node("get_plot_insights_node", get_plot_insights_node)
workflow.add_node("context_builder_node", context_builder_node)
workflow.add_node("summarizer_node", summmarizer_node)
workflow.add_node("audit_summary_node", audit_summary_node)

workflow.add_edge(START, "metrics_node")
workflow.add_edge(START, "web_search_node")
workflow.add_edge(START, "get_plot_data_node")
workflow.add_edge("get_plot_data_node", "get_plot_insights_node")
workflow.add_edge("metrics_node", "context_builder_node")
workflow.add_edge("web_search_node", "context_builder_node")
workflow.add_edge("get_plot_insights_node", "context_builder_node")
workflow.add_edge("context_builder_node", "summarizer_node")
workflow.add_edge("summarizer_node", "audit_summary_node")

workflow.add_conditional_edges("audit_summary_node", should_continue)

graph = workflow.compile()
