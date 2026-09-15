import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def create_db_engine():
    return create_engine(
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
        f"/{os.getenv('DB_NAME')}"
    )


# Загрузка данных о погоде в PostgreSQL
def load_weather_data(weather_df):
    engine = create_db_engine()

    weather_df.to_sql("weather_hourly", engine, if_exists="replace", index=False)

    print("Данные о погоде успешно загружены в PostgreSQL.")


# Загрузка данных о качестве воздуха в PostgreSQL
def load_air_quality_data(air_quality_df):
    engine = create_db_engine()

    air_quality_df.to_sql(
        "air_quality_hourly", engine, if_exists="replace", index=False
    )

    print("Данные о качестве воздуха успешно загружены в PostgreSQL.")
