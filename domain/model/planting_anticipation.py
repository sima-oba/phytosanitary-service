from dataclasses import dataclass
from typing import List, Optional

from .model import Model
from .geo import Geometry


@dataclass
class PlantingAnticipation(Model):
    farm_id: str
    owner_name: str
    cpf_cnpj: str
    address: str
    nucleos: str
    cep: str
    city: str
    state: str
    phones: List[str]
    email: Optional[str]
    farm_name: Optional[str]
    position: Geometry
    notes: Optional[str]
    status: str

    # File references
    rg_cnpj_ref: str
    attorney_letter_ref: Optional[str]
    commitment_ref: str
    sketch_ref: str
    soy_planting_ref: str
    art_ref: str
    work_plan_ref: str
    ordinance_ref: Optional[str]
