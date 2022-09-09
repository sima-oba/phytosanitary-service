from datetime import datetime
from flask.json import JSONEncoder


class CustomJsonEncoder(JSONEncoder):
    def default(self, obj: any) -> str:
        if isinstance(obj, datetime):
            return obj.isoformat()

        return super().default(obj)
