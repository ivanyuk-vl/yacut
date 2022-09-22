import random

from .models import URL_map
from .settings import MAX_LENGTH_RANDOM_SHORT_ID

DICTIONARY = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def get_unique_short_id():
    while True:
        short = ''.join(
            random.choices(DICTIONARY, k=MAX_LENGTH_RANDOM_SHORT_ID)
        )
        if not URL_map.query.filter_by(short=short).count():
            break
    return short
