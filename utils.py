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
from textwrap import wrap


def hex2dec(hex_value):
    hex2array = np.array(wrap(hex_value, 2))
    # hex2array_flipped = np.flip(hex2array)
    array_joined = "".join(hex2array)
    decimal_value = int(array_joined, 16)
    return decimal_value


def flip_hex(hex_value):
    hex2array = np.array(wrap(hex_value, 2))
    hex2array_flipped = np.flip(hex2array)
    hex2array_flipped = "".join(hex2array_flipped)
    return hex2array_flipped