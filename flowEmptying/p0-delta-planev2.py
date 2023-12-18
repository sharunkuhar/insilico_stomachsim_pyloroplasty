from plot_qvst import *
import matplotlib.patches as patches


def get_er(data):
    return 3 * np.trapz(data[1], dx=data[0][1] - data[0][0])


def get_bile_reflux(data):
    q_out = data[1].copy()
    q_out[q_out > 0] = 0
    return -3 * np.trapz(q_out, dx=data[0][1] - data[0][0])


def gen_patch(x, y, er, pos='d'):
    fac = fig.get_figwidth() / fig.get_figheight()
    x_ax, y_ax = (x-xll)/(xul-xll), (y-yll)/(yul-yll)
    cmap = plt.get_cmap('Blues')
    col = cmap((er - val_min)/(val_max - val_min))
    if er>0 and er/val_max>0.01:
        circ = patches.Ellipse((x_ax, y_ax), width=scale*er, height=fac*scale*er, transform=ax.transAxes, facecolor=col,
                           edgecolor='k')
    else:
        circ = patches.Ellipse((x_ax, y_ax), width=0.01, height=0.01, transform=ax.transAxes, facecolor=col,
                           edgecolor='k')
    if pos == 'd':
        ax.text(x_ax, y_ax-fac*scale*abs(er)*(er>0)/2-gap, f'{er:.{prec}f}', transform=ax.transAxes, ha='center', va='top')
    else:
        ax.text(x_ax, y_ax+fac*scale*abs(er)*(er>0)/2+gap, f'{er:.{prec}f}', transform=ax.transAxes, ha='center', va='bottom')
    return circ


# ===================================================

er_hlty = get_er(hlty)
er_p0 = get_er(gpp0)
er_d2 = get_er(gpd2)
er_d2p0 = get_er(gpd2p0)
er_d3p25 = get_er(gpd3p25)

ref_hlty = get_bile_reflux(hlty)
ref_p0 = get_bile_reflux(pylD4p0)
ref_d2 = get_bile_reflux(pylD4d2)
ref_d2p0 = get_bile_reflux(pylD4d2p0)
ref_d3p25 = get_bile_reflux(pylD4d3p25)

imp_p0 = 100*(get_er(pylD4p0)-er_p0)/er_p0
imp_d2 = 100*(get_er(pylD4d2)-er_d2)/er_d2
imp_d2p0 = 100*(get_er(pylD4d2p0)-er_d2p0)/er_d2p0
imp_d3p25 = 100*(get_er(pylD4d3p25)-er_d3p25)/er_d3p25

post_er_p0 = get_er(pylD4p0)
post_er_d2 = get_er(pylD4d2)
post_er_d2p0 = get_er(pylD4d2p0)
post_er_d3p25 = get_er(pylD4d3p25)

# My config
plt.style.use('halfcol')

# pscale = 1  # use this to plot wrt non-dim pressure
pscale = 1000*0.01**2*0.00750062  # (rho*U^2 Pa) * 0.00750062 mmHg/Pa
xll, xul = 0.15, 0.45
yll, yul = -15*pscale, 65*pscale
figsize = (2.2, 2.2)

# Plot emptying rate
val_min = min(er_hlty, er_p0, er_d2, er_d2p0, er_d3p25)
val_max = max(er_hlty, er_p0, er_d2, er_d2p0, er_d3p25)
scale = 0.06
prec = 1
gap = 0.025
fig, ax = plt.subplots(figsize=figsize)
ax.set_xlim(xll, xul)
ax.set_ylim(yll, yul)
ax.add_artist(gen_patch(0.2, 0*pscale, er_d2p0))
ax.add_artist(gen_patch(0.4, 0*pscale, er_p0))
ax.add_artist(gen_patch(0.2, 50*pscale, er_d2))
ax.add_artist(gen_patch(0.4, 50*pscale, er_hlty))
ax.add_artist(gen_patch(0.3, 25*pscale, er_d3p25))
ax.set_xlabel(r'$\delta$')
ax.set_ylabel(r'$p_o$ (mm Hg)')
# ax.set_title('Emptying rate (mL/min)')
ax.grid(False)
plt.savefig('p0-delta_er.png')
plt.savefig('p0-delta_er.eps')
plt.close()

