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

# excess deaths US
excess_death_dict_US = excess_deaths_US("Excess_Deaths_Associated_with_COVID-19.csv")

# excess deaths global
excess_death_dict_global = excess_deaths_global("../covid-19-excess-deaths-tracker/output-data/excess-deaths", threshold = 0)

# covid data
covid_data_US = pd.read_csv("us-states.csv.1")
covid_data_global = pd.read_csv("10-05-2020.csv")

# mortality measures
CFR_US = CFR_US(covid_data_US)
IFR_US = IFR_US(covid_data_US, excess_death_dict_US)
CFR_global, M_global = CFR_M_global(covid_data_global)
IFR_global = IFR_global(covid_data_global, excess_death_dict_global)
M_e_global = M_excess_global(covid_data_global, excess_death_dict_global)

# prepare mortality measures for box plot
mean_arr_US = [x['ratio'] for x in excess_death_dict_US.values()]
mean_arr_global = [x['ratio'] for x in excess_death_dict_global.values()]

mean_arr = np.append(mean_arr_US, mean_arr_global)
CFR_US_values = [x for x in CFR_US.values()]
CFR_global_values = [x for x in CFR_global.values()]
CFR_arr = np.append(CFR_US_values, CFR_global_values)

IFR_US_values = [x for x in IFR_US.values()]
IFR_global_values = [x for x in IFR_global.values()]
IFR_arr = np.append(IFR_US_values, IFR_global_values)

M_global_arr = [x for x in M_global.values()]
M_e_global_arr = [x for x in M_e_global.values()]

names = [r'$r$', 'CFR', 'IFR', r'$M$', r'$\mathcal{M}$']
x_arr = [len(mean_arr)*[1], len(CFR_arr)*[2], len(IFR_arr)*[3], len(M_global_arr)*[4], len(M_e_global_arr)*[5]]
val_arr = [mean_arr, CFR_arr, IFR_arr, M_global_arr, M_e_global_arr]

# seaborn style
sns.set_style("whitegrid")  # "white","dark","darkgrid","ticks"
boxprops = dict(linestyle='-', linewidth=1.5, color='#00145A')
flierprops = dict(marker='o', markersize=2,
                  linestyle='none')
whiskerprops = dict(color='#00145A')
capprops = dict(color='#00145A')
medianprops = dict(linewidth=1.5, linestyle='-', color='#01FBEE')

           
fig, ax = plt.subplots(ncols = 5)

bins_arr = find_bins(mean_arr, 0.05)

xx1, pdf_fitted1 = fit(mean_arr, 0, 1)

ax[0].text(0.04*0.5, 0.9*20, r"(c)")
ax[0].hist(mean_arr, bins = bins_arr, density = True, color = 'tab:blue', alpha = 0.6)
ax[0].plot(xx1, pdf_fitted1, 'k', alpha = 0.6)
ax[0].set_xlim(0,0.5)
ax[0].set_ylim(0,20)
ax[0].set_xlabel(r"$r$")
ax[0].set_ylabel(r"PDF")

bins_arr = find_bins(CFR_arr, 0.05*0.2)

xx2, pdf_fitted2 = fit(CFR_arr, 0, 0.2)

ax[1].text(0.04*0.2, 0.9*50, r"(d)")
ax[1].hist(CFR_arr, bins = 31, density = True, color = 'tab:orange', alpha = 0.6)
ax[1].plot(xx2, pdf_fitted2, 'k', alpha = 0.6)
ax[1].set_xlim(0,0.2)
ax[1].set_ylim(0,50)
ax[1].set_xlabel(r"$\mathrm{CFR}$")

bins_arr = find_bins(IFR_arr, 0.05*0.02)

xx3, pdf_fitted3 = fit(IFR_arr, 0, 0.02)

