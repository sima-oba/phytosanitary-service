from abc import ABC, abstractmethod
from typing import List, Optional

from domain.model import Report


class IReportRepository(ABC):
    @abstractmethod
    def find_all(self, filter: Optional[dict]) -> List[Report]:
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[Report]:
        pass

    @abstractmethod
    def add(self, report: Report) -> Report:
        pass

    @abstractmethod
    def update(self, report) -> Report:
        pass
