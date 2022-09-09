from pymongo.database import Database
from typing import List

from domain.model import Farm
from domain.repository import IFarmRepository
from .base import BaseRepository


class FarmRepository(BaseRepository[Farm], IFarmRepository):
    def __init__(self, db: Database):
        super().__init__(Farm, db['farm'])

    def find_by_imported_id(self, id: str) -> Farm:
        return self.find_one({'imported_id': id})

    def find_nearby(self, lat: float, lng: float, rad: float) -> List[Farm]:
        return self.aggregate([
            {
                '$geoNear': {
                    'near': {
                        'type': "Point",
                        'coordinates': [lng, lat]
                    },
                    'spherical': True,
                    'distanceField': "dist.calculated",
                    'maxDistance': rad
                }
            }
        ])

    def search(self, filter: dict) -> List[Farm]:
        return self.find_all(filter)
