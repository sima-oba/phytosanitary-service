import logging
from typing import List, BinaryIO

from domain.model import Report
from domain.exception import EntityNotFoundError
from domain.repository import IReportRepository, IStorage

_log = logging.getLogger(__name__)


class ReportService:
    def __init__(self, repo: IReportRepository, storage: IStorage):
        self._repo = repo
        self._storage = storage

    def get_all(self, filter: dict = None) -> List[Report]:
        return self._repo.find_all(filter)

    def get_by_id(self, id: str) -> Report:
        report = self._repo.find_by_id(id)

        if report is None:
            raise EntityNotFoundError(Report, f'_id {id}')

        return report

    def add(self, data: dict, file: BinaryIO) -> Report:
        occurrence_photo = self._storage.write(file, 'occurrence.jpg')
        report = Report.new({
            'reporter':              data.get('reporter'),
            'area':                  data['area'],
            'location':              data['location'],
            'occurrence_type':       data['occurrence_type'],
            'occurrence_date':       data['occurrence_date'],
            'occurrence_photo_href': occurrence_photo,
            'resolved_date':         None,
            'resolved_photo_href':   None,
            'notes':                 None,
            'position': {
                'type': 'Point',
                'coordinates': [data['longitude'], data['latitude']]
            }
        })
        report = self._repo.add(report)
        _log.debug(f'added Report {report._id}')

        return report

    def mark_as_resolved(self, id: str, data: dict, file: BinaryIO) -> Report:
        report = self.get_by_id(id)
        resolved_photo = self._storage.write(file, 'resolved_occurrence.jpg')
        report = report.merge({
            'notes':               data['notes'],
            'resolved_date':       data['resolved_date'],
            'resolved_photo_href': resolved_photo
        })
        self._repo.update(report)
        _log.debug(f'Report {report._id} has been resolved')

        return report
