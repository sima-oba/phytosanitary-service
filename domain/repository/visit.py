from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from domain.model import Visit


class IVisitRepository(ABC):
    @abstractmethod
    def find_all(self) -> List[Visit]:
        pass

    @abstractmethod
    def find_by_farm(self, farm_id: str) -> List[Visit]:
        pass

    @abstractmethod
    def find_by_date(self, farm_id: str, date: datetime) -> Optional[Visit]:
        pass

    @abstractmethod
    def add(self, visit: Visit) -> Visit:
        pass

    @abstractmethod
    def update(self, visit: Visit) -> Optional[Visit]:
        pass
