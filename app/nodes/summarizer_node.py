from langchain_openai import ChatOpenAI

from app.agents.state import AgentState
from app.config.settings import load_settings
from app.prompts.prompts import PromptTemplates

settings = load_settings()


def summmarizer_node(state: AgentState) -> AgentState:
    llm = state.llm
    prompt = PromptTemplates.REPORT_SUMMARY.value.format(data=state.context)
    response = llm.invoke(prompt)
    state.response = response
    return state
