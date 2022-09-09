from flask import Flask, Blueprint
from flask_cors import CORS

from domain.service import (
    PhytosanitaryService,
    ReportService,
    PlantingAnticipationService,
)
from infrastructure import database
from infrastructure.repository import (
    VisitRepository,
    FarmRepository,
    ReportRepository,
    PlantingAnticipationRepository,
    LocalStorage,
)
from .resource import (
    files,
    farms,
    reports,
    planting_anticipation,
    visits,
)
from .encoder import CustomJsonEncoder
from .error import error_bp
from .security import Authorization, Role


URL_PREFIX = '/api/v1/phytosanitary'


def create_server(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['JSON_SORT_KEYS'] = False
    app.json_encoder = CustomJsonEncoder
    app.url_map.strict_slashes = False
    app.register_blueprint(error_bp)

    CORS(app)
    auth = Authorization(config.INTROSPECTION_URI)
    auth.grant_role_for_any_request(Role.ADMIN)

    db = database.get_database(config.MONGODB_SETTINGS)
    root_bp = Blueprint('Root', __name__, url_prefix=URL_PREFIX)

    storage = LocalStorage(db, URL_PREFIX + '/files')
    files_bp = files.get_blueprint(storage)
    root_bp.register_blueprint(files_bp)

    farm_repo = FarmRepository(db)
    visit_repo = VisitRepository(db)
    phytosanitary_svc = PhytosanitaryService(visit_repo, farm_repo)
    visits_bp = visits.get_blueprint(auth, phytosanitary_svc)
    root_bp.register_blueprint(visits_bp)

    farm_bp = farms.get_blueprint(auth, phytosanitary_svc)
    root_bp.register_blueprint(farm_bp)

    report_repo = ReportRepository(db)
    report_svc = ReportService(report_repo, storage)
    report_bp = reports.get_blueprint(auth, report_svc)
    root_bp.register_blueprint(report_bp)

    planting_repo = PlantingAnticipationRepository(db)
    planting_svc = PlantingAnticipationService(planting_repo, storage)
    planting_bp = planting_anticipation.get_blueprint(auth, planting_svc)
    root_bp.register_blueprint(planting_bp)

    app.register_blueprint(root_bp)

    return app
