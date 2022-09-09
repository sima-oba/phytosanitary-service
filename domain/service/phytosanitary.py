import logging
from typing import List, Tuple

from domain.model import Visit, Farm
from domain.exception import EntityNotFoundError
from domain.repository import IVisitRepository, IFarmRepository


class PhytosanitaryService:
    def __init__(
        self,
        visits: IVisitRepository,
        farms: IFarmRepository
    ):
        self._visits = visits
        self._farms = farms
        self._log = logging.getLogger(self.__class__.__name__)

    def search_farms(self, filter: dict) -> List[Farm]:
        return self._farms.search(filter)

    def search_farms_nearby(self, query: dict) -> List[Farm]:
        return self._farms.find_nearby(**query)

    def get_visits(self, farm_id: str = None) -> List[Visit]:
        if farm_id is None:
            return self._visits.find_all()

        farm = self._farms.find_by_id(farm_id)

        if farm is None:
            raise EntityNotFoundError(Farm, f'_id {farm_id}')

        return self._visits.find_by_farm(farm._id)

    def save(self, data: dict) -> Tuple[Farm, Visit]:
        farm = self._farms.find_by_imported_id(data['imported_id'])
        # new_farm = {
        #     'imported_id':          data['imported_id'],
        #     'name':                 data['farm_name'],
        #     'address':              data['address'],
        #     'city':                 data['city'],
        #     'classification':       data['classification'],
        #     'nucleos':              data['nucleos'],
        #     'cultivation_system':   data['cultivation_system'],
        #     'irrigation_system':    data['irrigation_system'],
        #     'dryland_area':         data['dryland_area'],
        #     'irrigated_area':       data['irrigated_area'],
        #     'owner':                data['owner'],
        #     'owner_name':           data['owner_name'],
        #     'geometry':             data['geometry']
        # }

        # if old_farm is None:
        #     farm = self._farms.add(Farm.new(new_farm))
        #     self._log.debug(f'added farm {farm._id}')
        # else:
        #     farm = self._farms.update(old_farm.merge(new_farm))
        #     self._log.debug(f'updated farm {farm._id}')

        old_visit = self._visits.find_by_date(farm._id, data['visit_date'])
        new_visit = {
            'farm_id':      farm._id,
            'crop_type':    data['crop_type'],
            'visit_date':   data['visit_date'],
            'seeding_date': data['seeding_date'],
            'harvest_date': data['harvest_date'],
            'plagues':      data['plagues'],
            'notes':        data['notes']
        }

        if old_visit is None:
            visit = self._visits.add(Visit.new(new_visit))
            self._log.debug(f'added visit {visit._id}')
        else:
            visit = self._visits.update(old_visit.merge(new_visit))
            self._log.debug(f'updated visit {visit._id}')

        return farm, visit
