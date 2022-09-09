import datetime
from flask import Flask
import pytest
import json
from os.path import dirname, abspath
from domain.model.farm import Farm
from domain.model.geo import Geometry
from domain.service import (
    OrdinanceService,
    PhytosanitaryService,
    PlantingAnticipationService,
    ReportService
)
from handlers.route_handlers import (
    configure_routes_farms,
    configure_routes_ordinance,
    configure_routes_planting,
    configure_routes_reports,
    configure_routes_storage,
    configure_routes_visits
)
from infrastructure.repository import (
    FarmRepository,
    FileRepository,
    OrdinanceRepository,
    PlantingAnticipationRepository,
    ReportRepository,
    LocalStorage,
    VisitRepository
)
from infrastructure.database import get_database
from . import TestConfig as config


URL_PREFIX = '/api/v1/phytosanitary'
db = get_database(config.MONGODB_SETTINGS)
storage = LocalStorage(db, URL_PREFIX + '/files')
farm_repo = FarmRepository(db)
visit_repo = VisitRepository(db)
phytosanitary_service = PhytosanitaryService(visit_repo, farm_repo)
file_repo = FileRepository(db)
ordinance_repo = OrdinanceRepository(db)
ordinance_service = OrdinanceService(ordinance_repo, file_repo)
report_repo = ReportRepository(db)
report_service = ReportService(report_repo, storage)
planting_ant_repo = PlantingAnticipationRepository(db)
planting_ant_svc = PlantingAnticipationService(planting_ant_repo, storage)


@pytest.fixture
def clientinstance():
    app = Flask(__name__)
    configure_routes_farms(app, phytosanitary_service)
    configure_routes_ordinance(app, ordinance_service)
    configure_routes_planting(app, planting_ant_svc)
    configure_routes_reports(app, report_service)
    configure_routes_storage(app, storage)
    configure_routes_visits(app, phytosanitary_service)
    return app.test_client()


@pytest.fixture
def postReport(clientinstance):
    url = '/reports'

    data = {
        'longitude': 1,
        'latitude': 2,
        'location': '',
        'occurrence_date': '2014-12-22T03:12:58.019077+00:00',
        'occurrence_type': 'RUST',
        'area': 3
    }
    data['photo'] = (f'{dirname(abspath(__name__))}/test/photo.jpg', 'photo.jpg')  # noqa
    posting = clientinstance.post(url, data=data, content_type='multipart/form-data')  # noqa
    return posting.status_code, posting.get_data()


@pytest.fixture
def postPlanting(clientinstance):
    url = '/planting_anticipation'

    data = {
        "address": "",
        "cellphone": 12334554300,
        "cep": 99999999,
        "city": "Baianpolis",
        "cpf_cnpj": 11111111111,
        "email": "teste@mail.com",
        "farm_id": "0",
        "latitude": 25,
        "longitude": 54,
        "nucleos": 2,
        "owner_name": "Seu Zé",
        "phone": 83744154151,
        "state": "Bahia"
    }

    data['rg_cnpj'] = (f'{dirname(abspath(__name__))}/test/rg_cnpj.pdf', 'rg_cnpj.pdf')  # noqa
    data['commitment'] = (f'{dirname(abspath(__name__))}/test/commitment.pdf', 'commitment.pdf')  # noqa
    data['sketch'] = (f'{dirname(abspath(__name__))}/test/sketch.pdf', 'sketch.pdf')  # noqa
    data['soy_planting'] = (f'{dirname(abspath(__name__))}/test/soy_planting.pdf', 'soy_planting.pdf')  # noqa
    data['art'] = (f'{dirname(abspath(__name__))}/test/art.pdf', 'art.pdf')  # noqa
    data['work_plan'] = (f'{dirname(abspath(__name__))}/test/work_plan.pdf', 'work_plan.pdf')  # noqa
    posting = clientinstance.post(url, data=data, content_type='multipart/form-data')  # noqa

    return posting.status_code, posting.get_data()


def test_file_route(clientinstance):
    url = '/files/0'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 404


def test_visits(clientinstance):
    url = '/visits'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200


def test_farms(clientinstance):
    url = '/farms'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200


def test_farms_geojson(clientinstance):
    url = '/farms/geojson'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200


def _test_farms_nearby(clientinstance):
    url = '/farms/nearby?lat=9.1&lng=1.2&rad=1.4'
    farm_repo.add(
        Farm(  # noqa
        address="BA-2902500-5B08A644E20E41B18E44E1E6AB082109",  # noqa
        name="Fazenda Santa Helena",  # noqa
        city="Baianópolis",  # noqa
        created_at=datetime.datetime.now(),  # noqa
        updated_at=datetime.datetime.now(),  # noqa
        nucleos="1",  # noqa
        owner="55692199000155",  # noqa
        imported_id="0",  # noqa
        irrigated_area="",  # noqa
        dryland_area="",  # noqa
        cultivation_system="",  # noqa
        irrigation_system="",  # noqa
        _id='0',  # noqa
        classification="a",  # noqa
        geometry=Geometry(  # noqa
            type="Point",  # noqa
            coordinates=[  # noqa
                    88.8,  # noqa
                    -86.8  # noqa
                ]  # noqa
            )  # noqa
        )  # noqa
    )
    db['farm'].create_index([("geometry", "2dsphere")])

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200


def _test_farm_visits(clientinstance):
    url = '/farms/0/visits'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200


def test_ordinance(clientinstance):
    url = '/ordinances'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200


def test_ordinance_doc(clientinstance):
    url = '/ordinances/teste.pdf'
    file_repo.write("teste", b'documento teste')

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200


def test_reports(clientinstance):
    url = '/reports'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200


def test_report_id(clientinstance, postReport):
    code, data = postReport
    response = data.decode("utf-8")
    _id = json.loads(response)['_id']
    url = f'/reports/{_id}'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200 and code == 200


def test_report_geojson(clientinstance):
    url = '/reports/geojson'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200


def test_report_post(postReport):
    code, data = postReport

    assert data != b''
    assert code == 200


def test_report_put(clientinstance, postReport):
    code, data = postReport
    response = data.decode("utf-8")
    _id = json.loads(response)['_id']
    url = f'/reports/{_id}'
    data = {
        'resolved_date': '2014-12-22T03:12:58.019077+00:00',
        'notes': '',
    }
    data['resolved_photo'] = (f'{dirname(abspath(__name__))}/test/photo.jpg', 'resolved_photo.jpg')  # noqa
    posting = clientinstance.put(url, data=data, content_type='multipart/form-data')  # noqa
    assert posting.status_code == 200
    assert code == 200


def test_planting_anticipation(clientinstance):
    url = '/planting_anticipation'

    response = clientinstance.get(url)
    assert response.get_data() != b''
    assert response.status_code == 200


def test_planting_post(postPlanting):
    code, data = postPlanting

    assert code == 201
    assert data != b''


def test_planting_put(clientinstance, postPlanting):
    code, data = postPlanting
    response = data.decode("utf-8")
    _id = json.loads(response)['_id']
    url = f'/planting_anticipation/{_id}/status'

    mjson = {
        "ordinance_ref": "",
        "status": "REVIEW",
    }

    posting = clientinstance.put(url, json=mjson)
    assert posting.status_code == 200 and code == 201
