#!/bin/bash

sudo apt-get update
sudo apt-get install python-pip python-dev build-essential

cp NewsSpectrum/example_runapp.py runapp.py
mkworkspace PyNewsSpec
pip install -r NewsSpectrum/pip_requirements.txt
pip install gunicorn supervisor
cat >simple.conf <<EOF
[program:myserver]
command gunicorn runapp:app -w 4 -b 0.0.0.0:80

[supervisord]
logfile=/home/ubuntu/supervisord.log
loglevel=DEBUG
user=root
EOF
