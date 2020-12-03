import pandas as pd
import numpy as np
from fitter import Fitter
import scipy
import os

def excess_deaths_US(directory):
    """ 
    Load US excess death data taken from the following CDC website: 
    https://www.cdc.gov/nchs/nvss/vsrr/covid19/excess_deaths.htm
    
    Parameters: 
    directory (string): path of excess death data file 
  
    Returns: 
    excess_death_dict (dictionary): excess death data dictionary
  
    """
    
    # load raw data
    data = pd.read_csv(directory)
    
    # identify all US states in the data
    states = data['State'].unique()

    # initalize dictionary
    excess_death_dict = {}
    
    for state in states:
        state_data = data[(data['State'] == '%s'%state) \
                          & (data['Week Ending Date'] >= '2020-01-04')]
    
        observed_cases = state_data['Observed Number'].fillna(0).tolist()
        expected_count = state_data['Average Expected Count'].fillna(0).tolist()
        lower_estimate = state_data['Excess Lower Estimate'].fillna(0).tolist()
        higher_estimate = state_data['Excess Higher Estimate'].fillna(0).tolist()
    
        low_total = state_data['Total Excess Lower Estimate in 2020'].fillna(0).to_numpy()[0] 
        high_total = state_data['Total Excess Higher Estimate in 2020'].fillna(0).to_numpy()[0] 

        mean = 0.5*(low_total+high_total)
        
        # pay attention that the original CDC data lists all states multiple times
        # we removed these multiple occurrences in the CSV file
        ratio = mean/sum(expected_count)
        ratio_low = low_total/sum(expected_count)
        ratio_high = high_total/sum(expected_count)
        
        excess_death_dict[state] = {'excess deaths' : mean, \
                                     'excess deaths lwr' : low_total, \
                                     'excess deaths upr' : high_total, \
                                     'ratio' : ratio, \
                                     'ratio_low' : ratio_low, \
                                     'ratio_high' : ratio_high
                                   }
        
    return excess_death_dict

def excess_deaths_global(directory,
                         threshold = 0,
                         CI_factor = 1.96):
    """ 
    Load global excess death data taken from the following GitHub repository: 
    https://github.com/TheEconomist/covid-19-excess-deaths-tracker
    
    Parameters: 
    directory (string): path of excess death data file 
    threshold (int): threshold above which Covid deaths are counted
    CI_factor (float): prefactor to scale CI (1.96 corresponds to a 95% CI)
    
    Returns: 
    excess_death_dict (dictionary): excess death data dictionary
  
    """
    
    # initalize dictionary
    excess_death_dict = {}
    
    for file in os.listdir(directory):
        data = pd.read_csv(os.path.join(directory, file))
        
        country = data['country'].unique()[0]
        
        # exclude countries for which there are no CIs are available
        if country not in ["Mexico","South Africa","Spain","Brazil"]:
            region_deaths = data[data['region'] == '%s'%country]
            covid_deaths = region_deaths['covid_deaths'].to_numpy()
     
            excess_deaths = region_deaths['excess_deaths.fit'].to_numpy()[covid_deaths > threshold]
            excess_deaths_lwr = region_deaths['excess_deaths.lwr'].to_numpy()[covid_deaths > threshold]
            excess_deaths_upr = region_deaths['excess_deaths.upr'].to_numpy()[covid_deaths > threshold]
            expected_deaths = sum(region_deaths['expected_deaths.fit'].to_numpy()[covid_deaths > threshold])+1e-9
            
            # the underlying CI is a 95% CI, so we divide by 1.96 to obtain
            # the underlying sigma
            
            sigma = (excess_deaths_upr-excess_deaths)/1.96
            delta_y = CI_factor*np.linalg.norm(sigma)

            excess_deaths = sum(excess_deaths)

            ratio = excess_deaths/expected_deaths
            ratio_low = (excess_deaths-delta_y)/expected_deaths
            ratio_high = (excess_deaths+delta_y)/expected_deaths
        
            excess_death_dict[country] = {'excess deaths': excess_deaths, \
                                             'excess deaths lwr': excess_deaths-delta_y, \
                                             'excess deaths upr': excess_deaths+delta_y, \
                                             'ratio' : ratio, \
                                             'ratio_low' : ratio_low, \
                                             'ratio_high' : ratio_high
                                         }
        
        # for the remaining countries there are no CIs are available
        else:
            covid_deaths = data['covid_deaths'].to_numpy()
            excess_deaths = sum((data['excess_deaths'].to_numpy())[covid_deaths > threshold])
            expected_deaths = sum(data['expected_deaths'].to_numpy())
            
            ratio = excess_deaths/expected_deaths

            excess_death_dict[country] = {'excess deaths': excess_deaths, \
                                             'excess deaths upr': -1, \
                                             'excess deaths lwr': -1, \
                                             'ratio': ratio, \
 				             'ratio_low' : -1, \
                                             'ratio_high' : -1
                                        }
    return excess_death_dict

def IFR_US(covid_data_US, 
           excess_death_dict_US, 
           p = 0.1):
    """ 
    Calculate IFRs based on excess death data and the following GitHub repository data: 
    https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv

    Parameters: 
    covid_data_US (pandas DataFrame): Covid data 
    excess_death_dict_US (dictionary): excess death data dictionary
    p (float): fraction of reported cases
    
    Returns: 
    IFR_US (dictionary): IFR dictionary
  
    """
    
    states = covid_data_US['state'].unique()
    
    IFR_US = {}
    
    for state in states:
        
        cases = float(covid_data_US[covid_data_US['state'] == state]['cases'])

        try:        
            IFR = excess_death_dict_US[state]['excess deaths']/cases*p
            IFR_US[state] = IFR
        
        except:
            pass
        
    return IFR_US

