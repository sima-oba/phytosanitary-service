from flask import Blueprint, jsonify, request
from http import HTTPStatus

from application.schema import (
    PlantingAnticipationSchema,
    PlantingAnticipationStatus
)
from domain.service import PlantingAnticipationService
from . import utils
from ..security import Authorization, Role


def get_blueprint(
    auth: Authorization,
    service: PlantingAnticipationService
) -> Blueprint:
    bp = Blueprint('PlantingAnticipation', __name__)
    schema = PlantingAnticipationSchema()
    statusSchema = PlantingAnticipationStatus()

    @auth.require_role(Role.WRITE_PROTOCOLS)
    @bp.get('/planting_anticipation')
    def get_all():
        return jsonify(service.get_all())

    @auth.require_role(Role.WRITE_PROTOCOLS)
    @bp.post('/planting_anticipation')
    def add():
        data = schema.load(request.form)
        files = {
            'rg_cnpj': utils.get_file('rg_cnpj', 'application/pdf'),
            'commitment': utils.get_file('commitment', 'application/pdf'),
            'sketch': utils.get_file('sketch', 'application/pdf'),
            'soy_planting': utils.get_file('soy_planting', 'application/pdf'),
            'art': utils.get_file('art', 'application/pdf'),
            'work_plan': utils.get_file('work_plan', 'application/pdf')
        }

        if 'attorney_letter' in request.files:
            files['attorney_letter'] = utils.get_file(
                'attorney_letter', 'application/pdf'
            )

        return jsonify(service.add(data, files)), HTTPStatus.CREATED

    @auth.require_role(Role.WRITE_PROTOCOLS)
    @bp.put('/planting_anticipation/<string:id>/status')
    def change_status(id: str):
        data = statusSchema.load(request.json)
        return jsonify(service.change_status(data, id))

    return bp
