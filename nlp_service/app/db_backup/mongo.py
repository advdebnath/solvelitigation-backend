from pymongo import MongoClient
from gridfs import GridFS
from app.config import settings

_client = None
_db = None
_fs = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGO_URI)
    return _client


def get_db():
    global _db
    if _db is None:
        _db = get_client()[settings.MONGO_DB]
    return _db


def get_gridfs() -> GridFS:
    global _fs
    if _fs is None:
        _fs = GridFS(get_db())
    return _fs
