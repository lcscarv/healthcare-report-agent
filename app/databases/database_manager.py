import logging

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    Date,
    PrimaryKeyConstraint,
    Engine,
)
from sqlalchemy.exc import SQLAlchemyError
from app.config.settings import load_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = load_settings()


def create_database(engine: Engine) -> None:
    try:
        metadata = MetaData()

        srag_features = Table(
            "srag_features",
            metadata,
            Column("id", String, primary_key=True),
            Column("EVOLUCAO", Integer),
            Column("DT_SIN_PRI", Date),
            Column("SEM_PRI", Integer),
            Column("UTI", Integer),
            Column("HOSPITAL", Integer),
            Column("VACINA", Integer),
            PrimaryKeyConstraint("id", name="srag_features_pk"),
        )

        metadata.create_all(engine)
        logger.info("Database and tables created successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Error creating database: {e}")


if __name__ == "__main__":
    engine = create_engine(settings.database_url)
    create_database(engine)
