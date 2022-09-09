from pymongo.database import Database
from pymongo import DESCENDING
from typing import List

from domain.model import PlantingAnticipation
from domain.repository import IPlantingAnticipationRepository
from .base import BaseRepository


class PlantingAnticipationRepository(
    BaseRepository[PlantingAnticipation], IPlantingAnticipationRepository
):
    def __init__(self, db: Database):
        super().__init__(PlantingAnticipation, db['planting_anticipation'])

    def find_all(self) -> List[PlantingAnticipation]:
        docs = self.collection.find().sort('updated_at', direction=DESCENDING)
        return self._as_list(docs)
