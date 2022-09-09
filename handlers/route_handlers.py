from http import HTTPStatus
from flask import (
    jsonify,
    request,
    send_file,
    abort
)
from application.rest.resource import utils
from application.schema import (
    FarmNearbyQuery,
    FarmQuery,
    NewOccurrenceSchema,
    OccurrenceQuery,
    ResolvedOccurrenceSchema,
    PlantingAnticipationSchema,
    PlantingAnticipationStatus
)
from domain.service import (
    PhytosanitaryService,
    OrdinanceService,
    ReportService,
    PlantingAnticipationService
)
from infrastructure.repository.storage import LocalStorage


def configure_routes_storage(app, storage: LocalStorage):

    @app.route('/files/<string:id>')
    def get_file(id: str):
        file = storage.open(id)

        if file is None:
            abort(HTTPStatus.NOT_FOUND)

        return send_file(file, download_name=file.filename)


def configure_routes_visits(app, service: PhytosanitaryService):

    @app.route('/visits')
    def get_visits_by_farm():
        farm_id = request.args.get('farm_id')
        return jsonify(service.get_visits(farm_id))


def configure_routes_farms(app, service: PhytosanitaryService):

    farm_query = FarmQuery()
    farm_nearby_query = FarmNearbyQuery()

    def _search_farms():
        query = farm_query.load(request.args.to_dict())
        return service.search_farms(query)

    @app.route('/farms')
    def search_farms():
        return jsonify(_search_farms())

    @app.route('/farms/geojson')
    def search_farms_geojson():
        farms = _search_farms()
        geojson = utils.export_feature_collection(farms, 'geometry')
        return jsonify(geojson)

    @app.route('/farms/nearby')
    def get_farms_nearby():
        query = farm_nearby_query.load(request.args.to_dict())
        results = service.search_farms_nearby(query)
        return jsonify(results)

    @app.route('/farms/<string:id>/visits')
    def get_farm_visits(id: str):
        results = service.get_visits(id)
        return jsonify(results)


def configure_routes_ordinance(app, service: OrdinanceService):

    @app.route('/ordinances')
    def get_all_ordinances():
        return jsonify(service.get_all())

    @app.route('/ordinances/<string:id>.pdf')
    def get_document(id: str):
        file = service.get_document(id)
        return utils.export_file(file, 'application/pdf', 'pdf')


def configure_routes_reports(app, service: ReportService):

    report_schema = NewOccurrenceSchema()
    report_resolved_schema = ResolvedOccurrenceSchema()
    report_query = OccurrenceQuery()

    @app.route('/reports')
    def get_all_reports():
        query = report_query.load(request.args)
        return jsonify(service.get_all(query))

    @app.route('/reports/<string:id>')
    def get_report_by_id(id: str):
        return jsonify(service.get_by_id(id))

    @app.route('/reports/geojson')
    def get_all_geojson_reports():
        query = report_query.load(request.args)
        reports = service.get_all(query)
        features = utils.export_feature_collection(reports, 'position')
        return jsonify(features)

    @app.route('/reports', methods=['POST'])
    def report_occurrence():
        data = report_schema.load(request.form.to_dict())
        file = utils.get_file('photo', 'image/jpeg')
        report = service.add(data, file)
        return jsonify(report)

    @app.route('/reports/<string:id>', methods=['PUT'])
    def resolve_reported_occurrence(id: str):
        data = report_resolved_schema.load(request.form.to_dict())
        file = utils.get_file('resolved_photo', 'image/jpeg')
        report = service.mark_as_resolved(id, data, file)
        return jsonify(report)


def configure_routes_planting(app, service: PlantingAnticipationService):

    schema = PlantingAnticipationSchema()
    statusSchema = PlantingAnticipationStatus()

    @app.route('/planting_anticipation')
    def get_all():
        return jsonify(service.get_all())

    @app.route('/planting_anticipation', methods=['POST'])
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

    @app.route('/planting_anticipation/<string:id>/status', methods=['PUT'])
    def change_status(id: str):
        data = statusSchema.load(request.json)
        return jsonify(service.change_status(data, id))
