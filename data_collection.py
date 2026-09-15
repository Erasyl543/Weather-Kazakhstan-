import requests
import pandas as pd
from datetime import datetime, timedelta
from config import cities  # Импортируем список городов и их координаты


# Функция для получения данных о погоде
def fetch_weather_data(lat, lon, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive"  # Используем архивный API
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relativehumidity_2m,windspeed_10m",
        "timezone": "Asia/Almaty",
        "start_date": start_date,
        "end_date": end_date,
    }
    response = requests.get(url, params=params)
    return response.json()


# Функция для получения данных о качестве воздуха
def fetch_air_quality_data(lat, lon, start_date, end_date):
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide",
        "timezone": "Asia/Almaty",  # Таймзона для Казахстана
        "start_date": start_date,
        "end_date": end_date,
    }
    response = requests.get(url, params=params)
    return response.json()


# Получаем текущую дату и дату 90 дней назад от текущей даты
end_date = datetime.today().strftime("%Y-%m-%d")  # Текущая дата
start_date = (datetime.today() - timedelta(days=90)).strftime(
    "%Y-%m-%d"
)  # 90 дней назад

# Печать, чтобы убедиться, что расчёт правильный
print(f"Fetching data from {start_date} to {end_date}")

# Сбор данных для каждого города
weather_data = []
air_quality_data = []

for city in cities:
    weather_response = fetch_weather_data(
        city["lat"], city["lon"], start_date, end_date
    )
    air_quality_response = fetch_air_quality_data(
        city["lat"], city["lon"], start_date, end_date
    )

    # Добавляем данные о погоде в список
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

        air_quality_data.append(
            {
                "city": city["city"],
                "timestamp": air_quality_response["hourly"]["time"][i],
                "pm10": air_quality_response["hourly"]["pm10"][i],
                "pm2_5": air_quality_response["hourly"]["pm2_5"][i],
                "carbon_monoxide": air_quality_response["hourly"]["carbon_monoxide"][i],
                "nitrogen_dioxide": air_quality_response["hourly"]["nitrogen_dioxide"][
                    i
                ],
            }
        )

# Преобразуем в DataFrame
weather_df = pd.DataFrame(weather_data)
air_quality_df = pd.DataFrame(air_quality_data)

# Выведем первые несколько строк для проверки
print(weather_df.head())
print(air_quality_df.head())
