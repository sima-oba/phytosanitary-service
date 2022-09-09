from pymongo.database import Database

from domain.model import Report
from domain.repository import IReportRepository
from .base import BaseRepository


class ReportRepository(BaseRepository[Report], IReportRepository):
    def __init__(self, db: Database):
        super().__init__(Report, db['report'])
