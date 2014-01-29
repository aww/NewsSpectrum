#!/bin/bash

sudo apt-get update
sudo apt-get install python-pip python-dev build-essential libxml2-dev libxslt-dev libmysqlclient-dev libssl-dev
#sudo pip install virtualenv

cp NewsSpectrum/example_runapp.py runapp.py

#virtualenv PyNewsSpec
#source PyNewsSpec/bin/activate
sudo pip install --allow-external mysql-connector-python --allow-insecure mysql-connector-python -r NewsSpectrum/pip_requirements.txt
#sudo pip install --allow-external mysql-connector-python --allow-unverified mysql-connector-python -r NewsSpectrum/pip_requirements.txt
git clone https://github.com/nltk/nltk_contrib.git
pushd nltk_contrib
sudo python setup.py install
popd

cat >simple.conf <<EOF
[program:myserver]
command gunicorn runapp:app -w 4 -b 0.0.0.0:80

[supervisord]
logfile=/home/ubuntu/supervisord.log
loglevel=DEBUG
user=root
EOF
