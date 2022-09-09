from http import HTTPStatus
from flask import Blueprint, abort, send_file

from infrastructure.repository.storage import LocalStorage


def get_blueprint(storage: LocalStorage) -> Blueprint:
    bp = Blueprint('Storage', __name__)

    @bp.get('/files/<string:id>')
    def get_file(id: str):
        file = storage.open(id)

        if file is None:
            abort(HTTPStatus.NOT_FOUND)

        return send_file(file, download_name=file.filename)

    return bp
