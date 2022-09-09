from marshmallow import Schema, fields, EXCLUDE, post_load

from .constants import plagues


class PhytosanitarySchema(type('_PhytosanitarySchema', (Schema,), {
    key: fields.Field(data_key=value, missing=None)
    for key, value in plagues.items()
})):
    class Meta:
        unknown = EXCLUDE
    imported_id = fields.String(data_key='GlobalID', required=True)
    farm_name = fields.String(data_key='Nome da Prorpriedade', required=True)
    address = fields.String(data_key='Endereço da Propriedade', missing=None)
    city = fields.String(data_key='Município', missing=None)
    classification = fields.String(
        data_key='Classificação do produtor',
        missing=None
    )
    nucleos = fields.String(
        data_key='Núcleo',
        missing=None)
    owner = fields.Number(data_key='CPF/CNPJ', missing=None)
    owner_name = fields.String(data_key='Nome do Proprietário', required=True)
    cultivation_system = fields.String(
        data_key='Sistema de cultivo da Soja',
        missing=None
    )
    irrigation_system = fields.String(
        data_key='Sistema de cultivo Irrigado',
        missing=None
    )
    dryland_area = fields.Integer(data_key='Área sequeiro (ha)', missing=None)
    irrigated_area = fields.Integer(
        data_key='Área Irrigado (ha)', missing=None
    )
    crop_type = fields.String(data_key='Tipo plantado', missing=None)
    notes = fields.String(data_key='Observações', missing=None)
    visit_date = fields.String(data_key='Primeira Visita', missing=None)
    seeding_date = fields.String(
        data_key='Data da semeadura',
        missing=None
    )
    harvest_date = fields.String(
        data_key='Data provável de colheita',
        missing=None
    )
    latitude = fields.Float(data_key='y', required=True)
    longitude = fields.Float(data_key='x', required=True)

    @post_load
    def format(self, data: dict, **kwargs) -> dict:
        items = []

        for key, value in plagues.items():
            plague = data.pop(key)

            if plague is not None:
                items.append(value)

        data['owner'] = str(data['owner'])
        data['plagues'] = items
        data['geometry'] = {
            'type': 'Point',
            'coordinates': [data.pop('longitude'), data.pop('latitude')]
        }

        return data
