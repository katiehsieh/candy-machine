#!/bin/bash

sudo pigpiod

export FLASK_APP=candy-machine-app.py
python3 -m flask run
