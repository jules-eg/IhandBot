#!/bin/bash
# Télécharger et installer geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz
tar -xvzf geckodriver-v0.35.0-linux64.tar.gz
chmod +x geckodriver
mv geckodriver /usr/local/bin/  # Déplace geckodriver dans un dossier accessible globalement

# Installer les dépendances Python
pip install -r requirements.txt
