import pandas as pd
import numpy as np
import os

def generate_data():
    dates = pd.date_range(start="2018-01-01", end="2023-12-31")
    data = []

    for i, date in enumerate(dates):
        day = date.timetuple().tm_yday

        seasonal = 10 * np.sin(2 * np.pi * day / 365)
        trend = 0.01 * i
        noise = np.random.normal(0, 1)

        temperature = 25 + seasonal + trend + noise

        # Rainfall (monsoon simulation)
        if 150 < day < 250:
            rainfall = np.random.uniform(5, 20)
        else:
            rainfall = np.random.uniform(0, 2)

        # Add anomalies
        if np.random.rand() < 0.01:
            temperature += np.random.uniform(8, 12)

        if np.random.rand() < 0.01:
            rainfall += np.random.uniform(20, 50)

        humidity = 50 + rainfall * 2 + np.random.uniform(-5, 5)

        data.append([date, round(temperature, 2), round(rainfall, 2), round(humidity, 2)])

    df = pd.DataFrame(data, columns=["date", "temperature", "rainfall", "humidity"])

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/climate_data.csv", index=False)

    print("✅ Dataset generated successfully!")

if __name__ == "__main__":
    generate_data()