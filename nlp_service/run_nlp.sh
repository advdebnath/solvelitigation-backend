#!/bin/bash

cd /var/www/solvelitigation/nlp_service

source .venv/bin/activate

exec python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
