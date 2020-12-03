import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from data_analysis_lib.load_data import *
from matplotlib import rcParams

# customized settings
params = {  # 'backend': 'ps',
    'font.family': 'serif',
    'font.serif': 'Latin Modern Roman',
    'font.size': 10,
    'axes.labelsize': 'medium',
    'axes.titlesize': 'medium',
    'legend.fontsize': 'medium',
    'xtick.labelsize': 'small',
    'ytick.labelsize': 'small',
    'savefig.dpi': 150,
    'text.usetex': True}
# tell matplotlib about your params
rcParams.update(params)

# set nice figure sizes
fig_width_pt = 245    # Get this from LaTeX using \showthe\columnwidth
golden_mean = (np.sqrt(5.) - 1.) / 2.  # Aesthetic ratio
ratio = golden_mean
inches_per_pt = 1. / 72.27  # Convert pt to inches
fig_width = fig_width_pt * inches_per_pt  # width in inches
fig_height = fig_width*ratio  # height in inches
fig_size = [fig_width, fig_height]
rcParams.update({'figure.figsize': fig_size})

# excess deaths US
excess_death_dict_US = excess_deaths_US("Excess_Deaths_Associated_with_COVID-19.csv")

# excess deaths global
excess_death_dict_global = excess_deaths_global("../covid-19-excess-deaths-tracker/output-data/excess-deaths", threshold = 0)

# covid data
covid_data_US = pd.read_csv("us-states.csv.1")
covid_data_global = pd.read_csv("10-29-2020.csv")

#%%

sns.set_style("whitegrid")  # "white","dark","darkgrid","ticks"
boxprops = dict(linestyle='-', linewidth=1.5, color='#00145A')
flierprops = dict(marker='o', markersize=2,
                  linestyle='none')
whiskerprops = dict(color='#00145A')
capprops = dict(color='#00145A')
medianprops = dict(linewidth=1.5, linestyle='-', color='#01FBEE')
        
x_vals = []
y_vals = []

plt.figure()
plt.text(0.02*200, 0.9*200, r"(a)")
xx = np.linspace(0,200,100)
plt.plot(xx, xx, color = 'k', linewidth = 1)
plt.plot(xx, 3*xx, linewidth = 1, ls = '-', color = '#006573')

countries = covid_data_global['Country_Region'].unique()
    
div = 1e3

for country in countries:

    country_data = covid_data_global[covid_data_global['Country_Region'] == country]
    
    confirmed_deaths = sum(country_data['Deaths'].to_numpy())

    x = confirmed_deaths
    
    try:
        y = excess_death_dict_global[country]['excess deaths']
        y_err1 = excess_death_dict_global[country]['excess deaths upr']
        y_err2 = excess_death_dict_global[country]['excess deaths lwr']
        
        x_vals.append(x)
        y_vals.append(y)
        
        deltay = y/div-y_err1/div        
        print(country, y/div, y/div-y_err1/div, y_err2/div-y/div)

        if y_err1 != -1:
            plt.errorbar(x/div, y/div, yerr = np.array([(y/div-y_err1/div,y_err2/div-y/div)]).T, ecolor='k', elinewidth=1, capsize=2, fmt = 'o', markersize = 5, color = '#ffa600', alpha = 0.8)
        else:
            plt.plot(x/div, y/div, 'o', markersize = 5, color = '#ffa600', alpha = 0.5)

        if (y/div > 20) & (country != 'Spain') & (country != 'Chile') & (country != 'Austria') & (country != 'Peru') & (country != 'Russia') & (country != 'Italy') & (country != 'France') & (country != 'Ecuador') & (country != 'South Africa'):
            plt.text(x/div-4, y/div+8.5, r'%s'%country, size = 9, alpha = 0.8)
        elif country == 'Spain':
            plt.text(x/div+2, y/div+7, r'%s'%country, size = 9, alpha = 0.8)
        elif country == 'Peru':
            plt.text(x/div+4, y/div-1.5, r'%s'%country, size = 9, alpha = 0.8)
        elif country == 'Russia':
            plt.text(x/div-24, y/div+16, r'%s'%country, size = 9, alpha = 0.8)
        elif country == 'Italy':
            plt.text(x/div-8, y/div+7, r'%s'%country, size = 9, alpha = 0.8)
        elif country == 'France':
            plt.text(x/div-8, y/div-17, r'%s'%country, size = 9, alpha = 0.8)
        elif country == 'Ecuador':
            plt.text(x/div-11, y/div+10.7, r'%s'%country, size = 9, alpha = 0.8)
        elif country == 'South Africa':
            plt.text(x/div+3, y/div, r'%s'%country, size = 9, alpha = 0.8)
    except:
        
        pass

