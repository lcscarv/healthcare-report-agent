from langchain.messages import AIMessage

from app.agents.state import AgentState
from app.config.settings import load_settings
from app.prompts.prompts import PromptTemplates

settings = load_settings()


def summmarizer_node(state: AgentState) -> dict[str, AIMessage]:
    llm = state.llm
    if state.iteration_count >= 1:
        prompt = PromptTemplates.SUMMARY_REWRITE_WITH_FEEDBACK.value.format(
            context_data=state.context,
            original_summary=state.response.content,
            feedback=state.feedback,
        )
        response = llm.invoke(prompt)
        return {"response": response}

    prompt = PromptTemplates.REPORT_SUMMARY.value.format(context_data=state.context)
    response = llm.invoke(prompt)
    return {"response": response}
