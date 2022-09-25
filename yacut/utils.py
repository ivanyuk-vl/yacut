import random

from flask import abort

from .models import URL_map
from .settings import (LIMIT_GENERATE_SHORT_ATTEMTS,
                       MAX_RANDOM_SHORT_ID_LENGTH, SHORT_ID_CHARS)


def get_unique_short_id():
    for attempt in range(LIMIT_GENERATE_SHORT_ATTEMTS):
        short = ''.join(
            random.choices(SHORT_ID_CHARS, k=MAX_RANDOM_SHORT_ID_LENGTH)
        )
        if not URL_map.query.filter_by(short=short).count():
            return short
    return abort(500)  # FIXME
