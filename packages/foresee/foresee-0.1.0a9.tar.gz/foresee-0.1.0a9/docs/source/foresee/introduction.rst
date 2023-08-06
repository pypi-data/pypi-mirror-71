=============
Introduction
=============

There are several open source python packages with models for time series forecasting.
The goal of this project is to generate forecasts using some of these models,
compare their results in a holdout period, and report the outcome.
There is also functionality for model hyper-parameter tuning across pre-selected
parameters and space using hyperopt library.
Forecasting and tuning process can run in parallel using dask library, if needed,
to speed up the operation.

This library has a basic web application created using plotly-dash which can accept
csv file, for input data, and some parameters using drop downs and check lists. Forecast
results is then displayed as a table and can be downloaded.

Currently there are five different forecasting models available. These will generate
forecasts using their default parameters if tuning is not selected but with tuning a
pre-selected set of their parameters will be tuned over a pre-defind space by comparing
forecast accuracy over a holdout period.

1) EWM: Exponentially Weighted Mean
2) FFT: Fast Fourier Transformation
3) Holt-Winters: Holt Winters exponential smoothing model from statsmodels library
4) Prophet: Prophet model from fbprophet library
5) SARIMAX: Sarimax model from statsmodels library


TODO:
=====
* add new models
* design user control over parameters and parameter space
* include other loss functions like *mse*
* ...





