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

# Import necessary libraries
import pyshark
import numpy as np
import math
from textwrap import wrap
import argparse
from vmatrices import vmatrices
from bfi_angles import bfi_angles
from utils import hex2dec, flip_hex

# Set the default value for the least significant bit (LSB)
LSB = True

# Check if the script is being run as the main program
if __name__ == '__main__':
    # Create a command-line argument parser
    parser = argparse.ArgumentParser(description=__doc__)

    # Define command-line arguments
    parser.add_argument('file_name', help='File name to process')
    parser.add_argument('standard', help='which standard are you operating on, options are "AC" or "AX" ')
    parser.add_argument('mimo', help='which type of network are you forming, options are "SU" for su-mimo or "MU" for mu-mimo ')
    parser.add_argument('config', help='which type of antenna config you have, for now, available options are 3x1 with AC and 4x2 with AX')
    parser.add_argument('bw', help='bandwidth of the capture')
    parser.add_argument('MAC', help='MAC of the Target Device')
    parser.add_argument('num_packet_to_process', help='num_packet_to_process')
    parser.add_argument('saved_vmatrices', help='saved_vmatrices')
    parser.add_argument('saved_angles', help='saved_angles')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Set variables based on command-line arguments
    file_name = 'traces/' + args.file_name
    standard = args.standard
    mimo = args.mimo
    config = args.config
    bw = int(args.bw)
    MAC = args.MAC
    num_packet_to_process = int(args.num_packet_to_process)
    saved_vmatrices = 'vmatrix/' + args.saved_vmatrices
    saved_angles = 'bfa/' + args.saved_angles

    # Check if mu-mimo is selected for AX standard
    if mimo == "MU" and standard == "AX":
        print("mu-mimo is not available for AX yet, we will add this feature soon")
    else:
        print("Processing")


    # Check standard and set parameters accordingly
    if standard == "AC":

        # Set subcarrier indices based on bandwidth
        if bw == 80:
            subcarrier_idxs = np.arange(-122, 123)
            pilot_n_null = np.array([-104, -76, -40, -12, -1, 0, 1, 10, 38, 74, 102])
            subcarrier_idxs = np.setdiff1d(subcarrier_idxs, pilot_n_null)
        elif bw == 40:
            subcarrier_idxs = np.arange(-58, 59)
            pilot_n_null = np.array([-54, -26, -12, -1, 0, 1, 10, 24, 52])
            subcarrier_idxs = np.setdiff1d(subcarrier_idxs, pilot_n_null)
        elif bw == 20:
            subcarrier_idxs = np.arange(-28, 29)
            pilot_n_null = np.array([-21, -8, 0, 6, 21])
            subcarrier_idxs = np.setdiff1d(subcarrier_idxs, pilot_n_null)
        else:
            print("input a valid bandwidth for IEEE 802.11ac")

    if standard == "AX":

        # Set subcarrier indices based on bandwidth
        if bw == 160:
            subcarrier_idxs = np.arange(-1012, 1013, 4)
            pilot_n_null = np.array([-512, -8, -4, 0, 4, 8, 512])
            subcarrier_idxs = np.setdiff1d(subcarrier_idxs, pilot_n_null)
        elif bw == 80:
            subcarrier_idxs = np.arange(-500, 504, 4)
            pilot_n_null = np.array([0])
            subcarrier_idxs = np.setdiff1d(subcarrier_idxs, pilot_n_null)
        elif bw == 40:
            subcarrier_idxs = np.arange(-244, 248, 4)
            pilot_n_null = np.array([0])
            subcarrier_idxs = np.setdiff1d(subcarrier_idxs, pilot_n_null)
        elif bw == 20:
            subcarrier_idxs = np.arange(-122, 126, 4)
            pilot_n_null = np.array([0])
            subcarrier_idxs = np.setdiff1d(subcarrier_idxs, pilot_n_null)
        else:
            print("input a valid bandwidth for IEEE 802.11ac")

        
    # Read packets from the pcap file based on the selected standard
    if standard == "AX":
        packets = pyshark.FileCapture(
            input_file=file_name,
            display_filter='wlan.he.mimo.feedback_type==SU && wlan.addr==%s' % (MAC),
            use_json=True,
            include_raw=True
        )._packets_from_tshark_sync()  # pcap_dir is the directory of my pcap file
    elif standard == "AC":
        packets = pyshark.FileCapture(
            input_file=file_name,
            display_filter='wlan.vht.mimo_control.feedbacktype==%s && wlan.addr==%s' % (mimo, MAC),
            use_json=True,
            include_raw=True
        )._packets_from_tshark_sync()

    # Initialize lists to store feedback angles and v-matrices
    bfi_angles_all_packets = []
    v_matrices_all = []

    # Process each packet
    for p in range(num_packet_to_process):
    	# Extract raw frame data from the packet
        packet = packets.__next__().frame_raw.value
        print('packet___________ ' + str(p) + '\n\n\n')

        # Extract header information from the raw frame data
        Header_rivision_dec = hex2dec(flip_hex(packet[0:2]))
        Header_pad_dec = hex2dec(flip_hex(packet[2:4]))
        Header_length_dec = hex2dec(flip_hex(packet[4:8]))
        i = Header_length_dec * 2

        # Extract various fields from the frame
        Frame_Control_Field_hex = packet[i:(i + 4)]
        packet_duration = packet[(i + 4):(i + 8)]
        packet_destination_mac = packet[(i + 8):(i + 20)]
        packet_sender_mac = packet[(i + 20):(i + 32)]
        packet_BSS_ID = packet[(i + 32):(i + 44)]
        packet_sequence_number = packet[(i + 44):(i + 48)]
        packet_HE_category = packet[(i + 48):(i + 50)]
        packet_CQI = packet[(i + 50):(i + 52)]

        # Extract specific fields for AX or AC standard
        if standard == "AX":
            packet_mimo_control = packet[(i + 52):(i + 62)]
            packet_mimo_control_binary = ''.join(format(int(char, 16), '04b') for char in flip_hex(packet_mimo_control))
            codebook_info = packet_mimo_control_binary[30] 
            packet_snr = packet[(i + 62):(i + 62 + 2*int(config[-1]))]
            frame_check_sequence = packet[-8:]

        if standard == "AC":
            packet_mimo_control = packet[(i + 52):(i + 58)]
            packet_mimo_control_binary = ''.join(format(int(char, 16), '04b') for char in flip_hex(packet_mimo_control))
            codebook_info = packet_mimo_control_binary[13]
            packet_snr = packet[(i + 58):(i + 58 + 2*int(config[-1]))]
            frame_check_sequence = packet[-8:]


        # Set bits for angles based on mimo type
        if mimo == "SU":
            if codebook_info == "1":
                psi_bit = 4
                phi_bit = psi_bit + 2
            else:
                psi_bit = 2
                phi_bit = psi_bit + 2
        elif mimo == "MU":
            if codebook_info == "1":
                psi_bit = 7
                phi_bit = psi_bit + 2
            else:
                psi_bit = 5
                phi_bit = psi_bit + 2


        if config == "4x2":
            # Set parameters for 4x2 antenna configuration
            Nc_users = 2  # number of spatial streams
            Nr = 4  # number of Tx antennas
            phi_numbers = 5
            psi_numbers = 5
            order_angles = ['phi_11', 'phi_21', 'phi_31', 'psi_21', 'psi_31', 'psi_41', 'phi_22', 'phi_32', 'psi_32',
                            'psi_42']
            order_bits = [phi_bit, phi_bit, phi_bit, psi_bit, psi_bit, psi_bit, phi_bit, phi_bit, psi_bit, psi_bit]
            tot_angles_users = phi_numbers + psi_numbers
            tot_bits_users = phi_numbers * phi_bit + psi_numbers * psi_bit

        elif config == "4x1":
            # Set parameters for 4x1 antenna configuration
            Nc_users = 1  # number of spatial streams
            Nr = 4  # number of Tx antennas
            phi_numbers = 3
            psi_numbers = 3
            order_angles = ['phi_11', 'phi_21', 'phi_31', 'psi_21', 'psi_31', 'psi_41']
            order_bits = [phi_bit, phi_bit, phi_bit, psi_bit, psi_bit, psi_bit]
            tot_angles_users = phi_numbers + psi_numbers
            tot_bits_users = phi_numbers * phi_bit + psi_numbers * psi_bit

        elif config == "3x3":
            # Set parameters for 3x3 antenna configuration
            Nc_users = 3  # number of spatial streams
            Nr = 3  # number of Tx antennas
            phi_numbers = 3
            psi_numbers = 3
            order_angles = ['phi_11', 'phi_21', 'psi_21', 'psi_31', 'phi_22', 'psi_32']
            order_bits = [phi_bit, phi_bit, psi_bit, psi_bit, phi_bit, psi_bit]
            tot_angles_users = phi_numbers + psi_numbers
            tot_bits_users = phi_numbers * phi_bit + psi_numbers * psi_bit

        elif config == "3x2":
            # Set parameters for 3x2 antenna configuration
            Nc_users = 2  # number of spatial streams
            Nr = 3  # number of Tx antennas
            phi_numbers = 3
            psi_numbers = 3
            order_angles = ['phi_11', 'phi_21', 'psi_21', 'psi_31', 'phi_22', 'psi_32']
            order_bits = [phi_bit, phi_bit, psi_bit, psi_bit, phi_bit, psi_bit]
            tot_angles_users = phi_numbers + psi_numbers
            tot_bits_users = phi_numbers * phi_bit + psi_numbers * psi_bit

        elif config == "3x1":
            # Set parameters for 3x1 antenna configuration
            Nc_users = 1  # number of spatial streams
            Nr = 3  # number of Tx antennas
            phi_numbers = 2
            psi_numbers = 2
            order_angles = ['phi_11', 'phi_21', 'psi_21', 'psi_31']
            order_bits = [phi_bit, phi_bit, psi_bit, psi_bit]
            tot_angles_users = phi_numbers + psi_numbers
            tot_bits_users = phi_numbers * phi_bit + psi_numbers * psi_bit

        else:
            print("the antenna configuration that you have is not available right now, you will update other configurations soon, stay tuned")

        # Set constant for valid subcarriers
        NSUBC_VALID = len(subcarrier_idxs)
        length_angles_users_bits = NSUBC_VALID * tot_bits_users
        length_angles_users = math.floor(length_angles_users_bits / 8)


        # Extract specific fields for AX or AC standard
        if standard == "AX":
            Feedback_angles = packet[(i + 62 + 2*int(config[-1])):(len(packet) - 8)]
            Feedback_angles_splitted = np.array(wrap(Feedback_angles, 2))
            Feedback_angles_bin = ""
        if standard == "AC":
            #Feedback_angles = packet[(i + 60):(i + 60 + (length_angles_users * 2))]
            Feedback_angles = packet[(i + 58 + 2*int(config[-1])):(len(packet) - 8)]
            #bfm_report_length = packet[(i + 60 + length_angles_users * 2):(len(packet) - 8)]
            Feedback_angles_splitted = np.array(wrap(Feedback_angles, 2))
            Feedback_angles_bin = ""



        # Convert feedback angles to binary format
        for i in range(0, len(Feedback_angles_splitted)):
            bin_str = str(format(hex2dec(Feedback_angles_splitted[i]), '08b'))
            if LSB:
                bin_str = bin_str[::-1]
            Feedback_angles_bin += bin_str

        # Split the binary feedback angles into chunks for each subcarrier
        # for j in range(0, len(subcarrier_idxs)):
        #     Feed_back_angles_bin_chunk = np.array(wrap(Feedback_angles_bin[:(tot_bits_users * NSUBC_VALID)], tot_bits_users))

        Feed_back_angles_bin_chunk = np.array(wrap(Feedback_angles_bin[:(tot_bits_users * NSUBC_VALID)], tot_bits_users))

        # Calculate angles and v-matrices and store them in lists
        angle = bfi_angles(Feed_back_angles_bin_chunk, LSB, NSUBC_VALID, order_bits)
        v_matrices_all.append(vmatrices(angle, phi_bit, psi_bit, NSUBC_VALID, Nr, Nc_users, config))
        bfi_angles_all_packets.append(bfi_angles(Feed_back_angles_bin_chunk, LSB, NSUBC_VALID, order_bits))

    # Save v-matrices and angles to files
    np.save(saved_vmatrices, v_matrices_all)
    np.save(saved_angles, bfi_angles_all_packets)
