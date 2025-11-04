from langgraph.graph import StateGraph, START, END

from app.agents.state import AgentState
from app.nodes.summarizer_node import summmarizer_node
from app.nodes.build_context_node import context_builder_node
from app.nodes.data_load_node import data_loader_node
from app.nodes.news_scrapping_node import web_search_node
from app.nodes.metrics_node import metrics_node


workflow = StateGraph(state_schema=AgentState)

workflow.add_node("data_loader_node", data_loader_node)
workflow.add_node("web_search_node", web_search_node)
workflow.add_node("metrics_node", metrics_node)
workflow.add_node("context_builder_node", context_builder_node)
workflow.add_node("summarizer_node", summmarizer_node)

workflow.add_edge(START, "data_loader_node")
workflow.add_edge("data_loader_node", "metrics_node")
workflow.add_edge("metrics_node", "web_metrics_node")
workflow.add_edge("web_metrics_node", "context_builder_node")
workflow.add_edge("context_builder_node", "summarizer_node")
workflow.add_edge("summarizer_node", END)

graph = workflow.compile()
