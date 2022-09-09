from abc import ABC, abstractmethod
from typing import List

from domain.model import AnnualOrdinance


class IOrdinanceRepository(ABC):
    @abstractmethod
    def find_all(self) -> List[AnnualOrdinance]:
        pass

    @abstractmethod
    def add(self, entity: AnnualOrdinance) -> AnnualOrdinance:
        pass

    @abstractmethod
    def remove_all(self) -> List[str]:
        pass
