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
import math
import cmath


def vmatrices(angle, phi_bit, psi_bit, NSUBC_VALID, Nr, Nc_users, config):
    if config == "4x2":

        const1_phi = 1 / 2 ** (phi_bit - 1)
        const2_phi = 1 / 2 ** (phi_bit)

        const1_psi = 1 / 2 ** (psi_bit + 1)
        const2_psi = 1 / 2 ** (psi_bit + 2)

        phi_11 = math.pi * (const2_phi + const1_phi * angle[:, 0])
        phi_21 = math.pi * (const2_phi + const1_phi * angle[:, 1])
        phi_31 = math.pi * (const2_phi + const1_phi * angle[:, 2])

        psi_21 = math.pi * (const2_psi + const1_psi * angle[:, 3])
        psi_31 = math.pi * (const2_psi + const1_psi * angle[:, 4])
        psi_41 = math.pi * (const2_psi + const1_psi * angle[:, 5])

        phi_22 = math.pi * (const2_phi + const1_phi * angle[:, 6])
        phi_32 = math.pi * (const2_phi + const1_phi * angle[:, 7])

        psi_32 = math.pi * (const2_psi + const1_psi * angle[:, 8])
        psi_42 = math.pi * (const2_psi + const1_psi * angle[:, 9])

        v_matrix = []
        v_matrix_all = []
        for s in range (NSUBC_VALID):
            #build D matrices(phi)
            D_1 = [[cmath.exp(1j * phi_11[s]), 0, 0, 0],
                  [0, cmath.exp(1j * phi_21[s]), 0, 0],
                  [0, 0, cmath.exp(1j * phi_31[s]), 0],
                  [0, 0, 0, 1]]

            D_2 = [[1, 0, 0, 0],
                  [0, cmath.exp(1j * phi_22[s]), 0, 0],
                  [0, 0, cmath.exp(1j * phi_32[s]), 0],
                  [0, 0, 0, 1]]


            #build G matrices(psi)
            G_21 = [[math.cos(psi_21[s]), math.sin(psi_21[s]), 0, 0],
                    [-math.sin(psi_21[s]), math.cos(psi_21[s]), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]]

            G_31 = [[math.cos(psi_31[s]), 0, math.sin(psi_31[s]), 0],
                    [0, 1, 0, 0],
                    [-math.sin(psi_31[s]), 0, math.cos(psi_31[s]), 0],
                    [0, 0, 0, 1]]

            G_41 = [[math.cos(psi_41[s]), 0, 0, math.sin(psi_41[s])],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [-math.sin(psi_41[s]), 0, 0, math.cos(psi_41[s])]]

            G_32 = [[1, 0, 0, 0],
                    [0, math.cos(psi_32[s]), math.sin(psi_32[s]), 0],
                    [0, -math.sin(psi_32[s]), math.cos(psi_32[s]), 0],
                    [0, 0, 0, 1]]

            G_42 = [[1, 0, 0, 0],
                    [0, math.cos(psi_42[s]), 0, math.sin(psi_42[s])],
                    [0, 0, 1, 0],
                    [0, -math.sin(psi_42[s]), 0, math.cos(psi_42[s])]]

            I_matrix = np.eye(Nr, Nc_users)
            V = np.matmul(np.matmul(np.matmul(np.matmul(np.matmul(np.matmul(np.matmul(D_1, np.transpose(G_21)), np.transpose(G_31)), np.transpose(G_41)), D_2), np.transpose(G_32)), np.transpose(G_42)), I_matrix)
            v_matrix = np.transpose(V)
            v_matrix_all.append(v_matrix)


    if config == "4x1":

        const1_phi = 1 / 2 ** (phi_bit - 1)
        const2_phi = 1 / 2 ** (phi_bit)

        const1_psi = 1 / 2 ** (psi_bit + 1)
        const2_psi = 1 / 2 ** (psi_bit + 2)

        phi_11 = math.pi * (const2_phi + const1_phi * angle[:, 0])
        phi_21 = math.pi * (const2_phi + const1_phi * angle[:, 1])
        phi_31 = math.pi * (const2_phi + const1_phi * angle[:, 2])

        psi_21 = math.pi * (const2_psi + const1_psi * angle[:, 3])
        psi_31 = math.pi * (const2_psi + const1_psi * angle[:, 4])
        psi_41 = math.pi * (const2_psi + const1_psi * angle[:, 5])


        v_matrix = []
        v_matrix_all = []
        for s in range (NSUBC_VALID):
            #build D matrices(phi)
            D_1 = [[cmath.exp(1j * phi_11[s]), 0, 0, 0],
                  [0, cmath.exp(1j * phi_21[s]), 0, 0],
                  [0, 0, cmath.exp(1j * phi_31[s]), 0],
                  [0, 0, 0, 1]]


            #build G matrices(psi)
            G_21 = [[math.cos(psi_21[s]), math.sin(psi_21[s]), 0, 0],
                    [-math.sin(psi_21[s]), math.cos(psi_21[s]), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]]

            G_31 = [[math.cos(psi_31[s]), 0, math.sin(psi_31[s]), 0],
                    [0, 1, 0, 0],
                    [-math.sin(psi_31[s]), 0, math.cos(psi_31[s]), 0],
                    [0, 0, 0, 1]]

            G_41 = [[math.cos(psi_41[s]), 0, 0, math.sin(psi_41[s])],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [-math.sin(psi_41[s]), 0, 0, math.cos(psi_41[s])]]


            I_matrix = np.eye(Nr, Nc_users)
            V = np.matmul(np.matmul(np.matmul(np.matmul(D_1, np.transpose(G_21)), np.transpose(G_31)), np.transpose(G_41)), I_matrix)
            v_matrix = np.transpose(V)
            v_matrix_all.append(v_matrix)


    if config == "3x3" or config == "3x2":

        const1_phi = 1 / 2 ** (phi_bit - 1)
        const2_phi = 1 / 2 ** (phi_bit)

        const1_psi = 1 / 2 ** (psi_bit + 1)
        const2_psi = 1 / 2 ** (psi_bit + 2)

        phi_11 = math.pi * (const2_phi + const1_phi * angle[:, 0])
        phi_21 = math.pi * (const2_phi + const1_phi * angle[:, 1])

        psi_21 = math.pi * (const2_psi + const1_psi * angle[:, 2])
        psi_31 = math.pi * (const2_psi + const1_psi * angle[:, 3])

        phi_22 = math.pi * (const2_phi + const1_phi * angle[:, 4])

        psi_32 = math.pi * (const2_psi + const1_psi * angle[:, 5])

        v_matrix = []
        v_matrix_all = []
        for s in range(NSUBC_VALID):
            # build D matrices(phi)
            D_1 = [[cmath.exp(1j * phi_11[s]), 0, 0],
                   [0, cmath.exp(1j * phi_21[s]), 0],
                   [0, 0, 1]]

            D_2 = [[1, 0, 0 ],
                  [0, cmath.exp(1j * phi_22[s]), 0],
                  [0, 0, 1]]

            # build G matrices(psi)
            G_21 = [[math.cos(psi_21[s]), math.sin(psi_21[s]), 0],
                    [-math.sin(psi_21[s]), math.cos(psi_21[s]), 0],
                    [0, 0, 1]]

            G_31 = [[math.cos(psi_31[s]), 0, math.sin(psi_31[s])],
                    [0, 1, 0],
                    [-math.sin(psi_31[s]), 0, math.cos(psi_31[s])]]

            G_32 = [[1, 0, 0],
                    [0, math.cos(psi_32[s]), math.sin(psi_32[s])],
                    [0, -math.sin(psi_32[s]), math.cos(psi_32[s])]]

            I_matrix = np.eye(Nr, Nc_users)
            V = np.matmul(np.matmul(np.matmul(np.matmul(np.matmul(D_1,np.transpose(G_21)),np.transpose(G_31)), D_2), np.transpose(G_32)), I_matrix)
            v_matrix = np.transpose(V)
            v_matrix_all.append(v_matrix)



    if config == "3x1":

        const1_phi = 1 / 2 ** (phi_bit - 1)
        const2_phi = 1 / 2 ** (phi_bit)
        phi_11 = math.pi * (const2_phi + const1_phi * angle[:, 0])
        phi_21 = math.pi * (const2_phi + const1_phi * angle[:, 1])

        const1_psi = 1 / 2 ** (psi_bit + 1)
        const2_psi = 1 / 2 ** (psi_bit + 2)
        psi_21 = math.pi * (const2_psi + const1_psi * angle[:, 2])
        psi_31 = math.pi * (const2_psi + const1_psi * angle[:, 3])

        v_matrix = []
        v_matrix_all = []
        for s in range(NSUBC_VALID):
            # build D matrices(phi)
            D_1 = [[cmath.exp(1j * phi_11[s]), 0, 0],
                   [0, cmath.exp(1j * phi_21[s]), 0],
                   [0, 0, 1]]

            # build G matrices(psi)
            G_21 = [[math.cos(psi_21[s]), math.sin(psi_21[s]), 0],
                    [-math.sin(psi_21[s]), math.cos(psi_21[s]), 0],
                    [0, 0, 1]]

            G_31 = [[math.cos(psi_31[s]), 0, math.sin(psi_31[s])],
                    [0, 1, 0],
                    [-math.sin(psi_31[s]), 0, math.cos(psi_31[s])]]

            I_matrix = np.eye(Nr, Nc_users)
            V = np.matmul(np.matmul(np.matmul(D_1,np.transpose(G_21)),np.transpose(G_31)),I_matrix)
            v_matrix = np.transpose(V)
            v_matrix_all.append(v_matrix)


    v_matrix_all = np.stack(v_matrix_all, axis=1)
    v_matrix_all = np.moveaxis(v_matrix_all, [1, 2, 0], [0, 1, 2])
    return v_matrix_all
