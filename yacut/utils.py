import random

from .models import URL_map
from .settings import MAX_RANDOM_SHORT_ID_LENGTH

CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def get_unique_short_id():
    while True:
        short = ''.join(
            random.choices(CHARS, k=MAX_RANDOM_SHORT_ID_LENGTH)
        )
        if not URL_map.query.filter_by(short=short).count():
            break
    return short
