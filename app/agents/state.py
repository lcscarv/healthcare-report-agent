from dataclasses import dataclass
from typing import Any, Optional
import pandas as pd
from langchain_core.messages import AIMessage
from langchain.chat_models import BaseChatModel


@dataclass
class AgentState:
    data: pd.DataFrame
    llm: BaseChatModel
    query: str = "('SRAG' OR 'Síndrome Respiratória Aguda Grave') AND Brasil"
    context: Optional[dict[str, Any]] = None
    metrics: Optional[dict[str, float]] = None
    news_content: Optional[str] = None
    response: Optional[AIMessage] = None
    plot_data: Optional[dict[str, pd.DataFrame]] = None
    plot_insights: Optional[AIMessage] = None

    @classmethod
    def initialize_state(cls, data: pd.DataFrame, llm: BaseChatModel):
        return cls(data=data, llm=llm)
