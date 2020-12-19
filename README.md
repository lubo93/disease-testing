# disease-testing

## Project Description

This project enables users to analyze COVID-19 mortality data and generate random and biased (disease) testing distributions.

Please run the files in ``excess_deaths'' to compute different mortality measures and analyze COVID-19 mortality data for different jurisdiction. (Make sure that you download the most recent source data, see below.) The coefficient of variation (CV) of the infection fatality ratio (IFR) can be directly calculated via ``IFR_CV.py''.

To study the influence of different type I and II errors (or false-positive and false-negative rates) on disease testing distributions, you can use the examples ``testing_analytical_replacement_false.py`` and ``testing_analytical_replacement_true.py`` in the ``src`` folder and plot the generated results with ``testing_plot.py``. The resulting plot will be similar to the one shown below:

![Image](testing.png)


## Related Data Sources

* https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv
* https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports
* https://github.com/TheEconomist/covid-19-excess-deaths-tracker
