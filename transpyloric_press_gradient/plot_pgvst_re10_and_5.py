import numpy as np
import matplotlib.pyplot as plt


def get_transpyloric_pg(case):
    tp = 20  # sec
    dt = 0.005
    dump_interval = 500

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
    print(f'Assuming average pressure-gradient over the open duration is the same as that at t={t[1]:f}')
    return dp[1]


# ----------------------------------------------------
s_pylorus = 21.7
l_pressure = 2  # cm
pressure_scaling = 1000 * 0.01 ** 2 * 0.00750062  # (rho*U^2 Pa) * 0.00750062 mmHg/Pa

s_antrum = s_pylorus - l_pressure / 2
s_duodenum = s_pylorus + l_pressure / 2

t_re10, dp_re10 = get_transpyloric_pg('re10_hlty')
t_re5, dp_re5 = get_transpyloric_pg('re5_hlty')

dpbyL_re10 = get_dpbar(t_re10, dp_re10) / l_pressure
dpbyL_re5 = get_dpbar(t_re5, dp_re5) / l_pressure
print('Transpyloric Pressure Gradient:')
print(f'\t 10 mPa s: {dpbyL_re10:.2f} mm Hg/cm')
print(f'\t 20 mPa s: {dpbyL_re5:.2f} mm Hg/cm')
