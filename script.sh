#!/bin/bash
wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
