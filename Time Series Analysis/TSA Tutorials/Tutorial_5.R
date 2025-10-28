# Install required packages if not already installed
# install.packages(c("forecast", "tseries", "imputeTS"))

# Load libraries
library(forecast)  # For Holt-Winters, forecasting
library(tseries)   # For ADF and KPSS tests
library(imputeTS)  # For handling missing values

# 1. Check whether the given dataset is Time Series dataset or not
data("lynx")
str(lynx)  # ts object, frequency = 1 (annual)
print("Dataset: lynx - Annual lynx trappings (1821-1934), time series confirmed.")
plot(lynx, main = "Lynx Trapping Time Series", ylab = "Number of Lynx")

# 2. Perform Exploratory Data Analysis (EDA)
summary(lynx)

# Plot
plot(lynx, main = "Lynx Trapping Time Series", ylab = "Number of Lynx")

# Decomposition using STL (since lynx has cycles ~10 years, not strict seasonality)
# Convert to ts with frequency 10 for STL
lynx_ts <- ts(lynx, frequency = 10)
decomp <- stl(lynx_ts, s.window = "periodic")
plot(decomp, main = "STL Decomposition: Lynx")

# 3. Perform Data Preprocessing
# Check for missing values
sum(is.na(lynx))  # 0

# Log transformation for variance stabilization
log_ts <- log(lynx)
plot(log_ts, main = "Log-Transformed Lynx Series")

# Differencing
diff_ts <- diff(log_ts, differences = 1)
plot(diff_ts, main = "First Difference of Log-Transformed Lynx")

# 4. Check for Stationarity using ADF Test and KPSS Test
# Original
adf_original <- adf.test(lynx)
print(adf_original)  # Non-stationary expected
kpss_original <- kpss.test(lynx)
print(kpss_original)

# Differenced
adf_diff <- adf.test(diff_ts)
print(adf_diff)  # Stationary
kpss_diff <- kpss.test(diff_ts)
print(kpss_diff)

# 5. Apply Holt-Winters Model and Plot
# Holt-Winters (multiplicative, due to varying amplitude)
hw_model <- HoltWinters(lynx_ts, seasonal = "multiplicative")
plot(hw_model, main = "Holt-Winters Fit: Lynx")
summary(hw_model)

# 6. Apply AR Model and MA Model and Plot
# AR(1) on differenced
ar_model <- arima(diff_ts, order = c(1, 0, 0))
summary(ar_model)
plot(ar_model)

# MA(1)
ma_model <- arima(diff_ts, order = c(0, 0, 1))
summary(ma_model)
plot(ma_model)

# ACF/PACF
acf(diff_ts, main = "ACF: Differenced Lynx")
pacf(diff_ts, main = "PACF: Differenced Lynx")

# 7. Finally Forecast
# Holt-Winters Forecast
hw_forecast <- forecast(hw_model, h = 10)
plot(hw_forecast, main = "Holt-Winters Forecast: Lynx")

# AR Forecast
ar_forecast <- forecast(ar_model, h = 10)
plot(ar_forecast, main = "AR Forecast: Differenced Lynx")

# MA Forecast
ma_forecast <- forecast(ma_model, h = 10)
plot(ma_forecast, main = "MA Forecast: Differenced Lynx")

# Print forecast
print(hw_forecast)

