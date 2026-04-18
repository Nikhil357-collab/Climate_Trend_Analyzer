import matplotlib.pyplot as plt
import seaborn as sns
import os

def perform_eda(df):
    os.makedirs("outputs/figures", exist_ok=True)

    # Temperature Trend
    plt.figure()
    plt.plot(df['date'], df['temperature'])
    plt.title("Temperature Trend")
    plt.savefig("outputs/figures/temp_trend.png")
    plt.close()

    # Rainfall
    plt.figure()
    plt.plot(df['date'], df['rainfall'])
    plt.title("Rainfall Trend")
    plt.savefig("outputs/figures/rainfall.png")
    plt.close()

    # Correlation Heatmap
    plt.figure()
    sns.heatmap(df[['temperature','rainfall','humidity']].corr(), annot=True)
    plt.savefig("outputs/figures/correlation.png")
    plt.close()

    print("✅ EDA completed!")