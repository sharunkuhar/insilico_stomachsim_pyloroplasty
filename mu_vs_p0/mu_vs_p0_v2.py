import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# ===================================================

# Plotting
plt.style.use('halfcol')
mycols = ['#377eb8', '#e41a1c', '#4daf4a', '#984ea3', '#ff7f00']

# --------------------------------------------------------------------------------------------------


def gx(x, a, b):
    return a * x + b


def hx(x, a):
    return a * x


# ---

pscale = 1000 * 0.01 ** 2 * 0.00750062  # (rho*U^2 Pa) * 0.00750062 mmHg/Pa
p0 = np.asarray([650, 300, 165, 50]) * pscale
tppg = np.asarray([0.25, 0.12, 0.07, 0.02])  # transpyloric-pressure-gradient (mmHg/cm)
                                            # find using the scripts in transpyloric_press_gradient folder

re = np.asarray([2, 5, 10, 100])

mu = (1000 * 0.01 * 0.01 / re) * 1000  # mPa s


popt, _ = curve_fit(gx, mu, tppg)
x_tppg = np.linspace(1, 60, 1000)
y_tppg = gx(x_tppg, *popt)

popt, _ = curve_fit(gx, mu, p0)
x_p0 = np.linspace(1, 60, 1000)
y_p0 = gx(x_p0, *popt)

fig, ax = plt.subplots(figsize=(3.0, 3.0))
ax.plot(mu, tppg, 'ks', markersize=7, markerfacecolor='none')
ax.plot(x_tppg, y_tppg, 'k--')
ax.set_xlabel(r'$\mu$ (mPa s)')
ax.set_ylabel(r'$\Delta p/L$ (mm Hg)')
# ax2 = ax.twinx()
# ax2.plot(mu, p0, 'o', markersize=5, markerfacecolor='none')
# ax2.set_ylabel(r'$p_0$ (mm Hg)')
# ax2.plot(x_p0, y_p0, '--')

plt.savefig('mu_vs_tppg.png')
plt.savefig('mu_vs_tppg.eps')
plt.close(fig)
