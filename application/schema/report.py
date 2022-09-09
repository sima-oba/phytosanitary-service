from marshmallow import Schema, fields
from marshmallow.validate import Range, OneOf


_occurrence_types = ('FALLOW', 'RUST')


class NewOccurrenceSchema(Schema):
    occurrence_type = fields.String(
        validate=OneOf(_occurrence_types), required=True
    )
    occurrence_date = fields.DateTime(required=True)
    area = fields.Float(required=True)
    location = fields.String(required=True)
    latitude = fields.Float(validate=Range(min=-90.0, max=90.0), required=True)
    longitude = fields.Float(
        validate=Range(min=-180.0, max=180.0), required=True
    )


class ResolvedOccurrenceSchema(Schema):
    resolved_date = fields.DateTime(required=True)
    notes = fields.String(required=True)


class OccurrenceQuery(Schema):
    occurrence_type = fields.String(validate=OneOf(_occurrence_types))
    username = fields.String(missing=None)
