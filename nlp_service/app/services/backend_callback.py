import requests
import logging

logger = logging.getLogger(__name__)

def notify_backend(url: str, payload: dict):
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        logger.error(f"Backend callback failed: {e}")
