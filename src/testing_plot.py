import numpy as np
import matplotlib.pyplot as plt
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
fig_width_pt = 490    # Get this from LaTeX using \showthe\columnwidth
golden_mean = (np.sqrt(5.) - 1.) / 2.  # Aesthetic ratio
ratio = golden_mean
inches_per_pt = 1. / 72.27  # Convert pt to inches
fig_width = fig_width_pt * inches_per_pt  # width in inches
fig_height = fig_width*ratio  # height in inches
fig_size = [fig_width, fig_height]
rcParams.update({'figure.figsize': fig_size})

# load data
testing_replacement_true_IR = np.loadtxt("TESTING/testing_data_replacement_true_IR_210620.dat")
testing_replacement_true_b = np.loadtxt("TESTING/testing_data_replacement_true_b_210620.dat")
testing_replacement_true_FNR = np.loadtxt("TESTING/testing_data_replacement_true_FNR_210620.dat")
testing_replacement_true_FPR = np.loadtxt("TESTING/testing_data_replacement_true_FPR_210620.dat")
testing_replacement_false_IR = np.loadtxt("TESTING/testing_data_replacement_false_IR_210620.dat")
testing_replacement_false_b = np.loadtxt("TESTING/testing_data_replacement_false_b_210620.dat")
testing_replacement_false_FNR = np.loadtxt("TESTING/testing_data_replacement_false_FNR_210620.dat")
testing_replacement_false_FPR = np.loadtxt("TESTING/testing_data_replacement_false_FPR_210620.dat")

Q = 1e3

fig, ax = plt.subplots(nrows = 2, ncols = 2)

#%% panel 1

ax[0][0].text(0.02*0.2, 0.9*0.1, r'(a)')
ax[0][0].set_title(r'$N=10^4$, $Q=10^3$, $b=1$, $\mathrm{FNR}=\mathrm{FPR}=0$')

ax[0][0].plot(testing_replacement_false_IR[:,0]/Q, testing_replacement_false_IR[:,1], label = r'$I+R=200$')
ax[0][0].plot(testing_replacement_false_IR[:,0]/Q, testing_replacement_false_IR[:,2], label = r'$I+R=400$')
ax[0][0].plot(testing_replacement_false_IR[:,0]/Q, testing_replacement_false_IR[:,3], label = r'$I+R=600$')
ax[0][0].plot(testing_replacement_false_IR[:,0]/Q, testing_replacement_false_IR[:,4], label = r'$I+R=800$')
ax[0][0].plot(testing_replacement_false_IR[:,0]/Q, testing_replacement_false_IR[:,5], label = r'$I+R=1000$')

ax[0][0].plot(testing_replacement_true_IR[:,0]/Q, testing_replacement_true_IR[:,1], ls = '--', color = 'Grey')
ax[0][0].plot(testing_replacement_true_IR[:,0]/Q, testing_replacement_true_IR[:,2], ls = '--', color = 'Grey')
ax[0][0].plot(testing_replacement_true_IR[:,0]/Q, testing_replacement_true_IR[:,3], ls = '--', color = 'Grey')
ax[0][0].plot(testing_replacement_true_IR[:,0]/Q, testing_replacement_true_IR[:,4], ls = '--', color = 'Grey')
ax[0][0].plot(testing_replacement_true_IR[:,0]/Q, testing_replacement_true_IR[:,5], ls = '--', color = 'Grey')

ax[0][0].set_xlim(0,0.2)
ax[0][0].set_ylim(0,0.1)
ax[0][0].legend(loc = 1, frameon = False, fontsize = 6)

#%% panel 2

ax[0][1].text(0.02*0.2, 0.9*0.2, r'(b)')
ax[0][1].set_title(r'$S=9700$, $I=300$, $Q=10^3$, $\mathrm{FNR}=\mathrm{FPR}=0$')

ax[0][1].plot(testing_replacement_false_b[:,0]/Q, testing_replacement_false_b[:,1], label = r'$b=0.5$')
ax[0][1].plot(testing_replacement_false_b[:,0]/Q, testing_replacement_false_b[:,2], label = r'$b=1$')
ax[0][1].plot(testing_replacement_false_b[:,0]/Q, testing_replacement_false_b[:,3], label = r'$b=1.5$')
ax[0][1].plot(testing_replacement_false_b[:,0]/Q, testing_replacement_false_b[:,4], label = r'$b=2$')

ax[0][1].plot(testing_replacement_true_b[:,0]/Q, testing_replacement_true_b[:,1], ls = '--', color = 'Grey')
ax[0][1].plot(testing_replacement_true_b[:,0]/Q, testing_replacement_true_b[:,2], ls = '--', color = 'Grey')
ax[0][1].plot(testing_replacement_true_b[:,0]/Q, testing_replacement_true_b[:,3], ls = '--', color = 'Grey')
ax[0][1].plot(testing_replacement_true_b[:,0]/Q, testing_replacement_true_b[:,4], ls = '--', color = 'Grey')

