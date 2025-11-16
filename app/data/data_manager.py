import logging

import pandas as pd
import requests
from sqlalchemy import Engine
from sqlalchemy.types import DateTime
from app.config.settings import load_settings

settings = load_settings()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_TYPE_MAP = {
    "float64": "int64",
    "object": "string",
}


class DataManager:
    def __init__(self):
        self.srag_data_path = settings.srag_data_path

    def check_data_path(self) -> bool:
        response = requests.get(self.srag_data_path)
        if response.status_code == 200:
            return True
        else:
            return False

    def load_srag_data(self) -> pd.DataFrame:
        """Load SRAG data from the specified CSV file path."""
        if not self.check_data_path():
            raise ValueError("Data path is not accessible.")
        cols_of_interest = [
            "EVOLUCAO",
            "DT_SIN_PRI",
            "SEM_PRI",
            "UTI",
            "HOSPITAL",
            "VACINA",
        ]
        return pd.read_csv(self.srag_data_path, sep=";", usecols=cols_of_interest)

    def change_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.astype(
            {
                col: DATA_TYPE_MAP[str(df[col].dtype)]
                for col in df.columns
                if str(df[col].dtype) in DATA_TYPE_MAP
            }
        )

    def treat_date_feature(self, date_feature: pd.Series) -> pd.Series:
        date_feature = pd.to_datetime(date_feature, errors="coerce", format="%Y-%m-%d")
        invalid_years = ~date_feature.dt.year.between(2024, 2025)
        invalid_months = ~date_feature.dt.month.between(1, 12)

        date_feature[invalid_years | invalid_months] = pd.NaT

        return date_feature

    def preprocess_data(self, srag_df: pd.DataFrame) -> pd.DataFrame:
        srag_df_treated = srag_df.copy()
        srag_df_treated["DT_SIN_PRI"] = self.treat_date_feature(
            srag_df_treated["DT_SIN_PRI"]
        )
        srag_df_treated.loc[
            (srag_df_treated.HOSPITAL.isna() & ~srag_df_treated.UTI.isna()),
            "HOSPITAL",
        ] = 1

        srag_df_treated = srag_df_treated[~srag_df_treated.HOSPITAL.isna()]
        srag_df_treated = srag_df_treated[~srag_df_treated.EVOLUCAO.isna()]
        srag_df_treated = srag_df_treated[~srag_df_treated.VACINA.isna()]

        srag_df_treated.loc[srag_df_treated.UTI.isna(), "UTI"] = 2

        srag_df_treated.loc[srag_df_treated.UTI == 9, "UTI"] = 2
        srag_df_treated.loc[srag_df_treated.HOSPITAL == 9, "HOSPITAL"] = 1

        srag_df_treated = srag_df_treated[~(srag_df_treated.VACINA == 9)]
        srag_df_treated = srag_df_treated[~(srag_df_treated.EVOLUCAO == 9)]

        srag_df_treated = self.change_data_types(srag_df_treated)

        return srag_df_treated

    def load_to_database(self, df: pd.DataFrame, engine: Engine, append: bool = False):
        with engine.connect() as connection:
            df.to_sql(
                "srag_features",
                con=connection,
                if_exists="append" if append else "replace",
                index_label="id",
                dtype={
                    "DT_SIN_PRI": DateTime(),  # enforce SQL datetime type
                },
            )


def processing_pipeline(engine: Engine):
    data_manager = DataManager()
    logger.info("Loading SRAG data.")
    srag_data = data_manager.load_srag_data()
    logger.info("Preprocessing data.")
    preprocessed_data = data_manager.preprocess_data(srag_data)

    logger.info("Loading data into database.")
    data_manager.load_to_database(preprocessed_data, engine)
    logger.info("Pipeline completed successfully.")


if __name__ == "__main__":
    processing_pipeline(settings.engine)
