# Install required packages if not already installed
# install.packages(c("forecast", "tseries", "imputeTS"))

# Load libraries
library(forecast)
library(tseries)
library(imputeTS)

# 1. Check whether the given dataset is Time Series dataset or not
data("USAccDeaths")
str(USAccDeaths)  # ts object, monthly
print("Dataset: USAccDeaths - Monthly accidental deaths (1973-1978), time series confirmed.")
plot(USAccDeaths, main = "US Accidental Deaths Time Series", ylab = "Deaths")

# 2. Perform Exploratory Data Analysis (EDA)
summary(USAccDeaths)

# Plot
plot(USAccDeaths, main = "US Accidental Deaths Time Series", ylab = "Deaths")

# Decomposition
decomp <- decompose(USAccDeaths, type = "additive")
plot(decomp)

# 3. Perform Data Preprocessing
# Check for missing values
sum(is.na(USAccDeaths))  # 0

# Log transformation
log_ts <- log(USAccDeaths)
plot(log_ts, main = "Log-Transformed USAccDeaths")

# Differencing
diff_ts <- diff(log_ts, differences = 1)
plot(diff_ts, main = "First Difference of Log-Transformed USAccDeaths")

# 4. Check for Stationarity using ADF Test and KPSS Test
# Original
adf_original <- adf.test(USAccDeaths)
print(adf_original)  # Non-stationary
kpss_original <- kpss.test(USAccDeaths)
print(kpss_original)

# Differenced
adf_diff <- adf.test(diff_ts)
print(adf_diff)  # Stationary
kpss_diff <- kpss.test(diff_ts)
print(kpss_diff)

# 5. Apply Holt-Winters Model and Plot
# Holt-Winters (additive)
hw_model <- HoltWinters(USAccDeaths, seasonal = "additive")
plot(hw_model, main = "Holt-Winters Fit: USAccDeaths")
summary(hw_model)

# 6. Apply AR Model and MA Model and Plot
# AR(1)
ar_model <- arima(diff_ts, order = c(1, 0, 0))
summary(ar_model)
plot(ar_model)

# MA(1)
ma_model <- arima(diff_ts, order = c(0, 0, 1))
summary(ma_model)
plot(ma_model)

# ACF/PACF
acf(diff_ts, main = "ACF: Differenced USAccDeaths")
pacf(diff_ts, main = "PACF: Differenced USAccDeaths")

# 7. Finally Forecast
# Holt-Winters Forecast
hw_forecast <- forecast(hw_model, h = 12)
plot(hw_forecast, main = "Holt-Winters Forecast: USAccDeaths")

# AR Forecast
ar_forecast <- forecast(ar_model, h = 12)
plot(ar_forecast, main = "AR Forecast: Differenced USAccDeaths")

# MA Forecast
ma_forecast <- forecast(ma_model, h = 12)
plot(ma_forecast, main = "MA Forecast: Differenced USAccDeaths")

# Print forecast
print(hw_forecast)

