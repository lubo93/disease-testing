import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
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
fig_width_pt = 2*245    # Get this from LaTeX using \showthe\columnwidth
golden_mean = (np.sqrt(5.) - 1.) / 2.  # Aesthetic ratio
ratio = golden_mean
inches_per_pt = 1. / 72.27  # Convert pt to inches
fig_width = fig_width_pt * inches_per_pt  # width in inches
fig_height = fig_width*ratio  # height in inches
fig_size = [fig_width, 0.5*fig_height]
rcParams.update({'figure.figsize': fig_size})

#%%

def IFR(De, fraction, N):
    return De/fraction/N

def f(b, ftilde, FPR, FNR):
    return (ftilde-FPR)/(np.exp(b)*(1-FPR-ftilde)+ftilde-FPR)


def CV_IFR(Sigma_e, De, sigma_I, sigma_II, sigma_b, FPR, FNR, ftilde, b, f):
    
    X = ftilde-FPR
    
    CV2 = (Sigma_e/De)**2
    CV2 += sigma_I**2*(1-f)**2/X**2
    CV2 += sigma_II**2*np.exp(2*b)*f**2/X**2
    CV2 += sigma_b**2*f**2*(1-f)**2/X**2

    return np.sqrt(CV2)
    
sns.set_style("whitegrid")  # "white","dark","darkgrid","ticks"
boxprops = dict(linestyle='-', linewidth=1.5, color='#00145A')
flierprops = dict(marker='o', markersize=2,
                  linestyle='none')
whiskerprops = dict(color='#00145A')
capprops = dict(color='#00145A')
medianprops = dict(linewidth=1.5, linestyle='-', color='#01FBEE')
        
N = 330e6
De = 268327
Sigma_e = 6536/1.96

FPR = 0.05
FNR = 0.2
ftilde = 0.093

sigma_I = 0.02
sigma_II = 0.05

xmin = -1
xmax = 1
b_arr = np.linspace(xmin, xmax, 100)

fig, ax = plt.subplots(ncols = 3, figsize = fig_size)

ax[0].text(0.03*(xmax-xmin)+xmin, 0.88*0.05, r"(a)")
ax[0].plot(b_arr, [IFR(De, f(b, ftilde, FPR, FNR), N) for b in b_arr], color = 'k', label = r"true IFR")
ax[0].plot(b_arr, len(b_arr)*[De/(ftilde*N)], ls = '--', color = 'k', label = r"observed IFR")

def colorFader(c1,c2,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

c1 = 'tab:blue'
c2 = 'tab:red'
#n = 2000

#for x in range(n+1):
#    ax[0].fill_between([xmin+(xmax-xmin)/n*x,xmin+(xmax-xmin)/n*(x+1)], 0.05, 0, facecolor=colorFader(c1, c2, x/n), edgecolor=colorFader(c1, c2, x/n), alpha = 0.04)
    
ax[0].text(-0.48, 0.0215, "negative \n testing bias", fontsize = 8, horizontalalignment = "center")
ax[0].text(0.56, 0.0115, "positive \n testing bias", fontsize = 8, horizontalalignment = "center")


#ax[0].legend(loc = "upper center", frameon = False, fontsize = 8)
ax[0].set_xlabel(r"$b$")
ax[0].set_ylabel(r"$\mathrm{IFR}$")
ax[0].set_xlim(xmin, xmax)
ax[0].set_ylim(0,0.05)

ax[1].text(0.03*(xmax-xmin)+xmin, 0.88*0.8, r"(b)")

ax[1].plot(b_arr, [CV_IFR(Sigma_e, De, sigma_I, sigma_II, 0.2, FPR, FNR, \
          ftilde, b, f(b, ftilde, FPR, FNR)) for b in b_arr], color = 'k', \
          label = r"$\frac{\Sigma_{\mathrm{IFR}}}{\mathrm{IFR}}$")
    
ax[1].plot(b_arr, len(b_arr)*[Sigma_e/De], ls = '--', color = 'k',\
           label = r"$\frac{\Sigma_e}{\bar{D}_{e}}$")

ax[1].legend(loc = 4, frameon = False, ncol = 1)
ax[1].set_xlabel(r"$b$")
ax[1].set_ylabel(r"$\mathrm{CV}$")
ax[1].set_xlim(xmin, xmax)
ax[1].set_ylim(0,0.8)

ax[2].text(0.87, 0.88*8, r"(c)")

FPR_arr = np.linspace(0, 1, 200)

ax[2].set_xlabel(r"FPR")
ax[2].set_ylabel(r"CV")
ax[2].set_xlim(0,1)
ax[2].set_ylim(0,8)
ax[2].set_yticks([0,4,8])

plt.tight_layout()
plt.savefig('IFR_CV.png', dpi = 480)
plt.show()