from marshmallow import Schema, fields


class FarmQuery(Schema):
    name = fields.String()
    classification = fields.String()
    nucleos = fields.String()
    owner = fields.String()


class FarmNearbyQuery(Schema):
    lat = fields.Float(required=True)
    lng = fields.Float(required=True)
    rad = fields.Float(required=True)
