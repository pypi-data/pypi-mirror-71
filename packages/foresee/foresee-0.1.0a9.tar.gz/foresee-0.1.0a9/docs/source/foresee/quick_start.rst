===========
Quick Start
===========

Install foresee
===============

*foresee* is hosted on PyPI and can be installed with pip.

.. code-block:: shell
	
	$ pip install foresee
	
.. _single-time-series:
	
Example 1: one time series as a single column dataframe
=======================================================

.. code-block:: python

	import warnings
	warnings.filterwarnings("ignore")


	import pandas as pd
	import numpy as np
	from io import StringIO
	import importlib_resources

	# import collect_result for handling the process
	from foresee.scripts.main import collect_result

	# 'basic_time_series_data.csv' file has only one column containing time series values
	basic_time_series_data_txt = importlib_resources.files('foresee.data').joinpath('basic_time_series_data.csv').read_text()

	ts_df = pd.read_csv(StringIO(basic_time_series_data_txt))
	ts_df.head()

	# present data here

	# user defind parameters

	# if input dataframe has more than one column, provide column name containing time series data

	endog_colname = None

	if len(ts_df.columns) > 1 and endog_colname is None:
		raise ValueError('time series column name is required!!!')
		
	# if uploading your own sample data, update the following parameters if needed

	freq = 5
	fcst_length = 10
	model_list = ['ewm_model', 'fft', 'holt_winters', 'prophet', 'sarimax']

	'''
	avilable run types:  'all_models', 'best_model', 'all_best'
	
	all_models: no holdout, no tuning, no model competition. return results for all models
	
	best_model: compare models forecast accuracy and return the result of the best model
	
	all_best: compute forecast accuracy for all models and return the result for all models
	
	'''

	run_type = 'all_models'

	# if comparing models results, holdout length is required

	if run_type == 'all_models':
		holdout_length = None
	else:
		holdout_length = 20


	# we are working with one time series and no date-time column so time series id and date-time column name are set to None.
	gbkey = None
	ds_column = None
	tune = False


	# we are fitting one time series in this example so no need to parallelize.

	fit_execution_method = 'non_parallel'


	'''
	result:  dataframe containing fitted values and future forecasts
	fit_results_list:  list of dictionaries containing fitted values, forecasts, and errors (useful for debuging)
	'''

	result, fit_result_list = collect_result(
		ts_df.copy(),
		endog_colname,
		gbkey,
		ds_column, 
		freq, 
		fcst_length, 
		run_type, 
		holdout_length, 
		model_list,
		fit_execution_method,
		tune
	)

	result.head()
	# present data here

.. _many-time-series:

Example 2: multiple time series as a dataframe with a time series id column
===========================================================================

.. code-block:: python

	import warnings
	warnings.filterwarnings("ignore")

	import pandas as pd
	import numpy as np
	from io import StringIO
	import importlib_resources

	# import main from foresee.scripts
	from foresee.scripts import main	
	# upload sample time-series dataframe with columns(id, date_stamp, y)

	test_data_light_txt = importlib_resources.files('foresee.data').joinpath('test_data_light.csv').read_text()

	ts_df = pd.read_csv(StringIO(test_data_light_txt))


	ts_df['date_stamp'] = pd.to_datetime(ts_df['date_stamp'])
	ts_df.head()
	
	# user defind parameters

	# time series values column name: required if input dataframe has more than one column

	endog_colname = 'y'

	if len(ts_df.columns) > 1 and endog_colname is None:
		raise ValueError('time series column name is required!!!')

	# time series frequency
	freq = 5

	# out of sample forecast length
	fcst_length = 10

	# available forecasting models
	model_list = ['ewm_model', 'fft', 'holt_winters', 'prophet', 'sarimax']

	# avilable run types: 'best_model', 'all_best', 'all_models'
	run_type = 'all_best'

	# if comparing models (run_type in 'best_model' or 'all_best') then holdout length is required

	if run_type == 'all_models':
		holdout_length = None
	else:
		holdout_length = 20
		
	# fit-forecast computations can be done in parallel for each time series. requires dask library!!!
	# for sequential processing set fit_execution_method to 'non_parallel'

	fit_execution_method = 'parallel'


	# since we have two time series in this dataset, time series id column name and date-time column name are required.
	gbkey = 'id'
	ds_column = 'date_stamp'
	tune = True

	'''
	result:  dataframe containing fitted values and future forecasts
	fit_results_list:  list of dictionaries containing fitted values, forecasts, and errors (useful for debuging)
	'''

	result, fit_result_list = main.collect_result(
			ts_df.copy(),
			endog_colname,
			gbkey,
			ds_column, 
			freq, 
			fcst_length, 
			run_type, 
			holdout_length, 
			model_list,
			fit_execution_method,
			tune
	)

	result.head()


.. _drop-file-forecast:

Example 3: run forecasts with UI app
====================================

This simple UI accepts *csv* file for input data and has check lists to set neccessary
parameters. Application runs at this url: http://localhost:8050/dash

Excecute the following block of code then navigate to above URL, fill out time series information,
and drop your file to be processed. Results will be returned as a table and can be downloaded.

.. code-block:: python

	import flask
	import dash

	server = flask.Flask(__name__)

	@server.route('/')
	def index():
		return 'Flask root.'

	from foresee.webapp.dash_app import app

	if __name__ == '__main__':
		app.run_server()








