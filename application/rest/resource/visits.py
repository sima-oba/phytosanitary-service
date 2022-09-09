from flask import Blueprint, jsonify, request

from domain.service import PhytosanitaryService
from ..security import Authorization, Role


def get_blueprint(
    auth: Authorization,
    service: PhytosanitaryService
) -> Blueprint:
    bp = Blueprint('Visits', __name__, url_prefix='/visits')

    @bp.get('/')
    @auth.require_role(Role.READ_PROPERTIES)
    def get_visits_by_farm():
        farm_id = request.args.get('farm_id')
        return jsonify(service.get_visits(farm_id))

    return bp
