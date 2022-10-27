from datetime import datetime
from pymongo.database import Database
from pymongo import DESCENDING
from typing import List, Optional

from domain.model import Visit
from domain.repository import IVisitRepository


class VisitRepository(IVisitRepository):
    def __init__(self, db: Database):
        self._collection = db.get_collection('visit')

    def find_all(self) -> List[Visit]:
        docs = self._collection.find()
        
        return [Visit.from_dict(doc) for doc in docs]

    def find_by_farm(self, farm_id: str) -> List[Visit]:
        docs = self._collection.find({'farm_id': farm_id})

        return [
            Visit.from_dict(doc) for doc
            in docs.sort('visit_date', DESCENDING)
        ]

    def find_by_date(self, farm_id: str, date: datetime) -> Optional[Visit]:
        doc = self._collection.find_one({
            'farm_id': farm_id,
            'visit_date': date
        })

        return Visit.from_dict(doc) if doc else None

    def add(self, visit: Visit) -> Visit:
        result = self._collection.insert_one(visit.asdict())
        visit._id = result.inserted_id

        return visit

    def update(self, visit: Visit) -> Optional[Visit]:
        doc = visit.asdict()
        result = self._collection.replace_one({'_id': visit._id}, doc)

        return visit if result.matched_count > 0 else None
