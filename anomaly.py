

from scipy.stats import zscore
import os

def detect_anomalies(df):
    df['z_score'] = zscore(df['temperature'])
    df['anomaly'] = df['z_score'].apply(lambda x: 1 if abs(x) > 3 else 0)

    anomalies = df[df['anomaly'] == 1]

    os.makedirs("outputs/tables", exist_ok=True)
    anomalies.to_csv("outputs/tables/anomalies.csv", index=False)

    print(f"✅ Anomalies detected: {len(anomalies)}")
    return df

