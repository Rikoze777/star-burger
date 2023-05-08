#!/bin/bash

set -e
cd /opt/star-burger
git pull
. ./venv/bin/activate
pip install -r requirements.txt
npm ci --dev
./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

python manage.py collectstatic --noinput
python manage.py migrate --noinput

systemctl restart burger.service
systemctl reload nginx.service
token=$(access_token)
username=$(rollbar_user)
last_commit=$(git rev-parse HEAD)
curl -H "X-Rollbar-Access-Token: '${token}'" \
     -H "Content-Type: application/json" \
     -X POST 'https://api.rollbar.com/api/1/deploy' \
     -d '{"environment": "production", "revision": "'${last_commit}'", "rollbar_username": "'${username}'", "status": "succeeded"}'

echo Successful
