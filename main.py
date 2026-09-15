from datetime import datetime, timedelta

import pandas as pd

from config import cities
from data_collection import fetch_weather_data, fetch_air_quality_data
from data_processing import (
    preprocess_weather_data,
    preprocess_air_quality_data,
)
from database import load_weather_data, load_air_quality_data


def main():
    # Получаем текущую дату и дату 90 дней назад
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=90)).strftime("%Y-%m-%d")

    # Списки для хранения собранных данных
    weather_data = []
    air_quality_data = []

    # Сбор данных для каждого города
    for city in cities:
        weather_response = fetch_weather_data(
            city["lat"],
            city["lon"],
            start_date,
            end_date,
        )

        air_quality_response = fetch_air_quality_data(
            city["lat"],
            city["lon"],
            start_date,
            end_date,
        )

        # Добавляем данные о погоде
        for i in range(len(weather_response["hourly"]["temperature_2m"])):
            weather_data.append(
                {
                    "city": city["city"],
                    "timestamp": weather_response["hourly"]["time"][i],
                    "temperature": weather_response["hourly"]["temperature_2m"][i],
                    "humidity": weather_response["hourly"]["relativehumidity_2m"][i],
                    "windspeed": weather_response["hourly"]["windspeed_10m"][i],
                }
            )

            # Добавляем данные о качестве воздуха
            air_quality_data.append(
                {
                    "city": city["city"],
                    "timestamp": air_quality_response["hourly"]["time"][i],
                    "pm10": air_quality_response["hourly"]["pm10"][i],
                    "pm2_5": air_quality_response["hourly"]["pm2_5"][i],
                    "carbon_monoxide": air_quality_response["hourly"][
                        "carbon_monoxide"
                    ][i],
                    "nitrogen_dioxide": air_quality_response["hourly"][
                        "nitrogen_dioxide"
                    ][i],
                }
            )

    # Преобразуем данные в DataFrame
    weather_df = pd.DataFrame(weather_data)
    air_quality_df = pd.DataFrame(air_quality_data)

    # Обработка данных
    weather_df = preprocess_weather_data(weather_df)
    air_quality_df = preprocess_air_quality_data(air_quality_df)

    # Загрузка данных в PostgreSQL
    load_weather_data(weather_df)
    load_air_quality_data(air_quality_df)


if __name__ == "__main__":
    main()
