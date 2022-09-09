from dataclasses import dataclass
from typing import List, Optional

from .model import Model


@dataclass
class Visit(Model):
    farm_id: str
    crop_type: Optional[str]
    visit_date: Optional[str]
    seeding_date: Optional[str]
    harvest_date: Optional[str]
    plagues: List[str]
    notes: Optional[str]
