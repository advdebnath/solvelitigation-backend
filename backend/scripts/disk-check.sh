#!/bin/bash
AVAIL=$(df / | awk 'NR==2 {print $4}')
MIN=5242880   # 5GB

if [ "$AVAIL" -lt "$MIN" ]; then
  echo "$(date) ❌ Disk low, aborting inbox scan" >> /var/www/solvelitigation/backend/logs/inbox-scan.log
  exit 1
fi
