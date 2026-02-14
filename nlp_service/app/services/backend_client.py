import requests
from typing import Dict


class BackendClient:
    def __init__(self, callback_url: str):
        self.callback_url = callback_url.rstrip("/")

    def send_status(self, payload: Dict):
        try:
            resp = requests.post(
                self.callback_url,
                json=payload,
                timeout=10,
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            raise RuntimeError(f"Backend callback failed: {e}")