mod = sm.OLS(y_vals, x_vals)
res = mod.fit()
slope = res.params[0]
slope1, slope2 = res.conf_int(0.05)[0]
print(slope)
print(slope1, slope2)   # 95% confidence interval

#plt.plot(xx, slope*xx, color = '#006573', alpha = 0.8, linewidth = 1)
#plt.fill_between(xx, slope2*xx, slope1*xx, color = '#006573', alpha = 0.3, linewidth = 1, ls = "--")
                 
plt.xlabel(r'confirmed deaths [$\times 10^3$]')
plt.ylabel(r'excess deaths [$\times 10^3$]')
plt.xlim(0,200)
plt.ylim(0,200)
plt.tight_layout()
plt.savefig('excess_vs_confirmed_global.png', dpi = 300)

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

plt.figure()
xx = np.linspace(0,100,100)
plt.plot(xx, xx, color = 'k', linewidth = 1)
#plt.plot(xx, 3*xx, linewidth = 1, ls = '--', color = '#003f5c')

states = covid_data_US['state'].unique()

x_vals = []
y_vals = []

for state in states:
    
    x = float(covid_data_US[covid_data_US['state'] == state]['deaths'])

    try:        
        
        y = excess_death_dict_US[state]['excess deaths']
        y_err1 = excess_death_dict_US[state]['excess deaths lwr']
        y_err2 = excess_death_dict_US[state]['excess deaths upr']
        
        d11 = 0.5*(y_err1-y_err2)/1.96

        if state == 'New York':
            y += excess_death_dict_US['New York City']['excess deaths']
            
            d12 = (excess_death_dict_US['New York City']['excess deaths'] - excess_death_dict_US['New York City']['excess deaths lwr'])/1.96
            y_err1 = y-1.96*np.sqrt(d11**2 +d12**2)
            y_err2 = y+1.96*np.sqrt(d11**2 +d12**2)
        #print(state, x, y, y_err1, y_err2)
        plt.errorbar(x/div, y/div, yerr = np.array([(y/div-y_err1/div,y_err2/div-y/div)]).T, fmt = 'o', markersize = 5, ecolor='k', elinewidth=1, capsize=2, color = '#ffa600', alpha = 0.8)
        
        x_vals.append(x)
        y_vals.append(y)
        
        if us_state_abbrev[state] == 'NY':
            plt.text(x/div+1, y/div-3, r'%s'%us_state_abbrev[state], size = 9, alpha = 0.8)
        elif us_state_abbrev[state] == 'NJ':
            plt.text(x/div+1, y/div-4, r'%s'%us_state_abbrev[state], size = 9, alpha = 0.8)
        elif us_state_abbrev[state] == 'CA':
            plt.text(x/div-2.8, y/div+2.1, r'%s'%us_state_abbrev[state], size = 9, alpha = 0.8)
        elif us_state_abbrev[state] == 'MA':
            plt.text(x/div+1, y/div-2, r'%s'%us_state_abbrev[state], size = 9, alpha = 0.8)
        elif us_state_abbrev[state] == 'FL':
            plt.text(x/div-2.5, y/div+0.8, r'%s'%us_state_abbrev[state], size = 9, alpha = 0.8)
        elif us_state_abbrev[state] == 'TX':
            plt.text(x/div+0.6, y/div+0.4, r'%s'%us_state_abbrev[state], size = 9, alpha = 0.8)
        elif us_state_abbrev[state] == 'IL':
            plt.text(x/div+0.5, y/div+1, r'%s'%us_state_abbrev[state], size = 9, alpha = 0.8)

    except:
        pass
    
mod = sm.OLS(y_vals, x_vals)
res = mod.fit()
slope = res.params[0]
slope1, slope2 = res.conf_int(0.05)[0]
print(slope)
print(slope1, slope2)   # 95% confidence interval

plt.plot(xx, slope*xx, color = '#006573', alpha = 0.8, linewidth = 1)
plt.fill_between(xx, slope2*xx, slope1*xx, color = '#006573', alpha = 0.3, linewidth = 1, ls = "--")

plt.text(0.02*40, 0.9*40, r"(b)")
plt.xlabel(r'confirmed deaths [$\times 10^3$]')
plt.ylabel(r'excess deaths [$\times 10^3$]')
plt.xlim(0,40)
plt.ylim(0,40)
plt.tight_layout()
plt.savefig('excess_vs_confirmed_US.png', dpi = 300)
