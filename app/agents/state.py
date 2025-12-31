from dataclasses import dataclass
from typing import Any, Optional, Protocol
import pandas as pd
from langchain_core.messages import AIMessage
from langchain.chat_models import BaseChatModel


class ContinuationState(Protocol):
    is_valid: bool
    iteration_count: int


@dataclass
class AgentState:
    data: pd.DataFrame
    llm: BaseChatModel
    audit_llm: BaseChatModel
    query: str = "('SRAG' OR 'Síndrome Respiratória Aguda Grave') AND Brasil"
    context: Optional[dict[str, Any]] = None
    metrics: Optional[dict[str, float]] = None
    news_content: Optional[str] = None
    response: Optional[AIMessage] = None
    plot_data: Optional[dict[str, pd.DataFrame]] = None
    plot_insights: Optional[AIMessage] = None
    iteration_count: int = 0
    is_valid: bool = False
    feedback: Optional[str] = None
    risk_score: Optional[float] = None

    @classmethod
    def initialize_state(
        cls, data: pd.DataFrame, llm: BaseChatModel, audit_llm: BaseChatModel
    ) -> "AgentState":
        return cls(data=data, llm=llm, audit_llm=audit_llm)
