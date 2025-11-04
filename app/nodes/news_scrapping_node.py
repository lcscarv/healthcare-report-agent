from app.agents.state import AgentState
from app.tools.web_search_tool import WebSearchTool


def web_search_node(state: AgentState) -> AgentState:
    query = state["query"]
    tool = WebSearchTool()
    web_context = tool.run(query)
    state["news_content"] = web_context

    return state
