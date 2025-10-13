#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python app/manage.py collectstatic --noinput --settings=mubaku.settings.prod
python app/manage.py migrate --settings=mubaku.settings.prod