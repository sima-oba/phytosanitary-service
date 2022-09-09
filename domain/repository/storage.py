from abc import ABC, abstractmethod
from typing import Union, IO, Optional


class IStorage(ABC):
    @abstractmethod
    def write(
        self,
        data: Union[bytes, IO],
        filename: str,
        key: Optional[str]
    ) -> str:
        pass

    @abstractmethod
    def open(self, key: str) -> Optional[IO]:
        pass

    @abstractmethod
    def remove(self, key):
        pass
