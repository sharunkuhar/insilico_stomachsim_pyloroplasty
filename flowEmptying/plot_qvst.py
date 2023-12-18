import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.font_manager as font_manager

mpl.rcParams.update(mpl.rcParamsDefault)


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
    print(f'Reading {fname} from {t_start} to {t_end} sec.')
    idx = (np.abs(t_full - t_start)).argmin()
    t = data[idx:, 0] - data[idx, 0]
    v_out = data[idx:, 4] * VELOCITY_SCALING  # cm/s

    # calculate outflow rate
    csa = np.pi * (DUODENUM_DIA / 2) ** 2  # cm^2
    q_out = -v_out * csa

    return t, q_out


# --------------------------------------------------------------------------
# Global Variables
DUODENUM_DIA = 2.5353  # cm
VELOCITY_SCALING = 1  # cm/s
TP = 20  # seconds

hlty = process_data('../data/hlty/inputs/run3_rec12k-16k/ioflux.dat')
gpd2 = process_data('../data/gpd2/inputs/run3_rec12k-16k/ioflux.dat')
pylD2d2 = process_data('../data/pylD2d2/inputs/run1_0-8k/ioflux.dat')
pylD3d2 = process_data('../data/pylD3d2/inputs/run1_0-8k/ioflux.dat')
pylD4d2 = process_data('../data/pylD4d2/inputs/run1_0-8k/ioflux.dat')

gpp0 = process_data('../data/gpp0/inputs/run2_rec8k-12k/ioflux.dat')
pylD2p0 = process_data('../data/pylD2p0/inputs/run1_0-8k/ioflux.dat')
pylD3p0 = process_data('../data/pylD3p0/inputs/run1_0-8k/ioflux.dat')
pylD4p0 = process_data('../data/pylD4p0/inputs/run1_0-8k/ioflux.dat')

gpd2p0 = process_data('../data/gpd2p0/inputs/run1_0-8k/ioflux.dat')
pylD3d2p0 = process_data('../data/pylD3d2p0/inputs/run1_0-8k/ioflux.dat')
pylD4d2p0 = process_data('../data/pylD4d2p0/inputs/run1_0-8k/ioflux.dat')

gpd3p25 = process_data('../data/gpd3p25/inputs/run1_0-8k/ioflux.dat')
pylD3d3p25 = process_data('../data/pylD3d3p25/inputs/run1_0-8k/ioflux.dat')
pylD4d3p25 = process_data('../data/pylD4d3p25/inputs/run1_0-8k/ioflux.dat')

# ===================================================
# Plotting
# plt.style.use('myplot.mplstyle')
# set the font to roboto
# -------------------------------------------------------------------------
# font_path = 'C:/Users/sharu/Documents/myfonts/Roboto-Regular.ttf'
# font_manager.fontManager.addfont(font_path)
# prop = font_manager.FontProperties(fname=font_path)
# plt.rcParams['font.family'] = 'sans-serif'
# plt.rcParams['font.sans-serif'] = prop.get_name()
# plt.rcParams['lines.linewidth'] = 1.0
# --------------------------------------------------------------------------------------------------
plt.style.use('halfcol')
mycols = ['#377eb8', '#e41a1c', '#4daf4a', '#984ea3', '#ff7f00']

