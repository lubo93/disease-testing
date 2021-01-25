# disease-testing

## Project Description

This project enables users to analyze COVID-19 mortality data and generate random and biased (disease) testing distributions.

Please run the files in ``excess_deaths`` to compute different mortality measures and analyze COVID-19 mortality data for different jurisdictions. (Make sure that you download the most recent source data, see below.) The coefficient of variation (CV) of the infection fatality ratio (IFR) can be directly calculated via ``IFR_CV.py``.

To study the influence of different type I and II errors (or false-positive and false-negative rates) on disease testing distributions, you can use the examples ``testing_analytical_replacement_false.py`` and ``testing_analytical_replacement_true.py`` in the ``src`` folder and plot the generated results with ``testing_plot.py``. The resulting plot will be similar to the one shown below:

![Image](testing.png)


## Related Data Sources

* https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv
* https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports
* https://github.com/TheEconomist/covid-19-excess-deaths-tracker

## Reference
* L. Böttcher, M. R. D'Orsogna, T. Chou, [Using excess deaths and testing statistics to improve estimates of COVID-19 mortalities](https://www.medrxiv.org/content/10.1101/2021.01.10.21249524v1.full), medRxiv:2021.01.10.21249524, arXiv:2101.03467

Please cite our paper if you use our data analysis and disease testing frameworks.

```
@article{bottcher2021using,
  title={Using excess deaths and testing statistics to improve estimates of COVID-19 mortalities},
  author={B{\"o}ttcher, Lucas and D'Orsogna, Maria and Chou, Tom},
  journal={arXiv preprint arXiv:2101.03467},
  year={2021}
}
```
