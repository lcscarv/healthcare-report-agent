import pandas as pd


class PlotDataTool:
    name: str = "plot_data_tool"
    description: str = "Tool to generate the data that will be used to generate the plots as well as the insights that follows them."

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def get_daily_cases(self, df: pd.DataFrame) -> pd.DataFrame:
        last_date = df["DT_SIN_PRI"].max()
        cutoff_date = last_date - pd.Timedelta(days=30)
        last_month_data = df[df["DT_SIN_PRI"].between(cutoff_date, last_date)]

        daily_cases = (
            last_month_data.groupby(last_month_data["DT_SIN_PRI"].dt.date)
            .size()
            .reset_index(name="N_CASOS")
        )
        return daily_cases

    def get_monthly_cases(self, df: pd.DataFrame) -> pd.DataFrame:
        last_date = df["DT_SIN_PRI"].max()
        cutoff_date = last_date - pd.DateOffset(months=12)
        last_year_data = df[df["DT_SIN_PRI"] >= cutoff_date]

        # Aggregate monthly cases
        monthly_cases = (
            last_year_data.groupby(last_year_data["DT_SIN_PRI"].dt.to_period("M"))
            .size()
            .reset_index(name="N_CASOS")
        )

        return monthly_cases

    def run(self):
        return {
            "daily_cases": self.get_daily_cases(self.df),
            "monthly_cases": self.get_monthly_cases(self.df),
        }
