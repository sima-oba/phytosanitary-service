from typing import Union, IO
from pymongo.database import Database
from gridfs import GridFS

from domain.repository import IFileRepository


class FileRepository(IFileRepository):
    def __init__(self, db: Database):
        self._fs = GridFS(db, 'file')

    def write(self, id: str, data: Union[bytes, IO]) -> str:
        return self._fs.put(data, _id=id)

    def open(self, id: str) -> IO:
        return self._fs.find_one(id)

    def read(self, id: str) -> bytes:
        return self.open(id).read()

    def remove(self, id):
        return self._fs.delete(id)
