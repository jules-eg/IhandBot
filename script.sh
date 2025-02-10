#!/bin/bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz
tar -xvzf geckodriver-v0.35.0-linux64.tar.gz
chmod +x geckodriver
sudo apt-get remove --purge firefox
sudo apt-get install firefox
sudo apt install firefox=123.0
pip install -r requirements.txt
ls -a
