#!/usr/bin/env ash

# generate help menu template
python3 helpers.py

# start the app
python3 app.py

# install editor library
npm install --prefix ./static/js ace-builds@1.11.2