# Plot reflux
val_min = min(ref_hlty, ref_p0, ref_d2, ref_d2p0, ref_d3p25)
val_max = max(ref_hlty, ref_p0, ref_d2, ref_d2p0, ref_d3p25)
scale = 0.03
prec = 1
gap = 0.025
fig, ax = plt.subplots(figsize=figsize)
ax.set_xlim(xll, xul)
ax.set_ylim(yll, yul)
ax.add_artist(gen_patch(0.2, 0*pscale, ref_d2p0, pos='u'))
ax.add_artist(gen_patch(0.4, 0*pscale, ref_p0, pos='u'))
ax.add_artist(gen_patch(0.2, 50*pscale, ref_d2, pos='u'))
# ax.add_artist(gen_patch(0.4, 50*pscale, ref_hlty))
ax.add_artist(gen_patch(0.3, 25*pscale, ref_d3p25, pos='u'))
ax.set_xlabel(r'$\delta$')
ax.set_ylabel(r'$p_o$ (mm Hg)')
# ax.set_title('Reflux rate (mL/min)')
ax.grid(False)
plt.savefig('p0-delta_ref.png')
plt.savefig('p0-delta_ref.eps')
plt.close()

# Plot % improvement
val_min = min(imp_p0, imp_d2, imp_d2p0, imp_d3p25)
val_max = max(imp_p0, imp_d2, imp_d2p0, imp_d3p25)
scale = 0.002
prec = 0
gap = 0.025
fig, ax = plt.subplots(figsize=figsize)
ax.set_xlim(xll, xul)
ax.set_ylim(yll, yul)
ax.add_artist(gen_patch(0.2, 0*pscale, imp_d2p0))
ax.add_artist(gen_patch(0.4, 0*pscale, imp_p0))
ax.add_artist(gen_patch(0.2, 50*pscale, imp_d2))
ax.add_artist(gen_patch(0.3, 25*pscale, imp_d3p25))
ax.set_xlabel(r'$\delta$')
ax.set_ylabel(r'$p_o$ (mm Hg)')
# ax.set_title('% Post-op. Improvement')
ax.grid(False)
plt.savefig('p0-delta_imp.png')
plt.savefig('p0-delta_imp.eps')
plt.close()


# Plot post-op. emptying rate
val_min = min(post_er_p0, post_er_d2, post_er_d2p0, post_er_d3p25)
val_max = max(post_er_p0, post_er_d2, post_er_d2p0, post_er_d3p25)
scale = 0.03
prec = 1
gap = 0.025
fig, ax = plt.subplots(figsize=figsize)
ax.set_xlim(xll, xul)
ax.set_ylim(yll, yul)
ax.add_artist(gen_patch(0.4, 0*pscale,  post_er_p0))
ax.add_artist(gen_patch(0.2, 50*pscale, post_er_d2))
ax.add_artist(gen_patch(0.3, 25*pscale, post_er_d3p25))
prec=2
ax.add_artist(gen_patch(0.2, 0*pscale,  post_er_d2p0))
ax.set_xlabel(r'$\delta$')
ax.set_ylabel(r'$p_o$ (mm Hg)')
# ax.set_title('% Post-op. Improvement')
ax.grid(False)
plt.savefig('p0-delta_poster.png')
plt.savefig('p0-delta_poster.eps')
plt.close()


