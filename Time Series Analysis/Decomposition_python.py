import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose, STL
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf


# Function to identify and plot time series
def identify_time_series(ts, title):
    print(f"\n--- Identifying Time Series: {title} ---")
    print("First few observations:")
    print(ts.head())
    print("\nData Type:", type(ts))
    print("Index Type:", type(ts.index))
    print("Inferred Frequency:", pd.infer_freq(ts.index))
    print("Basic Stats:")
    print(ts.describe())

    # Plot the series
    plt.figure(figsize=(12, 6))
    plt.plot(ts)
    plt.title(f"Time Series Plot: {title}")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.grid(True)
    plt.show()


# Function for classical decomposition
def classical_decompose(ts, model='additive', period=None):
    try:
        decomp = seasonal_decompose(ts, model=model, period=period)
        fig = decomp.plot()
        fig.suptitle(f"Classical Decomposition ({model.capitalize()})")
        plt.show()
        return decomp
    except ValueError as e:
        print(f"Error in classical decomposition: {e}")
        return None


# Function for STL decomposition
def stl_decompose(ts, period, seasonal_window=7):
    try:
        stl = STL(ts, period=period, seasonal=seasonal_window)
        res = stl.fit()
        fig = res.plot()
        fig.suptitle("STL Decomposition")
        plt.show()
        return res
    except ValueError as e:
        print(f"Error in STL decomposition: {e}")
        return None


# Function for ACF and PACF plots
def plot_acf_pacf(ts, title, lags=40):
    plt.figure(figsize=(12, 6))
    plt.subplot(211)
    plot_acf(ts, lags=lags, ax=plt.gca(), title=f"ACF: {title}")
    plt.subplot(212)
    plot_pacf(ts, lags=lags, ax=plt.gca(), title=f"PACF: {title}")
    plt.tight_layout()
    plt.show()


# Example 1: Monthly Data (Synthetic: Monthly Sales with Yearly Seasonality)
# Generate synthetic monthly data: Trend + Yearly Seasonality + Noise
np.random.seed(123)
date_rng_monthly = pd.date_range(start='2015-01-01', end='2024-12-31', freq='M')
n_months = len(date_rng_monthly)
trend = np.linspace(200, 500, n_months)  # Linear growth
seasonal_yearly = 50 * np.sin(2 * np.pi * np.arange(n_months) / 12)  # Yearly cycle
noise = np.random.normal(0, 10, n_months)  # Random noise
ts_monthly = pd.Series(trend + seasonal_yearly + noise, index=date_rng_monthly)
ts_monthly = ts_monthly.asfreq('M')

# Clean data
ts_monthly = ts_monthly.dropna()
ts_monthly = ts_monthly[ts_monthly.apply(lambda x: isinstance(x, (int, float)) and not pd.isna(x))]

identify_time_series(ts_monthly, "Monthly Sales (Synthetic)")
print("\nDecomposing Monthly Data...")
classical_decompose(ts_monthly, model='additive', period=12)  # Additive for simplicity
stl_decompose(ts_monthly, period=12, seasonal_window=13)
print("\nACF and PACF for Monthly Data...")
plot_acf_pacf(ts_monthly, "Monthly Sales (Synthetic)", lags=24)

# Example 2: Daily Data (Synthetic: Daily Website Visits with Weekly Seasonality)
# Generate synthetic daily data: Trend + Weekly Seasonality + Noise
date_rng_daily = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
n_days = len(date_rng_daily)
trend = np.linspace(100, 300, n_days)  # Upward trend
seasonal_weekly = 30 * np.sin(2 * np.pi * np.arange(n_days) / 7)  # Weekly cycle (e.g., weekend dips)
noise = np.random.normal(0, 8, n_days)
ts_daily = pd.Series(trend + seasonal_weekly + noise, index=date_rng_daily)
ts_daily = ts_daily.asfreq('D')

# Clean data
ts_daily = ts_daily.dropna()
ts_daily = ts_daily[ts_daily.apply(lambda x: isinstance(x, (int, float)) and not pd.isna(x))]

identify_time_series(ts_daily, "Daily Website Visits (Synthetic)")
print("\nDecomposing Daily Data...")
classical_decompose(ts_daily, model='additive', period=7)
stl_decompose(ts_daily, period=7, seasonal_window=15)
print("\nACF and PACF for Daily Data...")
plot_acf_pacf(ts_daily, "Daily Website Visits (Synthetic)", lags=28)

# Example 3: Hourly Data (Synthetic: Hourly Server Load with Daily Seasonality)
# Generate synthetic hourly data: Trend + Daily Seasonality + Noise
date_rng_hourly = pd.date_range(start='2023-01-01 00:00', end='2023-01-31 23:00', freq='H')
n_hours = len(date_rng_hourly)
trend = np.linspace(50, 150, n_hours)  # Gradual increase
seasonal_daily = 40 * np.sin(2 * np.pi * np.arange(n_hours) / 24)  # Daily cycle (e.g., peak usage in day)
noise = np.random.normal(0, 12, n_hours)
ts_hourly = pd.Series(trend + seasonal_daily + noise, index=date_rng_hourly)
ts_hourly = ts_hourly.asfreq('H')

# Clean data
ts_hourly = ts_hourly.dropna()
ts_hourly = ts_hourly[ts_hourly.apply(lambda x: isinstance(x, (int, float)) and not pd.isna(x))]

identify_time_series(ts_hourly, "Hourly Server Load (Synthetic)")
print("\nDecomposing Hourly Data...")
classical_decompose(ts_hourly, model='additive', period=24)
stl_decompose(ts_hourly, period=24, seasonal_window=25)
print("\nACF and PACF for Hourly Data...")
plot_acf_pacf(ts_hourly, "Hourly Server Load (Synthetic)", lags=48)

print("\nScript Execution Complete. Review plots and outputs for identification, decomposition, and correlation insights.")