"""
    Copyright (C) 2023 Khandaker Foysal Haque
    contact: haque.k@northeastern.edu
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gridspec

V_k = np.load("vmatrix/V_ax_su_4x2_160.npy")
V_k = V_k[:4000, :, :]
V_k = np.moveaxis(V_k, [0, 3, 1, 2], [0, 1, 2, 3])

V_k_0= V_k[:, :, :, 0]
V_k_1= V_k[:, :, :, 1]
V_k_2= V_k[:, :, :, 2]
V_k_3= V_k[:, :, :, 3]

mpl.rcParams['font.size'] = 16

sample_start = 0
sample_end = 100
subcarrier_start = 0
subcarrier_end = 499
fig = plt.figure(constrained_layout=True)
fig.set_size_inches(7.5, 5.5)
gs = gridspec.GridSpec(2, 2, hspace=0.2, wspace=0.2, figure=fig)
ax = []
ticks_y = np.arange(0, subcarrier_end - subcarrier_start, 100)
ticks_x = np.arange(0, sample_end - sample_start + 1, 15)


titles = [[r'$[\tilde{\mathbf{V}}]_{1, 1}$', r'$[\tilde{\mathbf{V}}]_{2, 1}$'],
          [r'$[\tilde{\mathbf{V}}]_{1, 2}$', r'$[\tilde{\mathbf{V}}]_{2, 2}$']]

for tx_ant in range(2):
    for rx_ant in range(2):
        v_submatrix = V_k[sample_start:sample_end, rx_ant, subcarrier_start:subcarrier_end, tx_ant]
        ax1 = fig.add_subplot(gs[(rx_ant, tx_ant)])
        ax1.pcolormesh(np.real(v_submatrix.T), cmap='viridis', linewidth=0, rasterized=True)  # , vmin=-1, vmax=1)
        ax1.set_title(titles[rx_ant][tx_ant])
        ax1.set_ylabel(r'sub-channel index')
        ax1.set_xlabel(r'time index')
        ax1.set_yticks(ticks_y + 0.5)
        ax1.set_yticklabels(ticks_y)
        ax1.set_xticks(ticks_x)
        ax1.set_xticklabels(ticks_x)
        ax.append(ax1)
for axi in ax:
    axi.label_outer()

plt.tight_layout()

plt.savefig('V_spectrogram.png', dpi=300, format='png')
plt.show()