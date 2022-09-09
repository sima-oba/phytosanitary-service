from dataclasses import dataclass, asdict
from dacite import from_dict
from datetime import datetime
from uuid import uuid4


@dataclass
class Model:
    _id: str
    created_at: datetime
    updated_at: datetime

    def asdict(self) -> dict:
        return asdict(self)

    def merge(self, data: dict):
        return from_dict(
            data_class=self.__class__,
            data={
                **asdict(self),
                'updated_at': datetime.utcnow(),
                **data
            }
        )

    @classmethod
    def new(cls, data: dict):
        return from_dict(
            data_class=cls,
            data={
                '_id': str(uuid4()),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                **data
            }
        )

    @classmethod
    def from_dict(cls, data: dict):
        return from_dict(data_class=cls, data=data)
