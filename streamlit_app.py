import pandas as pd
import streamlit as st
from statsmodels.tsa.stattools import adfuller, kpss
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.arima.model import ARIMA
import plotly.graph_objects as go

@st.cache_data
def load_data():
    df = pd.read_csv("data/delhi_daily.csv", parse_dates=["date"])
    df = df.set_index("date").asfreq("D")
    df["meantemp"] = df["meantemp"].interpolate()
    return df

def arima_forecast(series, steps=30):
    model = ARIMA(series, order=(2, 1, 2)).fit()
    return model.forecast(steps=steps)

df = load_data()
st.sidebar.title("Weather Dashboard Controls")
date_range = st.sidebar.date_input("Select Date Range", [df.index.min(), df.index.max()])
st.title("Delhi Weather Time Series Analysis")

filtered = df[date_range[0]:date_range[1]]["meantemp"]

adf_stat, adf_p, *_ = adfuller(filtered)
kpss_stat, kpss_p, *_ = kpss(filtered, nlags="auto")

st.subheader("📊 Stationarity Tests")
st.write(f"ADF p-value: {adf_p:.4f}")
st.write(f"KPSS p-value: {kpss_p:.4f}")
st.caption("Stationary if ADF p < 0.05 and KPSS p > 0.05")

st.subheader("🔍 STL Decomposition")
stl = STL(filtered, period=30).fit()
fig_decomp = go.Figure([
    go.Scatter(x=stl.trend.index, y=stl.trend, name="Trend"),
    go.Scatter(x=stl.seasonal.index, y=stl.seasonal, name="Seasonal"),
    go.Scatter(x=stl.resid.index, y=stl.resid, name="Residual"),
])
st.plotly_chart(fig_decomp, use_container_width=True)

st.subheader("🔮 ARIMA Forecast (Next 30 Days)")
train = filtered[:-30]
forecast = arima_forecast(train)
future_dates = pd.date_range(filtered.index[-1] + pd.Timedelta(days=1), periods=30)
fig_forecast = go.Figure([
    go.Scatter(x=filtered.index, y=filtered, name="Observed"),
    go.Scatter(x=future_dates, y=forecast, name="Forecast"),
])
st.plotly_chart(fig_forecast, use_container_width=True)

st.markdown("---")
st.caption("Built with Streamlit | Data Source: Delhi Daily Climate")