# er_hlty = get_er(hlty)
# er_p0 = [get_er(pylD2p0), get_er(pylD3p0), get_er(pylD4p0)]
# er_d2 = [get_er(pylD2d2), get_er(pylD3d2), get_er(pylD4d2)]
# er_d2p0 = [get_er(pylD3d2p0), get_er(pylD4d2p0)]
# er_d3p25 = [get_er(pylD3d3p25), get_er(pylD4d3p25)]
#
# reflux_p0 = [get_bile_reflux(pylD2p0), get_bile_reflux(pylD3p0), get_bile_reflux(pylD4p0)]
# reflux_d2 = [get_bile_reflux(pylD2d2), get_bile_reflux(pylD3d2), get_bile_reflux(pylD4d2)]
# reflux_d2p0 = [get_bile_reflux(pylD3d2p0), get_bile_reflux(pylD4d2p0)]
# reflux_d3p25 = [get_bile_reflux(pylD3d3p25), get_bile_reflux(pylD4d3p25)]
#
# mycols = ['#377eb8', '#e41a1c', '#4daf4a', '#984ea3', '#ff7f00']
# fig, ax = plt.subplots()
# # ax.plot([2], er_hlty, 'o')
# ax.plot([2, 3, 4], er_d2, 's-', label='(0.2, 50)')
# ax.plot([3, 4], er_d3p25, 's-', label='(0.3, 25)')
# ax.plot([2, 3, 4], er_p0, 's-', label='(0.4, 0)')
# ax.plot([3, 4], er_d2p0, 's-', label='(0.2, 0)')
# ax.plot([2], get_er(gpd2), 'o', color=mycols[1])
# ax.plot([2], get_er(gpd3p25), 'o', color=mycols[2])
# ax.plot([2], get_er(gpp0), 'o', color=mycols[3])
# ax.plot([2], get_er(gpd2p0), 'o', color=mycols[4])
# plt.title('Emptying Rate')
# plt.legend(title=r'($\delta$, $p_0$)', loc='center left', bbox_to_anchor=(1, 0.5))
# ax.set_xlabel('Pyloric Orifice Diameter (mm)')
# ax.set_ylabel('Emptying Rate (mL/min)')
# plt.savefig('postop_er.png')
# plt.close()
#
# print('Total emptying rate (mL/min):')
# v0 = get_er(hlty)
# print(f'\thlty_er={get_er(hlty):.3f}, ({100 * get_er(hlty) / v0: .0f} %)')
# print(f'\tgpd2_er={get_er(gpd2):.3f}, ({100 * get_er(gpd2) / v0: .0f} %)')
# print(f'\tpylD2d2_er={get_er(pylD2d2):.3f}, ({100 * get_er(pylD2d2) / v0: .0f} %)')
# print(f'\tpylD3d2_er={get_er(pylD3d2):.3f}, ({100 * get_er(pylD3d2) / v0: .0f} %)')
# print(f'\tpylD4d2_er={get_er(pylD4d2):.3f}, ({100 * get_er(pylD4d2) / v0: .0f} %)')
# print(f'\tgpp0_er={get_er(gpp0):.3f}, ({100 * get_er(gpp0) / v0: .0f} %)')
# print(f'\tpylD2p0_er={get_er(pylD2p0):.3f}, ({100 * get_er(pylD2p0) / v0: .0f} %)')
# print(f'\tpylD3p0_er={get_er(pylD3p0):.3f}, ({100 * get_er(pylD3p0) / v0: .0f} %)')
# # print(f'\tpylD4p0_er={get_er(pylD4p0):.3f}, ({100*get_er(pylD4p0)/v0: .0f} %)')
# print('Total bile reflux (mL/min):')
# print(f'\thlty:{get_bile_reflux(hlty):.3f}')
# print(f'\tgpp0:{get_bile_reflux(gpp0):.3f}')
# print(f'\tgpd2:{get_bile_reflux(gpd2):.3f}')
# print(f'\tpylD2d2:{get_bile_reflux(pylD2d2):.3f}')
# print(f'\tpylD3d2:{get_bile_reflux(pylD3d2):.3f}')
# print(f'\tpylD4d2:{get_bile_reflux(pylD4d2):.3f}')
