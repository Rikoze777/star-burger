#!/bin/bash

set -e
cd /opt/star-burger
git pull
. ./venv/bin/activate
pip install -r requirements.txt
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --publ>

python manage.py collectstatic --noinput
python manage.py migrate --noinput

systemctl restart burger.service
systemctl reload nginx.service

echo Successful
