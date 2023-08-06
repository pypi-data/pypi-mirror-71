.. foresee documentation master file, created by
   sphinx-quickstart on Tue May 19 20:45:46 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

foresee
===================================

Welcome to *foresee* documentation!

*foresee* is a python package.
Provided a time series and its parameters, foresee can generate forecasts using several
time series forecasting models in python, can tune hyper parameters of these models,
and can compare their forecast results using out of sample forecast accuracy. This library
can process more than one time series if a time series id is provided. To get started, install *foresee*
using pip

.. code-block:: shell

	$ pip install foresee
	
and try one of these examples.

* :ref:`single-time-series`
* :ref:`many-time-series`
* :ref:`drop-file-forecast`
 
or try it out at: https://easy-forecast.herokuapp.com/

.. note::
	Code and documentation for this library are still under development and will change frequently. 




.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
   foresee/introduction
   foresee/quick_start
   foresee/modules
   foresee/models
   foresee/authors
   foresee/license
   foresee/contribute
   



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
