import re

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import APIUsageError
from .models import URL_map
from .settings import MAX_SHORT_ID_LENGTH
from .utils import get_unique_short_id
from .views import SHORT_ID_PATTERN, UNIQUE_SHORT_URL_ERROR

EMPTY_REQUEST = 'Отсутствует тело запроса'
URL_FIELD_REQUIRED = '"url" является обязательным полем!'
WRONG_SHORT_ID = 'Указано недопустимое имя для короткой ссылки'  # FIXME
SHORT_ID_NOT_FOUND = 'Указанный id не найден'
# FIXME


@app.route('/api/id/', methods=['POST'])
def map_short_id_to_url():
    data = request.get_json()
    if not data:
        raise APIUsageError(EMPTY_REQUEST)
    if 'url' not in data:
        raise APIUsageError(URL_FIELD_REQUIRED)  # FIXME
    if (
        'custom_id' in data and (
            not re.match(SHORT_ID_PATTERN, data['custom_id']) or
            URL_map.query.filter_by(
                short=data['custom_id']
            ).first() is not None
        )
    ):
        raise APIUsageError(UNIQUE_SHORT_URL_ERROR)
    data['short_id'] = url_for(
        'redirect_view',
        short=data.pop('custom', get_unique_short_id()),
        _external=True
    )
    url_map = URL_map()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()  # FIXME
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<path:short>', methods=['GET'])
def get_url(short):
    query = URL_map.query.filter_by(short=short)
    if len(short) > MAX_SHORT_ID_LENGTH or not query.count():
        raise APIUsageError(SHORT_ID_NOT_FOUND)
    return jsonify(query.one().url_to_dict())  # FIXME
