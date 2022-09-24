import re

from flask import jsonify, request

from . import app, db
from .error_handlers import APIUsageError
from .forms import SHORT_ID_NAME_ERROR
from .models import URL_map
from .settings import MAX_SHORT_ID_LENGTH
from .utils import get_unique_short_id
from .views import SHORT_ID_PATTERN

EMPTY_REQUEST_ERROR = 'Отсутствует тело запроса'
URL_FIELD_REQUIRED_ERROR = '"url" является обязательным полем!'
SHORT_ID_NOT_FOUND_ERROR = 'Указанный id не найден'
# pass tests/test_endpoints.py::test_url_already_exists:
UNIQUE_SHORT_ID_ERROR = 'Имя "{short}" уже занято.'


@app.route('/api/id/', methods=['POST'])
def map_short_id_to_url():
    data = request.get_json()
    if not data:
        raise APIUsageError(EMPTY_REQUEST_ERROR)
    if 'url' not in data:
        raise APIUsageError(URL_FIELD_REQUIRED_ERROR)  # FIXME
    short_id = data.pop('custom_id', None)
    if short_id and (
        len(short_id) > MAX_SHORT_ID_LENGTH or  # FIXME
        not re.match(SHORT_ID_PATTERN, short_id)
    ):
        raise APIUsageError(SHORT_ID_NAME_ERROR)
    if (
        short_id and  # FIXME
        URL_map.query.filter_by(short=short_id).first() is not None
    ):
        raise APIUsageError(
            UNIQUE_SHORT_ID_ERROR.format(short=short_id)
        )
    data['short_id'] = short_id or get_unique_short_id()
    url_map = URL_map()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()  # FIXME
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<string:short>')
def get_url(short):
    query = URL_map.query.filter_by(short=short)
    if len(short) > MAX_SHORT_ID_LENGTH or not query.count():
        raise APIUsageError(SHORT_ID_NOT_FOUND_ERROR, 404)
    return jsonify(query.first().url_to_dict())  # FIXME
