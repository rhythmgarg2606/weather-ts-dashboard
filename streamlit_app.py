# upgraded_weather_ts_dashboard/streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
from datetime import datetime, timedelta
import io
import os

st.set_page_config(page_title="Dynamic Weather Time Series Dashboard", layout="wide")

# ------------------ SETTINGS ------------------
API_KEY = "c8927830ce51b245ec501a644440ed61"  # Replace with your key
BASE_URL = "http://api.openweathermap.org/data/2.5/onecall/timemachine"

# ------------------ HELPER FUNCTIONS ------------------
def get_historical_weather(city: str, days: int = 7):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
    geo_resp = requests.get(geo_url).json()
    if not geo_resp:
        st.error("City not found.")
        return None
    lat = geo_resp[0]['lat']
    lon = geo_resp[0]['lon']

    records = []
    for i in range(days):
        dt = int((datetime.utcnow() - timedelta(days=i+1)).timestamp())
        url = f"{BASE_URL}?lat={lat}&lon={lon}&dt={dt}&appid={API_KEY}&units=metric"
        resp = requests.get(url).json()
        if "hourly" in resp:
            temp = np.mean([h['temp'] for h in resp['hourly']])
            records.append({'date': datetime.utcfromtimestamp(dt).date(), 'meantemp': temp})

    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    df = df.asfreq('D')
    return df.sort_index()

def stationarity_tests(series):
    adf_stat, adf_p, *_ = adfuller(series.dropna())
    kpss_stat, kpss_p, *_ = kpss(series.dropna(), nlags='auto')
    return adf_p, kpss_p

def stl_decomposition(series):
    return STL(series.dropna(), period=7).fit()

def arima_forecast(series, steps=7):
    cleaned_series = series.interpolate().fillna(method='bfill').fillna(method='ffill').dropna()
    if len(cleaned_series) < 10:
        st.error("Not enough data points for ARIMA. Try uploading a longer time series.")
        return pd.Series()

    try:
        model = ARIMA(cleaned_series, order=(2, 1, 2))
        fit = model.fit()
        return fit.forecast(steps=steps)
    except Exception as e:
        st.error(f"ARIMA model failed: {e}")
        return pd.Series()

def prophet_forecast(df, steps=7):
    prophet_df = df.reset_index().rename(columns={"date": "ds", "meantemp": "y"})
    m = Prophet()
    m.fit(prophet_df)
    future = m.make_future_dataframe(periods=steps)
    forecast = m.predict(future)
    return forecast[['ds', 'yhat']].set_index('ds')

# ------------------ SIDEBAR ------------------
st.sidebar.title("Controls")
city = st.sidebar.text_input("Enter City for Live Weather", "Delhi")
use_live = st.sidebar.checkbox("Use Live Weather Data", value=True)
days = st.sidebar.slider("Days of History", 7, 30, 14)
uploaded_file = st.sidebar.file_uploader("Or Upload CSV (with 'date', 'meantemp')")
model_choice = st.sidebar.selectbox("Forecast Model", ["ARIMA", "Prophet"])
x_axis = st.sidebar.selectbox("X-Axis for Plot", ["date"])
y_axis = st.sidebar.selectbox("Y-Axis for Plot", ["meantemp"])

data = None
data_source = ""
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if 'date' not in df.columns:
        df['date'] = pd.date_range(end=pd.Timestamp.today(), periods=len(df), freq='D')
    else:
        df['date'] = pd.to_datetime(df['date'])

    df = df[['date', 'meantemp']].dropna()
    df = df.set_index('date').asfreq('D')
    data_source = "Uploaded CSV"
    data = df
elif use_live:
    data = get_historical_weather(city, days)
    data_source = f"Live Data for {city}"
else:
    st.warning("Please either upload a CSV file or enable live weather data.")
    st.stop()

if data is not None and not data.empty:
    st.title("📊 Dynamic Weather Time Series Dashboard")
    st.subheader(data_source)
    data['meantemp'] = data['meantemp'].interpolate().fillna(method='bfill').fillna(method='ffill')

    fig_line = px.line(data, x=data.index, y='meantemp', title="Daily Mean Temperature")
    st.plotly_chart(fig_line, use_container_width=True)
    st.caption("**Insight:** This line chart shows the average daily temperature over the selected time period, highlighting overall warming or cooling trends.")

    st.markdown("### 🔍 STL Decomposition")
    stl = stl_decomposition(data['meantemp'])
    fig_stl = px.line(
        pd.DataFrame({
            'Trend': stl.trend,
            'Seasonal': stl.seasonal,
            'Residual': stl.resid
        }),
        facet_col=1, height=600
    )
    st.plotly_chart(fig_stl, use_container_width=True)
    st.caption("**Insight:** STL decomposition separates the temperature time series into its trend, seasonal variation, and random noise, helping understand underlying behaviors.")

    st.markdown("### 🧪 Stationarity Test Results")
    adf_p, kpss_p = stationarity_tests(data['meantemp'])
    st.info(f"ADF p-value: {adf_p:.4f} | KPSS p-value: {kpss_p:.4f}")
    if adf_p < 0.05 and kpss_p > 0.05:
        st.success("The series appears to be stationary based on ADF and KPSS tests.")
    else:
        st.warning("The series may be non-stationary. Consider differencing or detrending.")

    st.markdown("### 🔮 Forecasting")
    if st.button("Run Forecast"):
        if model_choice == "ARIMA":
            forecast = arima_forecast(data['meantemp'], steps=7)
            if not forecast.empty:
                future_dates = pd.date_range(data.index[-1] + pd.Timedelta(days=1), periods=7)
                forecast_df = pd.DataFrame({'Forecast': forecast}, index=future_dates)
        else:
            forecast_df = prophet_forecast(data, steps=7)

        full_df = pd.concat([data['meantemp'], forecast_df['Forecast' if model_choice == 'ARIMA' else 'yhat']])
        fig_forecast = px.line(full_df, title="7-Day Forecast", labels={'value': 'Temperature'})
        st.plotly_chart(fig_forecast, use_container_width=True)
        st.caption("**Insight:** This forecast uses {} model to predict temperature trends. It helps identify whether the city is entering a warming, cooling, or stable phase.".format(model_choice))
else:
    st.warning("No data loaded yet. Check your input.")
