#!/bin/bash

STATUS=$(curl -s http://127.0.0.1:8000/health)

if [[ $STATUS != *"ok"* ]]; then
  echo "❌ NLP API DOWN - Restarting..."
  pm2 restart sl-nlp-api
fi
