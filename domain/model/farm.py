from dataclasses import dataclass
from typing import Optional

from .model import Model
from .geo import Geometry


@dataclass
class Farm(Model):
    imported_id: str
    name: str
    address: Optional[str]
    city: Optional[str]
    classification: Optional[str]
    nucleos: Optional[str]
    owner: Optional[str]
    owner_name: str

    cultivation_system: Optional[str]
    irrigation_system: Optional[str]
    dryland_area: Optional[int]
    irrigated_area: Optional[int]
    geometry: Geometry
