import pandas as pd
from sqlalchemy.engine import Engine

from app.agents.state import AgentState
from app.config.settings import load_settings

settings = load_settings()
engine = settings.engine


def data_loader_node(state: AgentState) -> AgentState:
    table_name = settings.table_name
    with engine.connect() as conn:
        df = pd.read_sql_table(table_name, conn, parse_dates=["DT_SIN_PRI"])

    state["data"] = df
    return state
