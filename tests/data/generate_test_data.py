import pandas as pd
from app.config.settings import load_settings

settings = load_settings()
engine = settings.engine


def generate_test_data() -> None:
    with engine.connect() as conn:
        df = pd.read_sql_table("srag_features", conn, parse_dates=["DT_SIN_PRI"])
    cols_of_interest = [
        "DT_SIN_PRI",
        "CS_SEXO",
        "TP_CLASSI_FIN",
        "NU_IDADE_N",
        "OUTCOME",
    ]

    test_df = (
        df[df["DT_SIN_PRI"].between("2025-08-01", "2025-09-30")]
        .sample(20, random_state=0)
        .sort_values(by="DT_SIN_PRI")[cols_of_interest]
    )

    output_path = "tests/data/metrics_data.csv"
    test_df.to_csv(output_path, index=False)
    print(f"Test data written to {output_path}")


if __name__ == "__main__":
    generate_test_data()
