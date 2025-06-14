

# Dynamic Weather Time Series Dashboard

## Overview

This **Dynamic Weather Time Series Dashboard** is a Streamlit application designed for comprehensive analysis and forecasting of daily mean temperatures. It allows users to visualize historical weather patterns, decompose time series data into its underlying components (trend, seasonality, residuals), perform stationarity tests, and predict future temperatures using powerful forecasting models like ARIMA and Prophet. Whether you're a data analyst, climate enthusiast, or simply curious about local weather trends, this dashboard provides an interactive and insightful platform.

-----

## Features

  * **Flexible Data Input:**
      * **Live Data Fetching:** Retrieve historical daily mean temperature data for any city using the OpenWeatherMap API.
      * **CSV Upload:** Upload your own CSV files containing 'date' and 'meantemp' columns for custom analysis.
  * **Interactive Visualizations:**
      * **Daily Mean Temperature Plot:** A clear line chart showing temperature trends over time.
  * **Advanced Time Series Analysis:**
      * **STL Decomposition:** Decompose temperature series into its trend, seasonal (weekly), and residual components to reveal hidden patterns and anomalies.
      * **Stationarity Tests:** Automated Augmented Dickey-Fuller (ADF) and KPSS tests to assess the statistical properties of the time series, crucial for model selection.
  * **Future Temperature Forecasting:**
      * Predict 7-day future temperatures using either the **ARIMA** (AutoRegressive Integrated Moving Average) or **Prophet** models.
      * Visualize forecasts alongside historical data for easy interpretation of upcoming temperature phases.
  * **User-Friendly Interface:** Built with Streamlit for an intuitive and interactive experience.

-----

## How It Works

The dashboard leverages the following key components and libraries:

  * **Streamlit:** For building the interactive web application.
  * **OpenWeatherMap API:** To fetch live historical weather data.
  * **Pandas & NumPy:** For efficient data manipulation and numerical operations.
  * **Plotly Express:** For creating dynamic and interactive visualizations.
  * **Statsmodels:** For classical time series analysis tools like STL decomposition, ADF, and KPSS tests, and the ARIMA model.
  * **Prophet (from Facebook):** A robust forecasting library designed for business time series data with strong seasonal effects.

-----

## Setup and Installation

Follow these steps to get the dashboard up and running on your local machine:

1.  **Clone the Repository:**

    ```bash
    git clone <https://github.com/rhythmgarg2606/weather-ts-dashboard>
    cd upgraded_weather_ts_dashboard
    ```

2.  **Create a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    *(If you don't have a `requirements.txt` file, you can create one by running `pip freeze > requirements.txt` after installing all the libraries mentioned in the `streamlit_app.py`'s import section: `streamlit`, `pandas`, `numpy`, `plotly`, `requests`, `statsmodels`, `prophet`)*.

4.  **Get an OpenWeatherMap API Key:**

      * Go to [OpenWeatherMap](https://openweathermap.org/api).
      * Sign up for a free account.
      * Navigate to the "API keys" tab in your profile to find your API key.

5.  **Update API Key in `streamlit_app.py`:**
    Open `streamlit_app.py` and replace `"c8927830ce51b245ec501a644440ed61"` with your actual API key:

    ```python
    API_KEY = "YOUR_OPENWEATHERMAP_API_KEY" # Replace with your key
    ```

-----

## Usage

To run the Streamlit dashboard:

1.  **Navigate to the project directory** (where `streamlit_app.py` is located) in your terminal or command prompt.
2.  **Execute the Streamlit command:**
    ```bash
    streamlit run streamlit_app.py
    ```
3.  Your web browser will automatically open a new tab displaying the dashboard (usually at `http://localhost:8501`).

### Interacting with the Dashboard:

  * **Enter City:** Type a city name in the sidebar to fetch live historical weather data.
  * **Use Live Weather Data:** Toggle this checkbox to switch between live API data and uploaded CSV data.
  * **Days of History:** Use the slider to select how many past days of live data to retrieve (7-30 days).
  * **Upload CSV:** Click the "Browse files" button to upload your own CSV file. Ensure it has columns named 'date' and 'meantemp'.
  * **Forecast Model:** Choose between 'ARIMA' and 'Prophet' for your temperature predictions.
  * **Run Forecast:** Click this button to generate and display the 7-day temperature forecast.

-----

## Code Structure

The project primarily consists of `streamlit_app.py` which contains:

  * **Imports and Settings:** Essential library imports and API key configuration.
  * **Helper Functions:**
      * `get_historical_weather()`: Handles API calls to OpenWeatherMap.
      * `stationarity_tests()`: Performs ADF and KPSS tests.
      * `stl_decomposition()`: Implements Seasonal-Trend decomposition.
      * `arima_forecast()`: Generates forecasts using the ARIMA model.
      * `prophet_forecast()`: Generates forecasts using the Prophet model.
  * **Sidebar Controls Logic:** Defines the UI elements in the sidebar and manages data loading based on user input.
  * **Main Dashboard Display Logic:** Renders the charts (Daily Mean Temperature, STL Decomposition, Forecast) and statistical test results based on the processed data.

-----

## Contributing

Feel free to fork this repository, open issues, or submit pull requests. Contributions are welcome\!

-----
