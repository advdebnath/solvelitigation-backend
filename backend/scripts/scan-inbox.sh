#!/bin/bash

API="https://solvelitigation.com/api/judgments/upload-bulk"
COOKIE="/var/www/solvelitigation/backend/cookies.txt"
LOG="/var/www/solvelitigation/backend/logs/inbox-scan.log"

bash /var/www/solvelitigation/backend/scripts/disk-check.sh || exit 1

echo "---- $(date) scan started ----" >> $LOG

curl -s -X POST "$API" \
  -b "$COOKIE" \
  >> $LOG 2>&1

echo "---- $(date) scan finished ----" >> $LOG
