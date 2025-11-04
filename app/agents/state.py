from typing import TypedDict, Any

import pandas as pd
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI


class AgentState(TypedDict):
    context: dict[str, Any]
    data: pd.DataFrame
    llm: ChatOpenAI
    query: str
    metrics: dict[str, float]
    news_content: str
    response: AIMessage
