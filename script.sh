#!/bin/bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz
tar -xvzf geckodriver-v0.35.0-linux64.tar.gz
chmod +x geckodriver
apt-get remove --purge firefox -y
apt install firefox
PATH=$PATH:$(pwd)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
