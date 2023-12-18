import numpy as np
import matplotlib.pyplot as plt


def get_transpyloric_pg(case):
    tp = 20  # sec
    dt = 0.005
    dump_interval = 50

    ndump = round((tp / dt)) // dump_interval

    t_out, dp_out = [], []
    for i in range(ndump):
        time = (i + 1) * dt * dump_interval
        t_out.append(time)

        fname = f'../data/{case}/clinedata/clinedat_{i}.csv'
        print(f'\t Reading {fname}')
        data = np.genfromtxt(fname, delimiter=',', skip_header=1)
        s_i, p_i = data[:, 5], data[:, 0]
        if np.all(np.diff(s_i) > 0):
            p_a = np.interp(s_antrum, s_i, p_i)
            p_d = np.interp(s_duodenum, s_i, p_i)
            dp = p_a - p_d
            dp_out.append(dp * pressure_scaling)
        else:
            print('Bad data: s is not monotonically increasing')

    return t_out, dp_out


def get_dpbar(t, dp):
    t_open = 20 * (0.01 + 0.09)
    t_close = 20 * (0.01 + 0.35 - 0.09)

    t_open_idx = np.searchsorted(t, t_open)
    t_close_idx = np.searchsorted(t, t_close)

    # find average dp between t_open and t_close
    dpbar = np.mean(dp[t_open_idx:t_close_idx]) 

    print(f'\t\t Average value between {t_open} and {t_close} is {dpbar:.2f}')
    return dpbar


# ----------------------------------------------------
s_pylorus = 21.7
l_pressure = 2  # cm
pressure_scaling = 1000 * 0.01 ** 2 * 0.00750062  # (rho*U^2 Pa) * 0.00750062 mmHg/Pa

s_antrum = s_pylorus - l_pressure / 2
s_duodenum = s_pylorus + l_pressure / 2

t_hlty, dp_hlty = get_transpyloric_pg('hlty')
t_re2hlty, dp_re2hlty = get_transpyloric_pg('re2_hlty')

dpbyL_hlty = get_dpbar(t_hlty, dp_hlty) / l_pressure
dpbyL_re2hlty = get_dpbar(t_re2hlty, dp_re2hlty) / l_pressure
print('Transpyloric Pressure Gradient:')
print(f'\t 1 mPa s: {dpbyL_hlty:.2f} mm Hg/cm')
print(f'\t 50 mPa s: {dpbyL_re2hlty:.2f} mm Hg/cm')

# Plot
plt.style.use('halfcol')
fig, ax = plt.subplots()
ax.plot(t_hlty, dp_hlty, label='1 mPa s')
ax.plot(t_re2hlty, dp_re2hlty, label='50 mPa s')
ax.set_xlim(0, 20)
ax.set_ylabel(r'$p_A - p_D$ (mm Hg)')
ax.set_xlabel('t (sec)')
ax.legend()

fig.savefig('dpvst.png')
fig.savefig('dpvst.eps')
plt.show()
plt.close(fig)
