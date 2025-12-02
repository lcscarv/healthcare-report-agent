import pandas as pd
import plotly.express as px


def update_feature_names(
    df: pd.DataFrame, feature_mapping: dict[str, str]
) -> pd.DataFrame:
    return df.rename(columns=feature_mapping)


def plot_daily(df_last_30: pd.DataFrame):
    df_last_30 = update_feature_names(
        df_last_30, {"DT_SIN_PRI": "Days", "N_CASOS": "Cases"}
    )
    return px.line(df_last_30, x="Days", y="Cases")


def plot_monthly(df_last_12: pd.DataFrame):
    df_last_12 = update_feature_names(
        df_last_12, {"DT_SIN_PRI": "Months", "N_CASOS": "Cases"}
    )
    df_last_12["Months"] = df_last_12["Months"].astype(str)
    return px.bar(df_last_12, x="Months", y="Cases")
