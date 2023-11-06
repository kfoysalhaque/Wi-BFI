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
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

angles= np.load("bfa/bfa_ac_su_3x1_40.npy")
#angles= np.load("bfa/bfa_ax_su_4x2_160.npy")
#print(np.shape(angles))

angle = angles[:1, :, :]


x = range(angle.shape[1])

# Create a figure and axis object using matplotlib
fig, ax = plt.subplots(2, 1, figsize=(8,8))

# Loop through the first dimension of the array (axis 0)
for i in range(angle.shape[0]):
    # Plot the slice angle[i, :, j]
    ax[0].plot(x, angle[i, :, 0].flatten(), label='$\phi$\u2081\u2081', linewidth=4.0)

for i in range(angle.shape[0]):
    # Plot the slice angle[i, :, j]
    ax[1].plot(x, angle[i, :, 1].flatten(), label='$\phi$\u2082\u2081', linewidth=4.0)

# Add labels and title to the plot
ax[0].set_xlabel('Sub-channel', fontsize=40)
ax[1].set_xlabel('Sub-channel', fontsize=40)

ax[0].set_ylabel('Value', fontsize=40)
ax[1].set_ylabel('Value', fontsize=40)

#ax.set_title('Plotting a numpy array')
ax[0].grid()
ax[1].grid()

# Add a legend to differentiate the slices
ax[0].legend(fontsize='35', loc='lower left')
ax[1].legend(fontsize='35', loc='lower left')

ax[0].tick_params(axis='x', labelsize=35)  # Fontsize of x-axis tick labels
ax[1].tick_params(axis='x', labelsize=35)  # Fontsize of x-axis tick labels

ax[0].tick_params(axis='y', labelsize=35)  # Fontsize of y-axis tick labels
ax[1].tick_params(axis='y', labelsize=35)  # Fontsize of y-axis tick labels

plt.tight_layout()

plt.savefig('angle.png', dpi=300, format='png')
# Show the plot
plt.show()
