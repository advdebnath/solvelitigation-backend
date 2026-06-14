import json
from pathlib import Path

REGISTRY_FILE = Path(
    "/var/www/solvelitigation/nlp_service/app/data/act_registry.json"
)

def load_act_registry():

    try:

        with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:

        print("❌ ACT REGISTRY LOAD FAILED")
        print(e)

        return []
