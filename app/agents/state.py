from dataclasses import dataclass
from typing import Any
import pandas as pd
from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI


@dataclass
class AgentState:
    context: dict[str, Any]
    data: pd.DataFrame
    llm: ChatOpenAI
    query: str
    metrics: dict[str, float]
    news_content: str
    response: AIMessage