if __name__ == '__main__':
    nskip = 20

    # Pre-op cases
    fig, ax = plt.subplots(figsize=(5.0, 2.8), tight_layout=True)

    ax.plot(gpd2[0][::nskip], gpd2[1][::nskip], label='AH (Pre-op.)', color=mycols[1])
    ax.plot(pylD4d2[0][::nskip], pylD4d2[1][::nskip], '--', label='AH (Post-op.)', color=mycols[1])
    # ax.plot(gpd3p25[0][::nskip], gpd3p25[1][::nskip], ':', label='(0.3, 25)')
    ax.plot(gpp0[0][::nskip], gpp0[1][::nskip], label='DT (Pre-op.)', color=mycols[2])
    ax.plot(pylD4p0[0][::nskip], pylD4p0[1][::nskip], '--', label='DT (Post-op.)', color=mycols[2])
    # ax.plot(gpd2p0[0][::nskip], gpd2p0[1][::nskip], label='AH + PA')
    ax.plot(hlty[0][::nskip], hlty[1][::nskip], label='Healthy', color='k', lw=1.1)

    ax.set_xlim(0, 20)
    ax.set_ylabel('Pylorus Flowrate (mL/s)')
    ax.set_xlabel('t (sec)')
    # ax.legend(title=r'$(\delta, p_0)$')  # , bbox_to_anchor=(1.05, 0.5), loc='center left')
    ax.legend(bbox_to_anchor=(1.05, 0.5), loc='center left')
    ax.grid(True)

    fig.savefig('qvst.png')
    fig.savefig('qvst.eps')
    plt.close(fig)

    # Post-op cases : d2
    fig, ax = plt.subplots()
    
    ax.plot(hlty[0][::nskip], hlty[1][::nskip], 'k-', label='Healthy')
    ax.plot(gpd2[0][::nskip], gpd2[1][::nskip], label='Pre-op.')
    ax.plot(pylD2d2[0][::nskip], pylD2d2[1][::nskip], '--', label='Post-op.(2 mm)', color=mycols[1])
    ax.plot(pylD3d2[0][::nskip], pylD3d2[1][::nskip], ':', label='Post-op.(3 mm)', color=mycols[2])
    ax.plot(pylD4d2[0][::nskip], pylD4d2[1][::nskip], '-.', label='Post-op.(4 mm)', color=mycols[3])
    
    ax.set_xlim(0, 20)
    ax.set_ylim(-0.6, 0.4)
    ax.set_xlabel('t (sec)')
    # ax.set_ylabel(r'$\bar{Q}_{out}$ (mL/s)')
    ax.set_ylabel('Pylorus Flowrate (mL/s)')
    # ax.legend(bbox_to_anchor=(1.05, 0.5), loc='center left')
    
    fig.savefig('qvst_d2.png')
    fig.savefig('qvst_d2.eps')
    plt.close(fig)
    
    # Post-op cases : p0
    fig, ax = plt.subplots()
    
    ax.plot(hlty[0][::nskip], hlty[1][::nskip], 'k-', label='Healthy')
    ax.plot(gpp0[0][::nskip], gpp0[1][::nskip], label='Pre-op.', color=mycols[0])
    ax.plot(pylD2p0[0][::nskip], pylD2p0[1][::nskip], '--', label='Post-op. (2 mm)', color=mycols[1])
    ax.plot(pylD3p0[0][::nskip], pylD3p0[1][::nskip], ':', label='Post-op. (3 mm)', color=mycols[2])
    ax.plot(pylD4p0[0][::nskip], pylD4p0[1][::nskip], '-.', label='Post-op. (4 mm)', color=mycols[3])
    
    ax.set_xlim(0, 20)
    ax.set_ylim(-0.6, 0.4)
    ax.set_xlabel('t (sec)')
    # ax.set_ylabel(r'$\bar{Q}_{out}$ (mL/s)')
    ax.set_ylabel('Pylorus Flowrate (mL/s)')
    ax.legend(bbox_to_anchor=(1.05, 0.5), loc='center left')
    
    fig.savefig('qvst_p0.png')
    fig.savefig('qvst_p0.eps')
    plt.close(fig)
    
    # Post-op cases : d2 + p0
    
    fig, ax = plt.subplots()
    
    ax.plot(gpd2p0[0][::nskip], gpd2p0[1][::nskip], label='Pre-op.', color=mycols[0])
    ax.plot(pylD3d2p0[0][::nskip], pylD3d2p0[1][::nskip], ':', label='3 mm', color=mycols[2])
    ax.plot(pylD4d2p0[0][::nskip], pylD4d2p0[1][::nskip], '-.', label='4 mm', color=mycols[3])
    
    ax.set_xlim(0, 20)
    ax.set_ylim(-0.6, 0.4)
    ax.set_xlabel('t (sec)')
    ax.set_ylabel(r'$\bar{Q}_{out}$ (mL/s)')
    ax.legend(bbox_to_anchor=(1.05, 0.5), loc='center left')
    
    fig.savefig('qvst_d2p0.png')
    plt.close(fig)
    
    # Post-op cases : d3 + p25
    
    fig, ax = plt.subplots()
    
    ax.plot(gpd3p25[0][::nskip], gpd3p25[1][::nskip], label='Pre-op.', color=mycols[0])
    ax.plot(pylD3d3p25[0][::nskip], pylD3d3p25[1][::nskip], ':', label='3 mm', color=mycols[2])
    ax.plot(pylD4d3p25[0][::nskip], pylD4d3p25[1][::nskip], '-.', label='4 mm', color=mycols[3])
    
    ax.set_xlim(0, 20)
    ax.set_ylim(-0.6, 0.4)
    ax.set_xlabel('t (sec)')
    ax.set_ylabel(r'$\bar{Q}_{out}$ (mL/s)')
    ax.legend(bbox_to_anchor=(1.05, 0.5), loc='center left')
    
    fig.savefig('qvst_d3p25.png')
    plt.close(fig)
