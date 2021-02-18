#!/bin/zsh

. .venv/bin/activate
export APP_CONFIG_FILE=$(pwd)/config/development.py
export FLASK_ENV=development
flask run