ax[0][1].set_xlim(0,0.2)
ax[0][1].set_ylim(0,0.2)
ax[0][1].legend(loc = 1, frameon = False, fontsize = 6)

#%% panel 3

ax[1][0].text(0.02*0.05, 0.9*0.1, r'(c)')
ax[1][0].set_title(r'$S=9700$, $I=300$, $Q=10^3$, $b=1$, $\mathrm{FPR}=0$')

ax[1][0].plot(testing_replacement_false_FNR[:,0]/Q, testing_replacement_false_FNR[:,1], label = r'$\mathrm{FNR}=0$')
ax[1][0].plot(testing_replacement_false_FNR[:,0]/Q, testing_replacement_false_FNR[:,2], label = r'$\mathrm{FNR}=0.05$')
ax[1][0].plot(testing_replacement_false_FNR[:,0]/Q, testing_replacement_false_FNR[:,3], label = r'$\mathrm{FNR}=0.1$')
ax[1][0].plot(testing_replacement_false_FNR[:,0]/Q, testing_replacement_false_FNR[:,4], label = r'$\mathrm{FNR}=0.2$')

ax[1][0].plot(testing_replacement_true_FNR[:,0]/Q, testing_replacement_true_FNR[:,1], ls = '--', color = 'Grey')
ax[1][0].plot(testing_replacement_true_FNR[:,0]/Q, testing_replacement_true_FNR[:,2], ls = '--', color = 'Grey')
ax[1][0].plot(testing_replacement_true_FNR[:,0]/Q, testing_replacement_true_FNR[:,3], ls = '--', color = 'Grey')
ax[1][0].plot(testing_replacement_true_FNR[:,0]/Q, testing_replacement_true_FNR[:,4], ls = '--', color = 'Grey')

ax[1][0].set_xlim(0,0.05)
ax[1][0].set_ylim(0,0.1)
ax[1][0].legend(loc = 1, frameon = False, fontsize = 6)

#%% panel 4

ax[1][1].text(0.02*0.3, 0.9*0.1, r'(d)')
ax[1][1].set_title(r'$S=9700$, $I=300$, $Q=10^3$, $b=1$, $\mathrm{FNR}=0$')

ax[1][1].plot(testing_replacement_false_FPR[:,0]/Q, testing_replacement_false_FPR[:,1], label = r'$\mathrm{FPR}=0$')
ax[1][1].plot(testing_replacement_false_FPR[:,0]/Q, testing_replacement_false_FPR[:,2], label = r'$\mathrm{FPR}=0.01$')
ax[1][1].plot(testing_replacement_false_FPR[:,0]/Q, testing_replacement_false_FPR[:,3], label = r'$\mathrm{FPR}=0.05$')
ax[1][1].plot(testing_replacement_false_FPR[:,0]/Q, testing_replacement_false_FPR[:,4], label = r'$\mathrm{FPR}=0.1$')
ax[1][1].plot(testing_replacement_false_FPR[:,0]/Q, testing_replacement_false_FPR[:,5], label = r'$\mathrm{FPR}=0.2$')

ax[1][1].plot(testing_replacement_true_FPR[:,0]/Q, testing_replacement_true_FPR[:,1], ls = '--', color = 'Grey')
ax[1][1].plot(testing_replacement_true_FPR[:,0]/Q, testing_replacement_true_FPR[:,2], ls = '--', color = 'Grey')
ax[1][1].plot(testing_replacement_true_FPR[:,0]/Q, testing_replacement_true_FPR[:,3], ls = '--', color = 'Grey')
ax[1][1].plot(testing_replacement_true_FPR[:,0]/Q, testing_replacement_true_FPR[:,4], ls = '--', color = 'Grey')
ax[1][1].plot(testing_replacement_true_FPR[:,0]/Q, testing_replacement_true_FPR[:,5], ls = '--', color = 'Grey')

ax[1][1].set_xlim(0,0.3)
ax[1][1].set_ylim(0,0.1)
ax[1][1].legend(loc = 1, frameon = False, fontsize = 6)

ax[1][0].set_xlabel(r'$\tilde{Q}^+/Q$')
ax[1][1].set_xlabel(r'$\tilde{Q}^+/Q$')
ax[0][0].set_ylabel(r'$P_{\mathrm{TOT}}(\tilde{Q}^+|\theta)$')
ax[1][0].set_ylabel(r'$P_{\mathrm{TOT}}(\tilde{Q}^+|\theta)$')

plt.tight_layout()
plt.savefig('testing.png', dpi = 300)

plt.show()
