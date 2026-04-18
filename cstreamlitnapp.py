import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import zscore

st.set_page_config(page_title="Climate Trend Analyzer", layout="wide")

st.title("🌍 Climate Trend Analyzer Dashboard")

# ==============================
# 📂 FILE UPLOAD
# ==============================
uploaded_file = st.file_uploader("📂 Upload Climate CSV", type=["csv"])

@st.cache_data
def load_default():
    return pd.read_csv("data/processed/cleaned_data.csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Uploaded dataset loaded")
else:
    df = load_default()
    st.info("Using default dataset")

# ==============================
# 🧹 BASIC CLEANING
# ==============================
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])
df = df.sort_values("date")

# ==============================
# 🎛️ SIDEBAR CONTROLS (SLICERS)
# ==============================
st.sidebar.header("🔧 Filters")

# Date range
start_date = st.sidebar.date_input("Start Date", df['date'].min())
end_date = st.sidebar.date_input("End Date", df['date'].max())

df = df[(df['date'] >= pd.to_datetime(start_date)) &
        (df['date'] <= pd.to_datetime(end_date))]

# Variable selection
variable = st.sidebar.selectbox("Select Variable", ["temperature", "rainfall", "humidity"])

# ==============================
# 🚨 ALERT SETTINGS
# ==============================
st.sidebar.header("🚨 Alerts")

temp_threshold = st.sidebar.slider("Temperature Alert Threshold (°C)", 30, 60, 40)

# ==============================
# 📊 MAIN VISUALIZATION
# ==============================
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"{variable.capitalize()} Trend")
    fig = px.line(df, x='date', y=variable, title=f"{variable.capitalize()} Over Time")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Temperature Moving Average")
    df['temp_ma'] = df['temperature'].rolling(30).mean()
    fig2 = px.line(df, x='date', y='temp_ma', title="30-Day Moving Average")
    st.plotly_chart(fig2, use_container_width=True)

# ==============================
# 🚨 TEMPERATURE ALERT
# ==============================
high_temp = df[df['temperature'] > temp_threshold]

st.subheader("🚨 Temperature Alerts")

if not high_temp.empty:
    st.error(f"⚠️ {len(high_temp)} High Temperature Events Detected!")
    st.dataframe(high_temp[['date', 'temperature']].tail(10))
else:
    st.success("✅ No extreme temperature events")

# ==============================
# 🚨 ANOMALY DETECTION
# ==============================
df['z_score'] = zscore(df['temperature'])
df['anomaly'] = df['z_score'].apply(lambda x: 1 if abs(x) > 3 else 0)

anomalies = df[df['anomaly'] == 1]

st.subheader("⚠️ Anomaly Detection")

if not anomalies.empty:
    st.warning(f"{len(anomalies)} anomalies detected")
    
    fig3 = px.scatter(df, x='date', y='temperature',
                      color=df['anomaly'].map({0:'Normal',1:'Anomaly'}),
                      title="Anomaly Detection")
    st.plotly_chart(fig3, use_container_width=True)

    st.dataframe(anomalies[['date','temperature','z_score']].tail(10))
else:
    st.success("No anomalies detected")

# ==============================
# 📊 SUMMARY METRICS
# ==============================
st.subheader("📊 Summary")

col3, col4, col5 = st.columns(3)

col3.metric("Avg Temp", round(df['temperature'].mean(),2))
col4.metric("Max Temp", round(df['temperature'].max(),2))
col5.metric("Total Anomalies", int(df['anomaly'].sum()))

# ==============================
# 📥 DOWNLOAD OUTPUT
# ==============================
st.subheader("📥 Download Results")

csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Processed Data",
    data=csv,
    file_name='processed_climate_data.csv',
    mime='text/csv',
)