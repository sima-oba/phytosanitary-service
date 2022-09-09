from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .model import Model
from .geo import Geometry


@dataclass
class Report(Model):
    reporter: Optional[str]
    area: float
    location: str
    occurrence_type: str
    occurrence_date: datetime
    occurrence_photo_href: str
    resolved_date: Optional[datetime]
    resolved_photo_href: Optional[str]
    position: Geometry
    notes: Optional[str]
