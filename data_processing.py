import pandas as pd


# Преобразуем данные о погоде
def preprocess_weather_data(weather_df):
    weather_df["timestamp"] = pd.to_datetime(weather_df["timestamp"])
    weather_df["temperature"] = weather_df["temperature"].astype(float)
    weather_df["humidity"] = weather_df["humidity"].astype(float)
    weather_df["windspeed"] = weather_df["windspeed"].astype(float)

    weather_df.drop_duplicates(inplace=True)
    weather_df["temperature"] = weather_df["temperature"].round(2)
    weather_df["humidity"] = weather_df["humidity"].round(2)
    weather_df["windspeed"] = weather_df["windspeed"].round(2)

    return weather_df


# Преобразуем данные о качестве воздуха
def preprocess_air_quality_data(air_quality_df):
    air_quality_df["timestamp"] = pd.to_datetime(air_quality_df["timestamp"])
    air_quality_df["pm10"] = air_quality_df["pm10"].astype(float)
    air_quality_df["pm2_5"] = air_quality_df["pm2_5"].astype(float)
    air_quality_df["carbon_monoxide"] = air_quality_df["carbon_monoxide"].astype(float)
    air_quality_df["nitrogen_dioxide"] = air_quality_df["nitrogen_dioxide"].astype(
        float
    )

    air_quality_df["pm10"] = air_quality_df["pm10"].round(2)
    air_quality_df["pm2_5"] = air_quality_df["pm2_5"].round(2)
    air_quality_df["carbon_monoxide"] = air_quality_df["carbon_monoxide"].round(2)
    air_quality_df["nitrogen_dioxide"] = air_quality_df["nitrogen_dioxide"].round(2)

    air_quality_df.drop_duplicates(inplace=True)

    return air_quality_df
