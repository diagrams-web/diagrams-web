#!/usr/bin/env ash

echo -e "\e[34m >>> Generate cache \e[97m"
python3 helpers.py
echo -e "\e[32m >>> Generation completed \e[97m"

echo -e "\e[32m >>> Start gunicorn \e[97m"
gunicorn -b 0.0.0.0:8000 --workers=3 'app:app'
