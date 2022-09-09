from marshmallow import Schema, fields, validate, post_load


_phone_regex = r'^(\d{10,11})$'


class PlantingAnticipationSchema(Schema):
    farm_id = fields.String(required=True)
    owner_name = fields.String(required=True)
    cpf_cnpj = fields.String(
        validate=validate.Regexp(r'^\d{11}$|^\d{14}'),
        required=True
    )
    address = fields.String(required=True)
    nucleos = fields.String(required=True)
    cep = fields.String(
        validate=validate.Regexp(r'^\d{8}'),
        required=True
    )
    city = fields.String(required=True)
    state = fields.String(required=True)
    email = fields.Email(required=True)
    farm_name = fields.String(missing=None)
    latitude = fields.Float(
        validate=validate.Range(min=-90, max=90),
        required=True
    )
    longitude = fields.Float(
        validate=validate.Range(min=-180, max=180),
        required=True
    )
    phone = fields.String(
        validate=validate.Regexp(_phone_regex),
        required=True
    )
    cellphone = fields.String(
        validate=validate.Regexp(_phone_regex),
        required=True
    )

    @post_load
    def format(self, data: dict, **kwargs) -> dict:
        data['phones'] = [data.pop('phone'), data.pop('cellphone')]
        return data


class PlantingAnticipationStatus(Schema):
    status = fields.String(
        validate=validate.OneOf(('REVIEW', 'GRANTED', 'DENIED')),
        required=True
    )
    notes = fields.String(missing=None)
    ordinance_ref = fields.String(required=True)
