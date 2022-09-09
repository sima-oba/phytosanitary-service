from dataclasses import dataclass
from datetime import datetime

from .model import Model


@dataclass
class AnnualOrdinance(Model):
    publish_date: datetime
    link: str
