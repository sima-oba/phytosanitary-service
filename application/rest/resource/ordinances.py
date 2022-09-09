from flask import Blueprint, jsonify

from domain.service import OrdinanceService
from . import utils


def get_blueprint(service: OrdinanceService) -> Blueprint:
    bp = Blueprint('Ordinances', __name__)

    @bp.get('/ordinances')
    def get_all_ordinances():
        return jsonify(service.get_all())

    @bp.get('/ordinances/<string:id>.pdf')
    def get_document(id: str):
        file = service.get_document(id)
        return utils.export_file(file, 'application/pdf', 'pdf')

    return bp
