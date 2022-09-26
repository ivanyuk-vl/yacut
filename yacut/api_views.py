from flask import jsonify, request
from werkzeug.exceptions import HTTPException

from . import app
from .error_handlers import APIUsageError
from .exceptions import (APIUsageError, GenerateShortError,
                         OriginalLenghtError, OriginalRequiredError,
                         ShortAlreadyExistsError, ShortLenghtError,
                         ValidateOriginalError, ValidateShortError)
from .models import INVALID_SHORT, URL_map

SHORT_ID_NOT_FOUND_ERROR = 'Указанный id не найден'
# pass tests/test_endpoints.py::test_url_already_exists:
UNIQUE_SHORT_ID_ERROR = 'Имя "{short}" уже занято.'


@app.route('/api/id/', methods=['POST'])
def map_short_id_to_url():
    try:
        return jsonify(URL_map.add_to_db(
            **URL_map.from_dict(request.get_json())
        ).to_dict()), 201
    except (ShortLenghtError, ValidateShortError):
        raise APIUsageError(INVALID_SHORT)
    except ShortAlreadyExistsError as exc:
        raise APIUsageError(UNIQUE_SHORT_ID_ERROR.format(short=exc.short))
    except GenerateShortError as exc:
        raise APIUsageError(str(exc), 500)
    except (
        OriginalLenghtError, OriginalRequiredError, ValidateOriginalError
    ) as exc:
        raise APIUsageError(str(exc))


@app.route('/api/id/<string:short>')
def get_url(short):
    try:
        return jsonify(URL_map.get_record_by_short(
            short=URL_map.validate_short(short, exists_check=False)
        ).url_to_dict())
    except (ShortLenghtError, ValidateShortError, HTTPException):
        raise APIUsageError(SHORT_ID_NOT_FOUND_ERROR, 404)
