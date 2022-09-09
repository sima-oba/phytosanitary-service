from dataclasses import is_dataclass, asdict
from flask import Response, request, send_file
from marshmallow import ValidationError
from typing import IO, BinaryIO


def export_feature_collection(data: list, geometry_key: str) -> dict:
    if not data:
        return {
            'type': 'FeatureCollection',
            'features': []
        }

    features = []

    for index, feat in enumerate(data):
        if is_dataclass(feat):
            feat = asdict(feat)

        geometry = feat.pop(geometry_key, None)
        features.append({
            'id': index,
            'type': 'Feature',
            'properties': {key: value for key, value in feat.items()},
            'geometry': geometry
        })

    return {
        'type': 'FeatureCollection',
        'features': features
    }


def export_file(file: IO, mimetype: str, ext: str) -> Response:
    return send_file(
        file,
        attachment_filename=f'{id}.{ext}',
        mimetype=mimetype
    )


def get_file(filename: str, mimetype: str) -> BinaryIO:
    if filename not in request.files:
        raise ValidationError({filename: 'missing required file'})

    file = request.files[filename]

    if file.content_type != mimetype:
        raise ValidationError({
            filename:   f'invalid mime type {file.content_type}. '
                        f'It has to be {mimetype}'
        })

    return file.stream
