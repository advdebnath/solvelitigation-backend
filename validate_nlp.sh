#!/bin/bash

echo "=== COMPILE ==="

python3 -m py_compile \
/var/www/solvelitigation/nlp_service/app/extractors/judge_extractor.py || exit 1

python3 -m py_compile \
/var/www/solvelitigation/nlp_service/app/tasks/judgment_task.py || exit 1

echo "=== IMPORT TEST ==="

cd /var/www/solvelitigation/nlp_service

python3 - <<'PY'
import app.extractors.judge_extractor
import app.tasks.judgment_task

print("IMPORT_OK")
PY

echo "=== SUCCESS ==="
