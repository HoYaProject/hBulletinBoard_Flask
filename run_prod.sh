#!/bin/zsh

. .venv/bin/activate
export APP_CONFIG_FILE=$(pwd)/config/production.py
export FLASK_ENV=production
flask run