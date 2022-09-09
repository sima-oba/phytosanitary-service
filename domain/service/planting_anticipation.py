import logging
from typing import List, Dict, IO

from domain.model import PlantingAnticipation
from domain.exception import EntityNotFoundError
from domain.repository import IPlantingAnticipationRepository, IStorage


_log = logging.getLogger(__name__)


class PlantingAnticipationService:
    def __init__(
        self,
        repo: IPlantingAnticipationRepository,
        storage: IStorage
    ):
        self._repo = repo
        self._storage = storage

    def _write_pdf_files(self, files: dict) -> dict:
        references = {}

        for filename, file in files.items():
            ref = self._storage.write(file, filename + '.pdf')
            references[f'{filename}_ref'] = ref

        return references

    def get_all(self) -> List[PlantingAnticipation]:
        return self._repo.find_all()

    def add(self, data: dict, files: Dict[str, IO]) -> PlantingAnticipation:
        file_refs = self._write_pdf_files(files)

        entity = PlantingAnticipation.new({
            **data,
            **file_refs,
            'status': 'REVIEW',
            'position': {
                'type': 'Point',
                'coordinates': [data.pop('longitude'), data.pop('latitude')]
            }
        })
        entity = self._repo.add(entity)
        _log.debug(f'added planting anticipation {entity._id}')

        return entity

    def change_status(self, data: dict, id: str):
        entity = self._repo.find_by_id(id)

        if entity is None:
            raise EntityNotFoundError(PlantingAnticipation, f'_id {id}')

        entity = self._repo.update(entity.merge(data))
        _log.debug(f'status of planting anticipation {id} changed')

        return entity
