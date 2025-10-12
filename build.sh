#!/usr/bin/env bash
# exit on error
set -o errexit

cd app

pip install --upgrade pip
pip install -r ../requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
