from app.agents.state import AgentState
from app.prompts.prompts import PromptTemplates
from app.services.llm_services import AuditResult


def audit_summary_node(state: AgentState) -> dict:
    prompt = PromptTemplates.AUDIT_SUMMARY.value
    context_data = {
        "summary": state.response.content,
        "metrics": state.metrics,
        "news": state.context["news_content"],
    }
    formatted_prompt = prompt.format(context_data=context_data)
    llm_response: AuditResult = state.audit_llm.invoke(formatted_prompt)  # type: ignore
    return {
        "iteration_count": state.iteration_count + 1,
        "feedback": llm_response.feedback,
        "is_valid": llm_response.is_valid,
        "risk_score": llm_response.risk_score,
    }
