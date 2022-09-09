import base64
from marshmallow import Schema, fields, post_load


class AnnualOrdinanceSchema(Schema):
    publish_date = fields.DateTime(format="%d/%m/%Y")
    content = fields.String(data_key='file', required=True)
    link = fields.String(missing=None)

    @post_load
    def format(self, data: dict, **kwargs) -> dict:
        data['content'] = base64.b64decode(data['content'])
        return data
