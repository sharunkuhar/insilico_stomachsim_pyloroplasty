import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# ===================================================
import matplotlib.font_manager as font_manager

# Plotting
plt.style.use('myplot.mplstyle')
mycols = ['#377eb8', '#e41a1c', '#4daf4a', '#984ea3', '#ff7f00']
# set the font to roboto
# -------------------------------------------------------------------------
font_path = 'C:/Users/sharu/Documents/myfonts/Roboto-Regular.ttf'
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = prop.get_name()


# --------------------------------------------------------------------------------------------------


def fx(x, a, b):
    return a / (np.exp(b * x) - 1)


def gx(x, a, b):
    return a * x + b


def hx(x, a):
    return a * x


# ---

pscale = 1000 * 0.01 ** 2 * 0.00750062  # (rho*U^2 Pa) * 0.00750062 mmHg/Pa
p0 = np.asarray([650, 300, 165, 50]) * pscale
re = np.asarray([2, 5, 10, 100])

# fit the (re, p0) data to the curve fx
popt, pcov = curve_fit(fx, re, p0)
xfill = np.linspace(1, 100, 100)
yfill = fx(xfill, *popt)
fig, ax = plt.subplots(figsize=(3.0, 3.0))
ax.plot(re, p0, 'ko', markersize=5, markerfacecolor='k')
ax.plot(xfill, yfill)
ax.set_xlabel(r'$Re$')
ax.set_ylabel(r'$p_o$ (mm Hg)')
eqn = r'$p_o=\frac{a}{e^{bx}-1}$'
ax.text(2, 0.75, eqn, color='C0')
plt.savefig('re_vs_p0.png')
plt.show()
plt.close(fig)

# fit the (mu, p0) data to the curve hx or gx
mu = (1000 * 0.01 * 0.01 / re) * 1000  # mPa s
popt, pcov = curve_fit(gx, mu, p0)
# popt, pcov = curve_fit(hx, mu, p0)
xfill = np.linspace(1, 60, 1000)
yfill = gx(xfill, *popt)
fig, ax = plt.subplots(figsize=(3.0, 3.0))
ax.plot(mu, p0, 'ko', markersize=5, markerfacecolor='k')
ax.plot(xfill, yfill)
ax.set_xlabel(r'$\mu$ (mPa s)')
ax.set_ylabel(r'$p_o$ (mm Hg)')
plt.savefig('mu_vs_p0.png')
plt.show()
plt.close(fig)
