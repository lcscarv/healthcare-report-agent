from app.tools.web_search_tool import WebSearchTool


def web_search_node(query: str) -> str:
    tool = WebSearchTool()
    return tool.run(query)
