#Air Passengers is an inbuilt dataset in R
data("AirPassengers")
ts_data <- AirPassengers


#Apply decomposition using decompose()
decomp <- decompose(ts_data, type = "multiplicative")

plot(decomp)


#STL is based on LOESS (Locally Estimated Scatterplot Smoothing)
stl_decomp <- stl(ts_data, s.window = "periodic")
plot(stl_decomp)

data <- ts(rnorm(100), start = c(2020,1), frequency = 12)
plot(data)

#line, bar, histogram, box plots. plot syntax changes
