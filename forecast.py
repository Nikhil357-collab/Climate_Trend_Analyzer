from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import os

def forecast(df):
    model = ARIMA(df['temperature'], order=(5,1,0))
    model_fit = model.fit()

    forecast = model_fit.forecast(steps=30)

    os.makedirs("outputs/figures", exist_ok=True)

    plt.figure()
    plt.plot(df['temperature'], label='History')
    plt.plot(range(len(df), len(df)+30), forecast, label='Forecast')
    plt.legend()
    plt.title("Temperature Forecast")
    plt.savefig("outputs/figures/forecast.png")
    plt.close()

    print("✅ Forecast generated!")