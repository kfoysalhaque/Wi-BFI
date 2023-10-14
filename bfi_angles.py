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


def bfi_angles(bin_chunk,LSB, NSUBC_VALID,order_bits):
    bfi_angles_all = []
    for l in range(NSUBC_VALID):
        chunk = bin_chunk[l]
        idx = 0
        bfi_angles_single = np.zeros(len(order_bits), dtype=int)
        for k in range(len(order_bits)):
            n_bits = order_bits[k]
            angle_bin = chunk[idx:(idx + n_bits)]
            angle_bin_str = ''.join([str(e) for j, e in enumerate(angle_bin)])
            if LSB:
                angle_bin_str = angle_bin_str[::-1]
            bfi_angles_single[k] = int(angle_bin_str, 2)
            idx += n_bits
        bfi_angles_all.append(bfi_angles_single)
    bfi_angles_all = np.array(bfi_angles_all)
    return bfi_angles_all