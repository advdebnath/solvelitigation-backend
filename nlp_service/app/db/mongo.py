from pymongo import MongoClient
from typing import Optional

MONGO_URI = "mongodb://sl_app:Debnath%401966@127.0.0.1:27017/solvelitigation"

_client: Optional[MongoClient] = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client


def get_db():
    return get_client()["solvelitigation"]


def close_client():
    global _client
    if _client:
        _client.close()
        _client = None
