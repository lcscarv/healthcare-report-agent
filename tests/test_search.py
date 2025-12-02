from app.tools.web_search_tool import WebSearchTool


def test_web_search():
    tool = WebSearchTool()
    query = '("SRAG" OR "Síndrome Respiratória Aguda Grave") AND Brasil'
    results = tool.get_srag_news(query, num_results=20)
    assert isinstance(results, str)
    assert len(results) > 0
