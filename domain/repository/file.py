from typing import Union, IO


class IFileRepository:
    def write(self, id: str, data: Union[bytes, IO]) -> str:
        pass

    def read(self, id: str) -> bytes:
        pass

    def open(self, id: str) -> IO:
        pass

    def remove(self, id):
        pass
