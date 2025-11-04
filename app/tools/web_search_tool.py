import logging

import requests
from bs4 import BeautifulSoup
from langchain.tools import BaseTool
from serpapi import GoogleSearch

from app.config.settings import load_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = load_settings()


class WebSearchTool(BaseTool):
    name: str = "web_search_tool"
    description: str = (
        "A tool to perform web searches and retrieve relevant information from the internet. "
        "Useful for obtaining up-to-date information on various topics."
    )

    def _search_news(self, query: str, num_results: int = 5) -> list[dict]:
        try:
            search = GoogleSearch(
                {
                    "q": query,
                    "tbm": "nws",
                    "api_key": settings.serp_api_key,
                    "num": num_results,
                }
            )
            results = search.get_dict()
            news_results = results.get("news_results", [])

            return news_results
        except Exception as e:
            logger.info(f"An error occurred during the web search: {str(e)}")
            return []

    def _extract_news_content(self, url: str) -> str:
        try:
            response = requests.get(
                url, timeout=10, headers=settings.web_search_headers
            )
            soup = BeautifulSoup(response.content, "html.parser")
            article = soup.find("article")
            paragraphs = article.find_all("p") if article else soup.find_all("p")
            content = "\n".join([para.get_text() for para in paragraphs])
            return content
        except Exception as e:
            logger.info(f"An error occurred while extracting content: {str(e)}")
            return "Content could not be retrieved."

    def get_srag_news(self, query: str, num_results: int = 5) -> str:
        news = self._search_news(query, num_results)
        news_contents = []
        for item in news:
            title = item.get("title", "No Title")
            link = item.get("link", "")
            snippet = item.get("snippet", "")
            content = self._extract_news_content(link)
            news_contents.append(
                f"Title: {title}\nLink: {link}\nSnippet: {snippet}\nContent: {content}\n"
            )
        return "\n".join(news_contents)

    def _run(self, query: str) -> str:
        return self.get_srag_news(query)
