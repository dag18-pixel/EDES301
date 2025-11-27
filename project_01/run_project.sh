#!/bin/bash

# This script runs the stethoscope project

#1. Change to the correct project directory
cd /var/lib/cloud9/EDES301/project_01

#2. Export the path to the Python libraries
export PYTHONPATH=/usr/local/lib/python3.7/dist-packages:$PYTHONPATH

#3. Call the main Python script
# We use python3 because that's what your script needs
python3 OLED.py 
