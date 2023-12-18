from plot_qvst import *


def get_er(data):
    return 3 * np.trapz(data[1], dx=data[0][1] - data[0][0])


def get_bile_reflux(data):
    q_out = data[1].copy()
    q_out[q_out > 0] = 0
    return -3 * np.trapz(q_out, dx=data[0][1] - data[0][0])


def get_positive_flux(data):
    q_out = data[1].copy()
    q_out[q_out < 0] = 0
    return 3 * np.trapz(q_out, dx=data[0][1] - data[0][0])


er_hlty = get_er(hlty)
er_gpd2 = get_er(gpd2)
er_pyld2 = [get_er(pylD2d2), get_er(pylD3d2), get_er(pylD4d2)]
print(er_pyld2/er_gpd2*100)

er_gpp0 = get_er(gpp0)
er_pyld2p0 = [get_er(pylD2p0), get_er(pylD3p0), get_er(pylD4p0)]
print(er_pyld2p0/er_gpp0*100)

ref_hlty = get_bile_reflux(hlty)
ref_gpd2 = 0# get_bile_reflux(gpd2)
ref_pyld2 = [get_bile_reflux(pylD2d2), get_bile_reflux(pylD3d2), get_bile_reflux(pylD4d2)]
print(ref_pyld2)

ref_gpp0 = 0# get_bile_reflux(gpp0)
ref_pylp0 = [get_bile_reflux(pylD2p0), get_bile_reflux(pylD3p0), get_bile_reflux(pylD4p0)]
print(ref_pylp0)

pos_hlty = get_positive_flux(hlty)
pos_gpd2 = get_positive_flux(gpd2)
pos_pyld2 = [get_positive_flux(pylD2d2), get_positive_flux(pylD3d2), get_positive_flux(pylD4d2)]
print(pos_pyld2)

pos_gpp0 = get_positive_flux(gpp0)
pos_pylp0 = [get_positive_flux(pylD2p0), get_positive_flux(pylD3p0), get_positive_flux(pylD4p0)]
print(pos_pylp0)

fig, axs = plt.subplots(1,3, figsize=(6.4, 2.5), tight_layout=True, sharey=True)
# ax.plot(2, er_hlty, 'o')
ax = axs[2]
ax.plot(2, er_gpd2, 'o', markersize=6, label='AH, Pre-op.', color=mycols[0])
ax.plot([2, 3, 4], er_pyld2, 's', linestyle='--', markersize=6, label='AH, Post-op.', color=mycols[0])
ax.plot(2, er_gpp0, 'o', markersize=6, label='DT, Pre-op.', color=mycols[2], markerfacecolor='none')
ax.plot([2, 3, 4], er_pyld2p0, 's', linestyle=':', label='DT, Post-op.', markersize=6, color=mycols[2], markerfacecolor='none')
# ax.set_ylim(2, 10)
ax.set_ylabel('Net Emptying Rate (mL/min)')
ax.set_xlabel('Orifice Dia. (mm)')
# ax.legend(bbox_to_anchor=(1.05, 0.5), loc='center left')

ax = axs[1]
ax.plot(2, ref_gpd2, 'o', markersize=6, label='AH, Pre-op.', color=mycols[0])
ax.plot([2, 3, 4], ref_pyld2, 's', linestyle='--', markersize=6, label='AH, Post-op.', color=mycols[0])
ax.plot(2, ref_gpp0, 'o', markersize=6, label='DT, Pre-op.', color=mycols[2], markerfacecolor='none')
ax.plot([2, 3, 4], ref_pylp0, 's', linestyle=':', markersize=6, label='DT, Post-op.', color=mycols[2], markerfacecolor='none')
# ax.set_ylim(0, 4)
ax.set_ylabel('Negative Flux (mL/min)')
ax.set_xlabel('Orifice Dia. (mm)')

ax = axs[0]
ax.plot(2, pos_gpd2, 'o', markersize=6, label='AH, Pre-op.', color=mycols[0])
ax.plot([2, 3, 4], pos_pyld2, 's', linestyle='--', markersize=6, label='AH, Post-op.', color=mycols[0])
ax.plot(2, pos_gpp0, 'o', markersize=6, label='DT, Pre-op.', color=mycols[2], markerfacecolor='none')
ax.plot([2, 3, 4], pos_pylp0, 's', linestyle=':', markersize=6, label='DT, Post-op.', color=mycols[2], markerfacecolor='none')
# ax.set_ylim(0, 4)
ax.set_ylabel('Positive Flux (mL/min)')
ax.set_xlabel('Orifice Dia. (mm)')
ax.legend()

fig.savefig('postop_er.png')
fig.savefig('postop_er.eps')