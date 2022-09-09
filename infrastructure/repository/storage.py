from flask import request
from gridfs import GridFS
from gridfs.grid_file import GridOut
from pymongo.database import Database
from typing import Union, IO, Optional
from uuid import uuid4

from domain.repository import IStorage


class LocalStorage(IStorage):
    def __init__(self, db: Database, path: str):
        self._fs = GridFS(db, 'file')
        self._path = path

    def write(
        self,
        data: Union[bytes, IO],
        filename: str,
        key: str = None
    ) -> str:
        key = key or str(uuid4())
        self._fs.put(data, filename=filename, _id=key)
        return f'{request.root_url.rstrip("/")}{self._path}/{key}'

    def open(self, key: str) -> Optional[GridOut]:
        return self._fs.find_one(key)

    def remove(self, key):
        return self._fs.delete(key)
