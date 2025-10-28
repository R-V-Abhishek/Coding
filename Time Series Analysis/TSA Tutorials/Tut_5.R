# Install required packages if not already installed
# install.packages(c("forecast", "tseries", "imputeTS"))

# Load libraries
library(forecast)
library(tseries)
library(imputeTS)

# 1. Check whether the given dataset is Time Series dataset or not
data("sunspots")
str(sunspots)  # ts object, monthly
print("Dataset: sunspots - Monthly sunspots (1749-1983), time series confirmed.")
plot(sunspots, main = "Monthly Sunspots Time Series", ylab = "Sunspot Count")

# 2. Perform Exploratory Data Analysis (EDA)
summary(sunspots)

# Plot
plot(sunspots, main = "Monthly Sunspots Time Series", ylab = "Sunspot Count")

# Decomposition (solar cycle ~11 years = 132 months)
decomp <- decompose(sunspots, type = "additive")
plot(decomp)

# 3. Perform Data Preprocessing
# Check for missing values
sum(is.na(sunspots))  # 0

# Log transformation
log_ts <- log(sunspots + 1)  # +1 for log(0)
plot(log_ts, main = "Log-Transformed Sunspots")

# Differencing
diff_ts <- diff(log_ts, differences = 1)
plot(diff_ts, main = "First Difference of Log-Transformed Sunspots")

# 4. Check for Stationarity using ADF Test and KPSS Test
# Original
adf_original <- adf.test(sunspots)
print(adf_original)  # Non-stationary
kpss_original <- kpss.test(sunspots)
print(kpss_original)

# Differenced
adf_diff <- adf.test(diff_ts)
print(adf_diff)  # Stationary
kpss_diff <- kpss.test(diff_ts)
print(kpss_diff)

# 5. Apply Holt-Winters Model and Plot
# Holt-Winters (additive)
sunspots_ts <- ts(sunspots, frequency = 132)
hw_model <- HoltWinters(sunspots_ts, seasonal = "additive")
plot(hw_model, main = "Holt-Winters Fit: Sunspots")
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
acf(diff_ts, main = "ACF: Differenced Sunspots")
pacf(diff_ts, main = "PACF: Differenced Sunspots")

# 7. Finally Forecast
# Holt-Winters Forecast
hw_forecast <- forecast(hw_model, h = 132)
plot(hw_forecast, main = "Holt-Winters Forecast: Sunspots")

# AR Forecast
ar_forecast <- forecast(ar_model, h = 132)
plot(ar_forecast, main = "AR Forecast: Differenced Sunspots")

# MA Forecast
ma_forecast <- forecast(ma_model, h = 132)
plot(ma_forecast, main = "MA Forecast: Differenced Sunspots")

# Print forecast
print(hw_forecast)

