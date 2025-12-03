import pandas as pd
from app.agents.state import AgentState
from langchain.messages import AIMessage
from app.prompts.prompts import PromptTemplates


def get_plot_insights_node(state: AgentState) -> dict[str, AIMessage]:
    llm = state.llm
    plot_data: dict[str, pd.DataFrame] = state.plot_data  # type: ignore

    prompt = PromptTemplates.CHART_INSIGHT.value.format(
        daily_cases_data=plot_data["daily_cases"].to_dict(orient="records"),
        monthly_cases_data=plot_data["monthly_cases"].to_dict(orient="records"),
    )
    response = llm.invoke(prompt)

    return {"plot_insights": response}
