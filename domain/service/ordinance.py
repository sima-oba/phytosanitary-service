import logging
from typing import List, BinaryIO

from domain.model import AnnualOrdinance
from domain.repository import IOrdinanceRepository, IFileRepository


_log = logging.getLogger(__name__)


class OrdinanceService:
    def __init__(
        self,
        ordinances: IOrdinanceRepository,
        files: IFileRepository
    ):
        self._ordinances = ordinances
        self._files = files

    def get_all(self) -> List[AnnualOrdinance]:
        return self._ordinances.find_all()

    def get_document(self, id: str) -> BinaryIO:
        file = self._files.open(id)

        if file is None:
            raise FileNotFoundError(f"Ordinance's document {id} not found")

        return file

    def save(self, data: dict) -> AnnualOrdinance:
        # We want to keep only the most recent ordinance
        removed_ids = self._ordinances.remove_all()

        for id in removed_ids:
            self._files.remove(id)

        ordinance = AnnualOrdinance.new({
            'publish_date': data['publish_date'],
            'link':         data['link']
        })
        ordinance = self._ordinances.add(ordinance)
        self._files.write(ordinance._id, data['content'])

        _log.debug(f'added annual ordinance {ordinance._id}')
        return ordinance
