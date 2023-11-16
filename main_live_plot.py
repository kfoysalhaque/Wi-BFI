"""
    Copyright (C) 2023 Francesca Meneghello
    contact: francesca.meneghello.1@unipd.it
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
from multiprocessing import Process, Value, Pool, Manager, Queue
import math as mt
import time
import matplotlib
from matplotlib import pyplot as plt
import os
import nest_asyncio
nest_asyncio.apply()

# Set the default value for the least significant bit (LSB)
LSB = True

matplotlib.use('QtCairo')  # works with debug and run!
import PySimpleGUI as sg
sg.set_options(font=('Arial'))
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.sans-serif'] = ['Times']
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['text.usetex'] = 'true'
#matplotlib.rcParams['text.latex.preamble'] = [r'\usepackage{newtxmath}']
matplotlib.rcParams['axes.linewidth'] = 0.5 #default 0.
matplotlib.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.Paired.colors)
matplotlib.rcParams['toolbar'] = 'None'


def plot_angles(q, i, title_plot):
    # PLOTS
    plt.ion()
    # fig, ax0 = plt.subplots(1, 1, figsize=(6, 4.5))
    fig, ax0 = plt.subplots(1, 1, figsize=(5.1, 4))
    fig_canvas = fig.canvas  # fig_canvas = FigureCanvasTkAgg(fig)

    # To place the figures
    num_columns = 5
    start_x = 80
    start_y = 220
    # x = start_x + 650 * int(mt.fmod(i, num_columns))
    x = start_x + 540 * int(mt.fmod(i, num_columns))
    # y = start_y + 525 * int(i // num_columns)
    y = start_y + 440 * int(i // num_columns)
    backend = matplotlib.get_backend()
    if backend == 'TkAgg':
        fig_canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
        # fig_canvas.manager.window.overrideredirect(True)
    elif backend == 'WXAgg':
        fig_canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        fig_canvas.manager.window.move(x, y)

    # print('I am number %d in process %d - plots' % (i, getpid()))
    # PLOT
    ax0.set_ylim(0, 80)
    ax0.set_xlim(0, NSUBC_VALID)
    ax0.set_xticks(np.arange(0, NSUBC_VALID + 1, 22))
    ax0.grid(axis='both')
    ax0.set_ylabel(r'value', fontsize=13)
    # name_plot = r'\textbf{angle: %s}' % title_plot
    name_plot = title_plot
    ax0.set_title(name_plot)

    x1 = np.arange(0, NSUBC_VALID)
    linea, = ax0.plot(x1, [np.nan] * NSUBC_VALID, linewidth=2.0, color='#0C2C52')
    fig_canvas.draw()  # draw and show it
    plt.show(block=False)

    path_print_int = 1

    while True:
        signal_considered = q.get() + 0
        linea.set_ydata(np.real(signal_considered))
        # fig.canvas.draw()
        # fig.canvas.flush_events()
        ax0.relim()
        ax0.autoscale_view(tight=True, scalex=True, scaley=False)
        fig_canvas.draw()
        plt.pause(1e-30)

# Check if the script is being run as the main program
if __name__ == '__main__':
    # Create a command-line argument parser
    parser = argparse.ArgumentParser(description=__doc__)

    # Define command-line arguments
    parser.add_argument('standard', help='which standard are you operating on, options are "AC" or "AX" ')
    parser.add_argument('mimo', help='which type of network are you forming, options are "SU" for su-mimo or "MU" for mu-mimo ')
    parser.add_argument('config', help='which type of antenna config you have, for now, available options are 3x1 with AC and 4x2 with AX')
    parser.add_argument('bw', help='bandwidth of the capture')
    parser.add_argument('MAC', help='MAC of the Target Device')
    parser.add_argument('dir', help='Directory of data')
    parser.add_argument('seconds_interval', help='Seconds every which you have a new file', type=int)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Set variables based on command-line arguments
    standard = args.standard
    mimo = args.mimo
    config = args.config
    bw = int(args.bw)
    MAC = args.MAC
    exp_dir = 'Demo/'+ args.dir + '/'
    step = args.seconds_interval

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

    NSUBC_VALID = len(subcarrier_idxs)

    if config == "4x2":
        # Set parameters for 4x2 antenna configuration
        Nc_users = 2  # number of spatial streams
        Nr = 4  # number of Tx antennas
        phi_numbers = 5
        psi_numbers = 5
        order_angles = ['phi_11', 'phi_21', 'phi_31', 'psi_21', 'psi_31', 'psi_41', 'phi_22', 'phi_32', 'psi_32',
                        'psi_42']


    elif config == "4x1":
        # Set parameters for 4x1 antenna configuration
        Nc_users = 1  # number of spatial streams
        Nr = 4  # number of Tx antennas
        phi_numbers = 3
        psi_numbers = 3
        order_angles = ['phi_11', 'phi_21', 'phi_31', 'psi_21', 'psi_31', 'psi_41']


    elif config == "3x3":
        # Set parameters for 3x3 antenna configuration
        Nc_users = 3  # number of spatial streams
        Nr = 3  # number of Tx antennas
        phi_numbers = 3
        psi_numbers = 3
        order_angles = ['phi_11', 'phi_21', 'psi_21', 'psi_31', 'phi_22', 'psi_32']


    elif config == "3x2":
        # Set parameters for 3x2 antenna configuration
        Nc_users = 2  # number of spatial streams
        Nr = 3  # number of Tx antennas
        phi_numbers = 3
        psi_numbers = 3
        order_angles = ['phi_11', 'phi_21', 'psi_21', 'psi_31', 'phi_22', 'psi_32']


    elif config == "3x1":
        # Set parameters for 3x1 antenna configuration
        Nc_users = 1  # number of spatial streams
        Nr = 3  # number of Tx antennas
        phi_numbers = 2
        psi_numbers = 2
        order_angles = ['phi_11', 'phi_21', 'psi_21', 'psi_31']


    else:
        print(
            "the antenna configuration that you have is not available right now, you will update other configurations soon, stay tuned")


    notDone = True
    while notDone:
        try:
            with open(exp_dir + 'start_time.txt') as f:
                start_time = int(f.readline())
            notDone = False
        except FileNotFoundError:
            print('Please, start tcpdump for data acquisition. Waiting...')
            time.sleep(1)
        # Define the window layout
    my_new_theme = {'BACKGROUND': '#152238',
                    'TEXT': '#dedede',  # '#9eb9d4',
                    'INPUT': '#c7e78b',
                    'TEXT_INPUT': '#000000',
                    'SCROLL': '#c7e78b',
                    'BUTTON': ('white', '#709053'),
                    'PROGRESS': ('#01826B', '#D0D0D0'),
                    'BORDER': 1,
                    'SLIDER_DEPTH': 0,
                    'PROGRESS_DEPTH': 0}
    sg.theme_add_new('MyNewTheme', my_new_theme)
    sg.theme('MyNewTheme')
    font1 = ('Arial', 30)
    font2 = ('Arial', 24)
    layout = [
        # [sg.Text(f'\n')],
        [sg.Text(f'*' * 140, font=font1), sg.Push()],
        [sg.Text(f'Real-time Beamforming Feedback Angles Plotting at IEEE 802.11ax ch. 36 BW 80 MHz', font=font1), sg.Push()],
        # [sg.Text(f'beamforming feedback angles collection at IEEE 802.11ax ch. 44 BW 80 MHz', font=font1), sg.Push()],
        [sg.Text(f'*' * 140, font=font1), sg.Push()],
        [sg.Text(f'\n' * 68)],
        # [sg.Text(f'For reference see:', font=font1), sg.Push()],
        #[sg.Text(f'F. Meneghello et al., \'DeepCSI: Rethinking Wi-Fi Radio Fingerprinting Through MU-MIMO CSI Feedback Deep Learning\', in Proc. of IEEE ICDCS, 2022.', font=font1), sg.Push()],
        #[sg.Text(f'K. F. Haque et al., \'BeamSense: Rethinking Wireless Sensing with MU-MIMO Wi-Fi Beamforming Feedback\', 2023.', font=font1), sg.Push()],
        [sg.Canvas(key="-CANVAS-")]
    ]

    # Create the form and show it without the plot
    window = sg.Window(
        "WiSEC",
        layout,
        location=(100, 0),
        finalize=True,
        element_justification="center",
        # font="Times 30",
        resizable=True,
        size=(3000, 1500),
        # no_titlebar=True,
        keep_on_top=True
    )

    # Create plots
    queues_plot = []
    processes_plot = []
    num_parallel_processes = 10
    for angle_idx in range(0, num_parallel_processes):
        queues_plot.append(Queue())
        p = Process(target=plot_angles, args=(queues_plot[angle_idx], angle_idx, order_angles[angle_idx]))
        p.start()
        processes_plot.append(p)

    iteration_num = 0
    while True:
        file_name = exp_dir + str(start_time + step*iteration_num)
        print('FILE NAME: ', file_name)

        file_name_next = exp_dir + str(start_time + step * (iteration_num + 1))
        while not os.path.exists(file_name_next):
            # print('No more files. Waiting...')
            time.sleep(step)
            file_name_next_next = exp_dir + str(start_time + step * (iteration_num + 2))
            if os.path.exists(file_name_next_next):
                # it means that we need to skip one file (not written because empty)
                iteration_num = iteration_num + 1
                break

        iteration_num = iteration_num + 1

    # Read packets from the pcap file based on the selected standard
        if standard == "AX":
            reader = pyshark.FileCapture(
                input_file=file_name,
                display_filter='wlan.he.mimo.feedback_type==SU && wlan.addr==%s' % (MAC),
                use_json=True,
                include_raw=True
            )._packets_from_tshark_sync()  # pcap_dir is the directory of my pcap file
        elif standard == "AC":
            reader = pyshark.FileCapture(
                input_file=file_name,
                display_filter='wlan.vht.mimo_control.feedbacktype==%s && wlan.addr==%s' % (mimo, MAC),
                use_json=True,
                include_raw=True
            )._packets_from_tshark_sync()

        # Initialize lists to store feedback angles and v-matrices
        bfi_angles_all_packets = []
        v_matrices_all = []

        # Process each packet
        while True:
            try:
                packet = reader.__next__().frame_raw.value
            except StopIteration:
                # print('Processing finished. Exiting...')
                break
            # print('packet no. ' + str(packet_no) + '\n\n\n')
            # packet_no = packet_no + 1

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
                packet_snr = packet[(i + 62):(i + 66)]
                frame_check_sequence = packet[-8:]

            if standard == "AC":
                packet_mimo_control = packet[(i + 52):(i + 58)]
                packet_mimo_control_binary = ''.join(format(int(char, 16), '04b') for char in flip_hex(packet_mimo_control))
                codebook_info = packet_mimo_control_binary[13]
                packet_snr = packet[(i + 58):(i + 60)]
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
                order_bits = [phi_bit, phi_bit, phi_bit, psi_bit, psi_bit, psi_bit, phi_bit, phi_bit, psi_bit, psi_bit]
                tot_angles_users = phi_numbers + psi_numbers
                tot_bits_users = phi_numbers * phi_bit + psi_numbers * psi_bit

            elif config == "4x1":

                order_bits = [phi_bit, phi_bit, phi_bit, psi_bit, psi_bit, psi_bit]
                tot_angles_users = phi_numbers + psi_numbers
                tot_bits_users = phi_numbers * phi_bit + psi_numbers * psi_bit

            elif config == "3x3":

                order_bits = [phi_bit, phi_bit, psi_bit, psi_bit, phi_bit, psi_bit]
                tot_angles_users = phi_numbers + psi_numbers
                tot_bits_users = phi_numbers * phi_bit + psi_numbers * psi_bit

            elif config == "3x2":

                order_bits = [phi_bit, phi_bit, psi_bit, psi_bit, phi_bit, psi_bit]
                tot_angles_users = phi_numbers + psi_numbers
                tot_bits_users = phi_numbers * phi_bit + psi_numbers * psi_bit

            elif config == "3x1":

                order_bits = [phi_bit, phi_bit, psi_bit, psi_bit]
                tot_angles_users = phi_numbers + psi_numbers
                tot_bits_users = phi_numbers * phi_bit + psi_numbers * psi_bit

            else:
                print("the antenna configuration that you have is not available right now, you will update other configurations soon, stay tuned")

            # Set constant for valid subcarriers
            length_angles_users_bits = NSUBC_VALID * tot_bits_users
            length_angles_users = math.floor(length_angles_users_bits / 8)

            # Extract specific fields for AX or AC standard
            if standard == "AX":
                Feedback_angles = packet[(i + 62 + 2 * int(config[-1])):(len(packet) - 8)]
                Feedback_angles_splitted = np.array(wrap(Feedback_angles, 2))
                Feedback_angles_bin = ""
            if standard == "AC":
                # Feedback_angles = packet[(i + 60):(i + 60 + (length_angles_users * 2))]
                Feedback_angles = packet[(i + 58 + 2 * int(config[-1])):(len(packet) - 8)]
                # bfm_report_length = packet[(i + 60 + length_angles_users * 2):(len(packet) - 8)]
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

            if Feed_back_angles_bin_chunk.shape[0] != NSUBC_VALID:
                print(Feed_back_angles_bin_chunk.shape[0])
                print('FILE NAME: ', file_name, 'bandwidth different than expected')
                continue
            bfi_angles_single_pkt = bfi_angles(Feed_back_angles_bin_chunk, LSB, NSUBC_VALID, order_bits)
            # bfi_angles_all_packets.append(bfi_angles_single_pkt)

            for angle_id in range(0, num_parallel_processes):
                queues_plot[angle_id].put(bfi_angles_single_pkt[:, angle_id])

            reader.close()
