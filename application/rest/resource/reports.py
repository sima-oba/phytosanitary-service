from flask import Blueprint, request, jsonify

from application.schema import (
    NewOccurrenceSchema,
    ResolvedOccurrenceSchema,
    OccurrenceQuery,
)
from domain.service import ReportService
from ..security import Authorization, Role
from . import utils


def get_blueprint(
    auth: Authorization,
    service: ReportService
) -> Blueprint:
    bp = Blueprint('Report Tiguera', __name__, url_prefix='/reports')
    new_occurrence_schema = NewOccurrenceSchema()
    resolved_occurrence_schema = ResolvedOccurrenceSchema()
    occurrence_query = OccurrenceQuery()

    def filter_occurrences():
        query = occurrence_query.load(request.args)
        user = auth.current_user

        if user and user.doc:
            query['reporter'] = user.username

        return service.get_all(query)

    @bp.get('/')
    @auth.require_role(Role.REPORT_OCCURRENCES)
    def get_occurrences():
        return jsonify(filter_occurrences())

    @bp.get('/geojson')
    @auth.require_role(Role.REPORT_OCCURRENCES)
    def get_occurrences_geojson():
        occurrences = filter_occurrences()
        features = utils.export_feature_collection(occurrences, 'position')
        return jsonify(features)

    @bp.get('/<string:id>')
    @auth.require_role(Role.REPORT_OCCURRENCES)
    def get_occurrence_by_id(id: str):
        return jsonify(service.get_by_id(id))

    @bp.post('/')
    @auth.require_role(Role.REPORT_OCCURRENCES)
    def report_occurrence():
        data = new_occurrence_schema.load(request.form)
        user = auth.current_user

        if user:
            data['reporter'] = user.username

        file = utils.get_file('photo', 'image/jpeg')
        report = service.add(data, file)
        return jsonify(report)

    @bp.put('/<string:id>')
    @auth.require_role(Role.MANAGE_OCCURRENCES)
    def resolve_reported_occurrence(id: str):
        data = resolved_occurrence_schema.load(request.form.to_dict())
        file = utils.get_file('resolved_photo', 'image/jpeg')
        report = service.mark_as_resolved(id, data, file)
        return jsonify(report)

    return bp
