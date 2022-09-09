from dacite import from_dict
from pymongo.database import Collection
from typing import Generic, TypeVar, Optional, Type, List

from domain.model.model import Model


T = TypeVar('T', bound=Model)


class BaseRepository(Generic[T]):
    def __init__(self, cls: Type[T], collection: Collection):
        self._cls = cls
        self.collection = collection

    def _as_entity(self, doc: dict) -> T:
        return from_dict(data_class=self._cls, data=doc)

    def _as_list(self, cursor: any) -> List[T]:
        return [self._as_entity(it) for it in cursor]

    def aggregate(self, pipeline: List[dict]) -> List[T]:
        docs = self.collection.aggregate(pipeline)
        return self._as_list(docs)

    def find_all(self, filter: dict = None) -> List[T]:
        docs = self.collection.find(filter)
        return self._as_list(docs)

    def find_one(self, filter: dict) -> Optional[T]:
        doc = self.collection.find_one(filter)
        return self._as_entity(doc) if doc else None

    def find_by_id(self, id: str) -> Optional[T]:
        return self.find_one({'_id': id})

    def add(self, entity: T, **kwargs) -> T:
        result = self.collection.insert_one({**entity.asdict(), **kwargs})
        entity._id = result.inserted_id
        return entity

    def update(self, entity: T, **kwargs) -> Optional[T]:
        result = self.collection.update_one(
            {'_id': entity._id},
            {'$set': {**entity.asdict(), **kwargs}}
        )
        return entity if result.matched_count > 0 else None

    def remove(self, id: str) -> bool:
        result = self.collection.delete_one({'_id': id})
        return result.deleted_count > 0
