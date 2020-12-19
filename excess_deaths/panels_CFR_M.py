import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
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
fig_size = [2*fig_width, fig_height]
rcParams.update({'figure.figsize': fig_size})

sns.set_style("whitegrid")  # "white","dark","darkgrid","ticks"
boxprops = dict(linestyle='-', linewidth=1.5, color='#00145A')
flierprops = dict(marker='o', markersize=2,
                  linestyle='none')
whiskerprops = dict(color='#00145A')
capprops = dict(color='#00145A')
medianprops = dict(linewidth=1.5, linestyle='-', color='#01FBEE')

# excess deaths US
excess_death_dict_US = excess_deaths_US("Excess_Deaths_Associated_with_COVID-19.csv")

# excess deaths global
excess_death_dict_global = excess_deaths_global("../covid-19-excess-deaths-tracker/output-data/excess-deaths", threshold = 0)

# covid data
covid_data_US = pd.read_csv("us-states.csv")
covid_data_global = pd.read_csv("12-10-2020.csv")

M_e_global = M_excess_global(covid_data_global, excess_death_dict_global)

CFR_global, M_global = CFR_M_global(covid_data_global)
IFR_global = IFR_global(covid_data_global, excess_death_dict_global)
#%%
fig, ax = plt.subplots(ncols = 2)
xx = np.linspace(0,100,100)
ax[0].plot(xx, xx, color = 'k', linewidth = 1)
         
countries = covid_data_global['Country_Region'].unique()

for country in countries:

    CFR = CFR_global[country]
    M = M_global[country]

    x = CFR
    y = M
    
    ax[0].plot(x, y, 'o',  markersize = 5, color = '#ffa600', alpha = 0.5)
    if y > 0.1:
        if country == "MS Zaandam":
            ax[0].text(x-0.02, y-0.1, r'%s'%country, size = 7, alpha = 0.8)
        elif country == "United Kingdom":
            ax[0].text(x-0.014, y-0.09, r'%s'%country, size = 7, alpha = 0.8)
        elif country == "Sweden":
            ax[0].text(x+0.006, y-0.06, r'%s'%country, size = 7, alpha = 0.8)
        elif country == "Serbia":
            ax[0].text(x+0.0065, y-0.055, r'Serb.', size = 7, alpha = 0.8)
        elif country == "Netherlands":
            ax[0].text(x-0.016, y+0.05, r'%s'%country, size = 7, alpha = 0.8)
        elif country == "Yemen":
            ax[0].text(x-0.026, y+0.04, r'%s'%country, size = 7, alpha = 0.8)
        elif country == "Belgium":
            ax[0].text(x+0.008, y, r'%s'%country, size = 7, alpha = 0.8)
        elif country == "Greece":
            ax[0].text(x-0.016, y+0.04, r'%s'%country, size = 7, alpha = 0.8)
        elif country == "Western Sahara":
            ax[0].text(x-0.016, y-0.09, r'%s'%country, size = 7, alpha = 0.8)
        elif country == "Mexico":
            ax[0].text(x-0.003, y+0.04, r'%s'%country, size = 7, alpha = 0.8)
        elif country == "France":
            ax[0].text(x+0.005, y+0.005, r'%s'%country, size = 7, alpha = 0.8)
      
ax[0].text(0.02*0.3, 0.9*1, r"(a)")  
ax[0].set_xlabel(r'CFR')
ax[0].set_ylabel(r'$M$')
ax[0].set_xlim(0,0.3)
ax[0].set_ylim(0,1)

countries = covid_data_global['Country_Region'].unique()

ax[1].plot(xx, xx, color = 'k', linewidth = 1)

for country in countries:
    
    try:
        IFR = IFR_global[country]
        M = M_e_global[country]
    
        x = IFR
        y = M
        
        ax[1].plot(x, y, 'o',  markersize = 5, color = '#ffa600', alpha = 0.5) 
        
        if y > 0.001:
            if country == "Ecuador":
                ax[1].text(x-0.002, y+0.007, r'%s'%country, size = 7, alpha = 0.8)
            elif country == "Mexico":
                ax[1].text(x-0.001, y+0.007, r'%s'%country, size = 7, alpha = 0.8)
            elif country == "Sweden":
                ax[1].text(x-0.001, y+0.007, r'%s'%country, size = 7, alpha = 0.8)
            elif country == "Italy":
                ax[1].text(x-0.0007, y+0.01, r'%s'%country, size = 7, alpha = 0.8)
            elif country == "Austria":
                ax[1].text(x-0.0002, y+0.006, r'%s'%country, size = 7, alpha = 0.8)
            elif country == "Netherlands":
                ax[1].text(x-0.0003, y+0.006, r'%s'%country, size = 7, alpha = 0.8)
            elif country == "Chile":
                ax[1].text(x-0.0018, y+0.006, r'%s'%country, size = 7, alpha = 0.8)
            elif country == "Spain":
                ax[1].text(x+0.0006, y-0.001, r'%s'%country, size = 7, alpha = 0.8)
            elif country == "Peru":
                ax[1].text(x+0.0004, y+0.01, r'%s'%country, size = 7, alpha = 0.8)
            elif country == "Denmark":
                ax[1].text(x+0.0003, y+0.007, r'%s'%country, size = 7, alpha = 0.8)
            elif country == "South Africa":
                ax[1].text(x+0.0004, y+0.007, r'South Afr.', size = 7, alpha = 0.8)
            elif country == "Portugal":
                ax[1].text(x+0.0006, y-0.002, r'Port.', size = 7, alpha = 0.8)
            elif country == "Russia":
                ax[1].text(x-0.003, y+0.013, r'%s'%country, size = 7, alpha = 0.8)
            
    except:
        pass

ax[1].text(0.02*0.03, 0.9*0.2, r"(b)")  
ax[1].set_xlabel(r'IFR')
ax[1].set_ylabel(r'$\mathcal{M}$')
ax[1].set_xlim(0,0.02)
ax[1].set_ylim(0,0.2)
plt.tight_layout()
plt.savefig('calM_vs_IFR_global.png', dpi = 300)
plt.close("all")