ax[2].text(0.04*0.02, 0.9*300, r"(e)")
ax[2].hist(IFR_arr, bins = bins_arr, density = True, color = 'tab:green', alpha = 0.6)
ax[2].plot(xx3, pdf_fitted3, 'k', alpha = 0.6)
ax[2].set_xlim(0,0.02)
ax[2].set_ylim(0,300)
ax[2].set_xlabel(r"$\mathrm{IFR}$")

bins_arr = find_bins(M_global_arr, 0.05*0.1)

xx4, pdf_fitted4 = fit(M_global_arr, 0, 0.1)

ax[3].text(0.04*0.1, 0.9*40, r"(f)")
ax[3].hist(M_global_arr, bins = bins_arr, density = True, color = 'tab:red', alpha = 0.6)
ax[3].plot(xx4, pdf_fitted4, 'k', alpha = 0.6)
ax[3].set_xlim(0,0.1)
ax[3].set_ylim(0,40)
ax[3].set_xlabel(r"$M$")

bins_arr = find_bins(M_e_global_arr, 0.05*0.4)

xx5, pdf_fitted5 = fit(M_e_global_arr, -0.2, 0.2)

ax[4].text(0.04*0.4-0.2, 0.9*20, r"(g)")
ax[4].hist(M_e_global_arr, bins = bins_arr, density = True, color = 'tab:purple', alpha = 0.6)
ax[4].plot(xx5, pdf_fitted5, 'k', alpha = 0.6)
ax[4].set_xlim(-0.2,0.2)
ax[4].set_ylim(0,20)
ax[4].set_xlabel(r"$\mathcal{M}$")

plt.tight_layout()
plt.savefig('distributions.png', dpi = 300)
      
fig, ax = plt.subplots(ncols = 2)
ax[0].text(0.6, 0.9*1.2-0.2, r"(a)")
ax[0].boxplot(val_arr, labels = names, notch=False, boxprops=boxprops, \
                whiskerprops=whiskerprops,capprops=capprops, \
                flierprops=flierprops, \
                medianprops=medianprops,showmeans=False,showfliers=False)  
                   
for x, val in zip(x_arr, val_arr):
    ax[0].scatter(x, val, alpha=0.4, s = 20)
  
ax[0].set_ylim(-0.2,1)

# define states/regions
regions = ["Italy", "Brazil", "Mexico"]

ax[1].text(0.59, 0.9*0.5, r"(b)")


for region in regions:
    try:
        x_vals = [1,2,3,4,5]
        y_vals = [excess_death_dict_global["%s"%region]["ratio"], \
                  CFR_global["%s"%region], IFR_global["%s"%region], \
                  M_global["%s"%region], M_e_global["%s"%region]]
        
        if excess_death_dict_global["%s"%region]["ratio_high"] != -1:
            y_err_vals = [excess_death_dict_global["%s"%region]["ratio_high"]-\
                          excess_death_dict_global["%s"%region]["ratio"],0,0,0,0]
        else:
            y_err_vals = [0,0,0,0,0]
        
        ax[1].plot(x_vals, y_vals, alpha=0.2, color = 'k')
        ax[1].errorbar(x_vals, y_vals, yerr=y_err_vals, alpha=0.6, fmt='o', markersize=4, label = r'%s'%region)

    except:
        pass
    
regions = ["New York"]

for region in regions:
    try:
        x_vals = [1,2,3]
        y_vals = [excess_death_dict_US["%s"%region]["ratio"], \
                  CFR_US["%s"%region], IFR_US["%s"%region]]
        
        ax[1].plot(x_vals, y_vals, alpha=0.2, color = 'k')
        ax[1].errorbar(x_vals, y_vals, alpha=0.6, fmt='o', markersize=4, label = r'%s'%region)
    
    except:
        pass

x_vals = [1,2,3,4,5]
ax[1].legend(loc = 1, frameon = False, fontsize = 8) 
ax[1].set_xticks(x_vals)  
ax[1].set_xticklabels(names)
ax[1].set_xlim(0.5,5.5)
ax[1].set_ylim(0,0.5)

plt.tight_layout()
plt.savefig('boxplot.png', dpi = 300)