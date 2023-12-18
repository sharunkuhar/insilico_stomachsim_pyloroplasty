import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as font_manager
mpl.rcParams.update(mpl.rcParamsDefault)


def get_coords_of_a_and_d():
    fname = f'../data/hlty/clinedata/clinedat_0.csv'
    print(f'Reading {fname}')
    data = np.genfromtxt(fname, delimiter=',', skip_header=1)
    s_i, x_i, y_i, z_i = data[:, 5], data[:, 6], data[:, 7], data[:, 8]
    if np.all(np.diff(s_i) > 0):
        x_a = np.interp(s_antrum, s_i, x_i)
        x_d = np.interp(s_duodenum, s_i, x_i)
        y_a = np.interp(s_antrum, s_i, y_i)
        y_d = np.interp(s_duodenum, s_i, y_i)
        z_a = np.interp(s_antrum, s_i, z_i)
        z_d = np.interp(s_duodenum, s_i, z_i)

        print(f'Antrum: ({x_a:.2f}, {y_a:.2f}, {z_a:.2f})')
        print(f'Duodenum: ({x_d:.2f}, {y_d:.2f}, {z_d:.2f})')
    else:
        print('Bad data: s is not monotonically increasing')


# ----------------------------------------------------
s_pylorus = 21.7
l_pressure = 2  # cm

s_antrum = s_pylorus - l_pressure/2
s_duodenum = s_pylorus + l_pressure/2

get_coords_of_a_and_d()
