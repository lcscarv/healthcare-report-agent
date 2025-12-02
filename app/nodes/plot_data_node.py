from app.agents.state import AgentState
from app.tools.plot_data_tool import PlotDataTool


def get_plot_data_node(state: AgentState) -> dict[str, dict]:
    get_plot_data_tool = PlotDataTool(state.data)
    plot_data = get_plot_data_tool.run()

    return {"plot_data": plot_data}
