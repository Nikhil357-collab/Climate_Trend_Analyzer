import pandas as pd
import os

def preprocess_data():
    df = pd.read_csv("data/raw/climate_data.csv")

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by="date")

    df.fillna(method='ffill', inplace=True)

    # Feature Engineering
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['temp_ma'] = df['temperature'].rolling(30).mean()

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/cleaned_data.csv", index=False)

    print("✅ Data preprocessing complete!")
    return df

if __name__ == "__main__":
    preprocess_data()