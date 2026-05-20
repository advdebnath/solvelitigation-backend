#!/bin/bash

cd /var/www/solvelitigation/nlp_service

# ✅ FIX PYTHON PATH
export PYTHONPATH=/var/www/solvelitigation/nlp_service

# Activate venv
source /var/www/solvelitigation/nlp_service/.venv/bin/activate

# Run uvicorn (foreground)
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
