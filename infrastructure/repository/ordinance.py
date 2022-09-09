from pymongo.database import Database
from typing import List

from domain.model import AnnualOrdinance
from domain.repository import IOrdinanceRepository
from .base import BaseRepository


class OrdinanceRepository(
    BaseRepository[AnnualOrdinance], IOrdinanceRepository
):
    def __init__(self, db: Database):
        super().__init__(AnnualOrdinance, db['annual_ordinance'])

    def remove_all(self) -> List[str]:
        ids = [doc['_id'] for doc in self.collection.find()]
        self.collection.delete_many({})
        return ids
