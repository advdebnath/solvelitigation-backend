#!/bin/bash

cd /var/www/solvelitigation/nlp_service

source .venv/bin/activate

exec celery -A app.celery_app worker --loglevel=info --pool=solo
