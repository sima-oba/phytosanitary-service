from abc import ABC, abstractmethod
from typing import List, Optional

from domain.model import PlantingAnticipation


class IPlantingAnticipationRepository(ABC):
    @abstractmethod
    def find_all(self) -> List[PlantingAnticipation]:
        pass

    @abstractmethod
    def find_by_id(self, id: str) -> Optional[PlantingAnticipation]:
        pass

    @abstractmethod
    def add(self, entity: PlantingAnticipation) -> PlantingAnticipation:
        pass

    @abstractmethod
    def update(self, entity) -> PlantingAnticipation:
        pass
