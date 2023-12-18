import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def getdata(fname):
    file = pd.read_csv(fname, delim_whitespace=True, header=None)
    data = np.asarray(file)
    return data


def process_data(fname):
    # read data containing t, p_y2, p_z1, v_y2, v_z1
    data = getdata(fname)

    # only need time and v_z1
    t_full = data[:, 0]
    # v_out_full = data[:, 4]

    # only need the last TP sec of t and v_out
    t_end = t_full[-1]
    t_start = t_end - TP
    print(f'Reading {fname} from {t_start:.0f} to {t_end:.0f} sec.')
    idx = (np.abs(t_full - t_start)).argmin()
    t = data[idx:, 0] - data[idx, 0]
    v_out = data[idx:, 4] * VELOCITY_SCALING  # cm/s

    # calculate outflow rate
    csa = np.pi * (DUODENUM_DIA / 2) ** 2  # cm^2
    q_out = -v_out * csa

    return t, q_out


def get_er(data):
    return 3 * np.trapz(data[1], dx=data[0][1] - data[0][0])


def get_bile_reflux(data):
    q_out = data[1].copy()
    q_out[q_out > 0] = 0
    return -3 * np.trapz(q_out, dx=data[0][1] - data[0][0])


# --------------------------------------------------------------------------
# Global Variables
DUODENUM_DIA = 2.5353  # cm
VELOCITY_SCALING = 1  # cm/s
TP = 20  # seconds

t_qout_610 = process_data('ioflux.dat')
t_qout_600 = process_data('../run2_p600/ioflux.dat')
er_610 = get_er(t_qout_610)
er_600 = get_er(t_qout_600)
print(f'\t p=600 ER={er_600:.2f} mL/min')
print(f'\t p=610 ER={er_610:.2f} mL/min')

fig, ax = plt.subplots(1, 1, figsize=(6, 4))
ax.plot(t_qout_610[0], t_qout_610[1], label='p=610')
ax.plot(t_qout_600[0], t_qout_600[1], label='p=600')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Outflow Rate (mL/s)')
ax.legend()
plt.tight_layout()
fig.savefig('compare_600_610.png', dpi=300)
plt.close(fig)
