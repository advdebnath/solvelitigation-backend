#!/bin/bash

cd /var/www/solvelitigation/nlp_service

source .venv/bin/activate

# kill any previous uvicorn instances
pkill -9 -f "uvicorn app.main:app"

# wait for port to free
sleep 3

# start fresh
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1
