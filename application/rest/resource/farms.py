from flask import Blueprint, jsonify, request

from application.schema import FarmQuery, FarmNearbyQuery
from domain.service import PhytosanitaryService
from . import utils
from ..security import Authorization, Role


def get_blueprint(
    auth: Authorization,
    service: PhytosanitaryService
) -> Blueprint:
    bp = Blueprint('Farms', __name__)
    farm_query = FarmQuery()
    farm_nearby_query = FarmNearbyQuery

    def _search_farms():
        query = farm_query.load(request.args)
        user = auth.current_user

        if user and user.doc:
            query['owner'] = user.doc

        return service.search_farms(query)

    @bp.get('/farms')
    @auth.require_role(Role.READ_PROPERTIES)
    def search_farms():
        return jsonify(_search_farms())

    @bp.get('/farms/geojson')
    @auth.require_role(Role.READ_PROPERTIES)
    def search_farms_geojson():
        farms = _search_farms()
        geojson = utils.export_feature_collection(farms, 'geometry')
        return jsonify(geojson)

    @auth.require_role(Role.READ_PROPERTIES)
    @bp.get('/farms/nearby')
    def get_farms_nearby():
        query = farm_nearby_query.load(request.args.to_dict())
        results = service.search_farms_nearby(query)
        return jsonify(results)

    @auth.require_role(Role.READ_PROPERTIES)
    @bp.get('/farms/<string:id>/visits')
    def get_farm_visits(id: str):
        results = service.get_visits(id)
        return jsonify(results)

    return bp
