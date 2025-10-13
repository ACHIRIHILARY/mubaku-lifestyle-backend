#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

cd app
python manage.py collectstatic --noinput --settings=mubaku.settings.prod
python manage.py migrate --settings=mubaku.settings.prod