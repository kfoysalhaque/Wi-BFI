#!/bin/bash

# Copyright (C) 2023 Francesca Meneghello
# contact: francesca.meneghello.1@unipd.it
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


folder_name=$1

interface=$2  # wlp3s0

channel=$3  # 60

BW=$4  # 80MHz

seconds_interval=$5 # 1

trap "sudo airmon-ng stop ${interface}mon" EXIT

# go to the current directory
cd "$(dirname "$0")"

# sleep one second just in case
sleep 1

# create the folder to storage the angle data
mkdir $folder_name
chmod 777 ./$folder_name

# set mode monitor
echo "Setting the interface in monitor mode"

sudo airmon-ng start $interface

sudo iw dev ${interface}mon set channel $channel $BW

# collect the angle data
echo "Collecting"

# name=0
# while true ; do
# name=$((name + 1))
# create the file
# touch ./traces/$folder_name/${name}/
# chmod 777 ./traces/$folder_name/${name}/
# sudo tcpdump -i wlp3s0mon -w ./traces/$folder_name/${name}/
# done

# [ -G rotate_seconds ] If specified, rotates the dump file specified with the -w option every rotate_seconds seconds. 
# [ -C file_size ] Before writing a raw packet to a savefile, check whether the file is currently larger than file_size and, if so, close the current savefile and open a new one. Savefiles after the first savefile will have the name specified with the -w flag, with a number after it, starting at 1 and continuing upward
# [ -W filecount ] Used in conjunction with the -C option, this will limit the number of files created to the specified number, and begin overwriting files from the beginning, thus creating a 'rotating' buffer. In addition, it will name the files with enough leading 0s to support the maximum number of files, allowing them to sort correctly.
# [ -K ] Don't attempt to verify IP, TCP, or UDP checksums. 
# [ -n ] Don't convert host addresses to names. This can be used to avoid DNS lookups.

date '+%s' > ./$folder_name/start_time.txt

sudo tcpdump -i ${interface}mon -w ./$folder_name/%s -G $seconds_interval -K -n
