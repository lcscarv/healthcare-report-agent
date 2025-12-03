import streamlit as st
import pandas as pd
from langchain_openai.chat_models import ChatOpenAI

from app.agents.report_agent import ReportAgent
from app.config.settings import load_settings
from app.services.plot_data_service import plot_daily, plot_monthly

settings = load_settings()
engine = settings.engine

loading_ph = st.empty()

with loading_ph.container():
    st.markdown("## ⏳ Loading Dashboard...")
    st.write("Please wait while we fetch data and prepare the layout.")
    st.spinner()

with engine.connect() as conn:
    data = pd.read_sql_table(settings.table_name, conn, parse_dates=["DT_SIN_PRI"])
llm = ChatOpenAI(
    name=settings.model_name, temperature=0, api_key=settings.openai_api_key
)
agent = ReportAgent.from_data_and_llm(data, llm)
final_state = agent.run()
latest_date = pd.to_datetime(data["DT_SIN_PRI"]).max()

loading_ph.empty()

st.title("💉 SRAG Monitoring Dashboard")
st.header("📌 About")
st.markdown(
    f"""
    This dashboard provides a comprehensive overview of Severe Acute Respiratory Syndrome (SRAG) cases, 
    utilizing the latest data to present key metrics and visualizations.  
    The information is sourced from the Brazilian Ministry of Health's Open Data platform, 
    ensuring up-to-date and accurate reporting.  
    **Data Source:** [OpenDataSUS SRAG Dataset](https://opendatasus.saude.gov.br/dataset/srag-2021-a-2024/resource/20c49de3-ddc3-4b76-a942-1518eaae9c91)  
    **Latest Data Update:** {latest_date.strftime("%Y-%m-%d")}
    """
)
st.header("📋 Summary Report")
st.markdown(final_state["response"].content)

st.header("🔍 Report Details")
metrics = final_state["metrics"]

st.subheader("📊 Metrics Overview")
st.markdown(
    "**Key performance indicators comparing the latest reference month to the previous month**"
)
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Mortality Change (vs. Last Month)",
    f"{metrics['last_month_mortality_rate']}%",
)
col2.metric("Case Change (vs. Last Month)", f"{metrics['case_increase_rate']}%")
col3.metric(
    "ICU Admissions Change (vs. Last Month)",
    f"{metrics['icu_admission_rate']}%",
)
col4.metric("Vaccination Change (vs. Last Month)", f"{metrics['vaccination_rate']}%")

st.subheader("Data Charts")
col_a, col_b = st.columns(2)
col_a.markdown("📅 **Daily Cases (Up to 30 days)**")
fig_daily = plot_daily(final_state["plot_data"]["daily_cases"])
col_a.plotly_chart(fig_daily)

col_b.markdown("📆 **Monthly Cases (Up to 12 months)**")
fig_monthly = plot_monthly(final_state["plot_data"]["monthly_cases"])
col_b.plotly_chart(fig_monthly)
