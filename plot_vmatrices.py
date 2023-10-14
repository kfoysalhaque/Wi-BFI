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

V_k = np.load("vmatrix/V_ax_su_4x2_160.npy")
V_k = V_k[3:4, :, :]

V_k_squeezed= np.squeeze(V_k)

V_k_0= V_k_squeezed[:, 0, :]
V_k_1= V_k_squeezed[:, 1, :]
V_k_2= V_k_squeezed[:, 2, :]
V_k_3= V_k_squeezed[:, 3, :]


x = range(V_k_0.shape[0])

fig, ax = plt.subplots(2, 2)

ax[0, 0].plot(x, np.abs(V_k_0[:, 0]))
ax[0, 1].plot(x, np.abs(V_k_0[:, 1]))
ax[1, 0].plot(x, np.abs(V_k_1[:, 0]))
ax[1, 1].plot(x, np.abs(V_k_1[:, 1]))


ax[0, 0].set_xlabel('Sub-channel Index', fontsize=13)
ax[0, 1].set_xlabel('Sub-channel Index', fontsize=13)
ax[1, 0].set_xlabel('Sub-channel Index', fontsize=13)
ax[1, 1].set_xlabel('Sub-channel Index', fontsize=13)

ax[0, 0].set_ylabel(r'$\tilde{V}_{k}$ Magnitude', fontsize=12)
ax[0, 1].set_ylabel(r'$\tilde{V}_{k}$ Magnitude', fontsize=12)
ax[1, 0].set_ylabel(r'$\tilde{V}_{k}$ Magnitude', fontsize=12)
ax[1, 1].set_ylabel(r'$\tilde{V}_{k}$ Magnitude', fontsize=12)


ax[0, 0].set_title(r'$m=1$ & $n_{ss}=1$', fontsize=12)
ax[0, 1].set_title(r'$m=2$ & $n_{ss}=1$', fontsize=12)
ax[1, 0].set_title(r'$m=1$ & $n_{ss}=2$', fontsize=12)
ax[1, 1].set_title(r'$m=2$ & $n_{ss}=2$', fontsize=12)



ax[0, 0].tick_params(axis='y', labelsize=12)  # Fontsize of x-axis tick labels
ax[0, 1].tick_params(axis='y', labelsize=12)  # Fontsize of x-axis tick labels
ax[1, 0].tick_params(axis='y', labelsize=12)  # Fontsize of x-axis tick labels
ax[1, 1].tick_params(axis='y', labelsize=12)  # Fontsize of x-axis tick labels

ax[0, 0].grid()
ax[0, 1].grid()
ax[1, 0].grid()
ax[1, 1].grid()

xtick_locs = [0, 250, 500]
xtick_labels = ['0', '250', '500']

ytick_locs = [0.0, 0.50, 1]
ytick_labels = ['0.00', '0.50', '1.00']

ax[0, 0].set_xticks(xtick_locs)  # Set the tick locations
ax[0, 0].set_xticklabels(xtick_labels, fontsize=12)  # Set the tick labels
ax[0, 1].set_xticks(xtick_locs)  # Set the tick locations
ax[0, 1].set_xticklabels(xtick_labels, fontsize=12)  # Set the tick labels
ax[1, 0].set_xticks(xtick_locs)  # Set the tick locations
ax[1, 0].set_xticklabels(xtick_labels, fontsize=12)  # Set the tick labels
ax[1, 1].set_xticks(xtick_locs)  # Set the tick locations
ax[1, 1].set_xticklabels(xtick_labels, fontsize=12)  # Set the tick labels


ax[0, 0].set_yticks(ytick_locs) # Set the tick locations
ax[0, 0].set_yticklabels(ytick_labels, fontsize=12)  # Set the tick labels
ax[0, 1].set_yticks(ytick_locs)  # Set the tick locations
ax[0, 1].set_yticklabels(ytick_labels, fontsize=12)  # Set the tick labels
ax[1, 0].set_yticks(ytick_locs)  # Set the tick locations
ax[1, 0].set_yticklabels(ytick_labels, fontsize=12)  # Set the tick labels
ax[1, 1].set_yticks(ytick_locs)  # Set the tick locations
ax[1, 1].set_yticklabels(ytick_labels, fontsize=12)  # Set the tick labels

# Add a legend
plt.legend()
plt.tight_layout()

plt.savefig('V_k.png', dpi=300, format='png')
# Display the plot
plt.show()
