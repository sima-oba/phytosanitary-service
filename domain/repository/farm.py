from abc import ABC, abstractmethod
from typing import List

from domain.model import Farm


class IFarmRepository(ABC):
    @abstractmethod
    def find_all(self) -> List[Farm]:
        pass

    @abstractmethod
    def find_by_id(self, farm_id: str) -> Farm:
        pass

    @abstractmethod
    def find_by_imported_id(self, id: str) -> Farm:
        pass

    @abstractmethod
    def find_nearby(self, lat: float, lng: float, rad: float) -> List[Farm]:
        pass

    @abstractmethod
    def search(self, filter: dict) -> List[Farm]:
        pass

    @abstractmethod
    def add(self, farm: Farm) -> Farm:
        pass

    @abstractmethod
    def update(self, farm: Farm) -> Farm:
        pass
