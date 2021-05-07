#!/bin/sh
gpsctl -c 0.2
source /home/pi/venv/racing-data-logger/bin/activate
python ./launch.py
