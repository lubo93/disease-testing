import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.dates as md
from matplotlib import rcParams
import seaborn as sns

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

data = pd.read_csv("../covid-19-excess-deaths-tracker/output-data/excess-deaths/ecuador_excess_deaths.csv")

covid_deaths = data[data['region'] == 'Ecuador']

dates = covid_deaths['start_date'].to_numpy()
excess_deaths = covid_deaths['excess_deaths.fit'].to_numpy()
excess_deaths_h = covid_deaths['excess_deaths.lwr'].to_numpy()
excess_deaths_l = covid_deaths['excess_deaths.upr'].to_numpy()

covid_deaths_data = covid_deaths['covid_deaths'].to_numpy()
delta = (excess_deaths_h-excess_deaths)/1.96

cum_sum = np.cumsum(excess_deaths)
cum_sum_covid = np.cumsum(covid_deaths_data)

cum_std = np.asarray([1.96*np.linalg.norm(delta[:i])*(i+1)/i if i > 0 else \
                      1.96*np.linalg.norm(delta[:i]) for i in range(len(delta))])

Ecuador_population = 17.08e6
prefactor = 1/Ecuador_population*1e5

#%%

sns.set_style("whitegrid")  # "white","dark","darkgrid","ticks"
boxprops = dict(linestyle='-', linewidth=1.5, color='#00145A')
flierprops = dict(marker='o', markersize=2,
                  linestyle='none')
whiskerprops = dict(color='#00145A')
capprops = dict(color='#00145A')
medianprops = dict(linewidth=1.5, linestyle='-', color='#01FBEE')
                   
fig, ax = plt.subplots(figsize = fig_size)
ax.set_title(r'Ecuador')
ax.text(datetime.date(2020, 1, 5), 0.89*100, r'(d)')
ax2 = ax.twinx()
ax.set_ylabel("weekly")
ax2.set_ylabel("cumulative", color = '#C81C1A')

ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%y'))
ax.plot(datetime.date(2019, 8, 1), 100)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%y'))
ax2.plot(datetime.date(2019, 8, 1), 100)
    
ax.errorbar(dates, prefactor*covid_deaths_data, color = 'k', \
            label = r'$\delta D_{\mathrm{c}}$')

ax.errorbar(dates, prefactor*excess_deaths, yerr = prefactor*delta, \
            color = '#223A27', ecolor='#223A27', elinewidth=1, \
            capsize=2, label = r'$\delta D_{\mathrm{e}}$')

ax2.errorbar(dates, prefactor*cum_sum_covid, color = 'DarkRed', \
             ecolor='k', elinewidth=1, capsize=2, label = r'$D_{\mathrm{c}}$')

ax2.errorbar(dates, prefactor*cum_sum, yerr = prefactor*cum_std, \
             color = '#C81C1A', ecolor='#C81C1A', elinewidth=1, \
             capsize=2, label = r'$D_{\mathrm{e}}$')

ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%y'))
ax.xaxis.set_minor_locator(md.MonthLocator())
ax.set_xlim([datetime.date(2020, 1, 1), datetime.date(2020, 9, 1)])
    
for tick in ax.get_xticklabels():
    tick.set_rotation(45)

#ax.legend(loc = 3, fontsize = 8, frameon = False)
#ax2.legend(loc = 4, fontsize = 8, frameon = False)

ax.set_ylim(0,100)
ax2.set_ylim(0,200)
ax2.yaxis.grid()
ax2.tick_params(axis='y', colors='#C81C1A')
ax.tick_params(axis='y', colors='#223A27')
plt.tight_layout()
plt.savefig('Ecuador_Covid_excess.png', dpi = 480)
plt.show()