def CFR_US(covid_data_US):
    """ 
    Calculate CFRs based on excess death data and the following GitHub repository data: 
    https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv

    Parameters: 
    covid_data_US (pandas DataFrame): Covid data
    
    Returns: 
    CFR_US (dictionary): CFR dictionary
  
    """
    
    states = covid_data_US['state'].unique()
    
    CFR_US = {}
    
    for state in states:
        
        deaths = covid_data_US[covid_data_US['state'] == state]['deaths'].to_numpy()
        cases = covid_data_US[covid_data_US['state'] == state]['cases'].to_numpy()
        
        CFR_US[state] = float(deaths/cases)
        
    return CFR_US

def CFR_M_global(covid_data_global):
    """ 
    Calculate CFR and M based on the following GitHub repository data: 
    https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/    

    Parameters: 
    covid_data_global (pandas DataFrame): Covid data 

    Returns: 
    CFR_global (dictionary), M_global (dictionary): CFR and M dictionaries
  
    """
    
    countries = covid_data_global['Country_Region'].unique()
    
    CFR_global = {}
    M_global = {}
    
    for country in countries:
    
        country_data = covid_data_global[covid_data_global['Country_Region'] == country]
        
        confirmed_cases = sum(country_data['Confirmed'].to_numpy())
        confirmed_deaths = sum(country_data['Deaths'].to_numpy())
        confirmed_recovered = sum(country_data['Recovered'].to_numpy())
        
        CFR = confirmed_deaths/confirmed_cases
        M = confirmed_deaths/(confirmed_deaths + confirmed_recovered)
            
        CFR_global[country] = CFR
        M_global[country] = M

    return CFR_global, M_global

def IFR_global(covid_data_global, 
               excess_death_dict_global, 
               p = 0.1):
    """ 
    Calculate IFRs based on excess death data and the following GitHub repository data: 
    https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/    

    Parameters: 
    covid_data_global (pandas DataFrame): Covid data 
    excess_death_dict_global (dictionary): excess death data dictionary
    p (float): fraction of reported cases
    
    Returns: 
    IFR_global (dictionary): IFR dictionary
  
    """
    
    countries = covid_data_global['Country_Region'].unique()
    
    IFR_global = {}
    
    for country in countries:
    
        country_data = covid_data_global[covid_data_global['Country_Region'] == country]
        
        confirmed_cases = sum(country_data['Confirmed'].to_numpy())
        
        try:
            IFR = excess_death_dict_global[country]['excess deaths']/confirmed_cases*p
            IFR_global[country] = IFR
            
        except:
            pass
        
    return IFR_global

def M_excess_global(covid_data_global, 
                    excess_death_dict_global, 
                    gamma_d_mu = 1e2):
    """ 
    Calculate M based on excess death data and the following GitHub repository data: 
    https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/    

    Parameters: 
    covid_data_global (pandas DataFrame): Covid data 
    excess_death_dict_global (dictionary): excess death data dictionary
    gamma_d_mu (float): \gamma over \mu ()
    
    Returns: 
    M_excess_global (dictionary): dictionary that stores "M excess"
  
    """
        
    countries = covid_data_global['Country_Region'].unique()
    
    M_excess = {}
    
    for country in countries:
    
        try:
            Rast = sum(covid_data_global[covid_data_global['Country_Region'] == country]['Recovered'].to_numpy())
            Dast = sum(covid_data_global[covid_data_global['Country_Region'] == country]['Deaths'].to_numpy())
            De = excess_death_dict_global[country]['excess deaths']
            M = De/(De + Rast + gamma_d_mu*(De - Dast))
            M_excess[country] = M
            
        except:
            pass
        
    return M_excess

def find_bins(observations, 
              width):
    """ 
    Calculate bins given a set of observations and the desired bin width.

    Parameters: 
    observations (numpy array): histogram data 
    width (float): desired bin width
    
    Returns: 
    bins (numpy array): bins with a distance that corresponds to the desired
    bin width.
  
    """
    
    minimmum = np.min(observations)
    maximmum = np.max(observations)
    bound_min = -1.0 * (minimmum % width - minimmum)
    bound_max = maximmum - maximmum % width + width
    n = int((bound_max - bound_min) / width) + 1
    bins = np.linspace(bound_min, bound_max, n)
    
    return bins

def fit(data, 
        xmin, 
        xmax):
    """ 
    Determine the distribution that best describes some observations.
    
    Parameters: 
    data (numpy array): observation data 
    xmin (float): plot xmin
    xmax (float): plot xmax
    
    Returns: 
    xx (numpy array), pdf_fitted (numpy array): fitted distribution x,y values
  
    """
    
    common_distr = ['gamma', 'rayleigh', 'norm', 'expon', 'lognorm', 'beta', \
                    'logistic', 'invgamma', 'exponpow', 'chi2']

    f = Fitter(data, distributions=common_distr)
    f.fit()
    # may take some time since by default, all distributions are tried
    # but you call manually provide a smaller set of distributions
    #f.summary()
    best_fit = f.get_best()
    best_fit_name = [x for x in best_fit.keys()][0]
    best_fit_param = [x for x in best_fit.values()][0]
    
    #print(f.summary())
    print("Distribution name: ", best_fit_name)
    print("Distribution parameters: ", best_fit_param)
    
    dist = eval("scipy.stats." + best_fit_name)
    xx = np.linspace(xmin, xmax, 200)
    pdf_fitted = dist.pdf(xx, *best_fit_param)
    
    mean = float(dist.stats(*best_fit_param, moments='m'))
    lwr = dist.ppf(0.025, *best_fit_param)
    upr = dist.ppf(0.975, *best_fit_param)
    
    print("Mean: ", mean, lwr, upr)

    return xx, pdf_fitted
