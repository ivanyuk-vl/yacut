import re
from datetime import datetime
from random import choices

from flask import url_for

from . import db
from .exceptions import (APIUsageError, GenerateShortError,
                         OriginalLengthError, OriginalRequiredError,
                         ShortAlreadyExistsError, ShortLengthError,
                         ValidateShortError)
from .settings import (LIMIT_GENERATE_SHORT_ATTEMTS, MAX_SHORT_ID_LENGTH,
                       MAX_URL_LENGTH, RANDOM_SHORT_ID_LENGTH, SHORT_ID_CHARS,
                       SHORT_ID_PATTERN)
from .validators import URLValidator

EMPTY_REQUEST_ERROR = 'Отсутствует тело запроса'
GENERATE_SHORT_ERROR = ('Не удалось сгенерировать короткую ссылку. '
                        'Напишите свой вариант.')
UNIQUE_SHORT_ERROR = 'Имя {short} уже занято!'
URL_FIELD_REQUIRED_ERROR = '"url" является обязательным полем!'
URL_LENGTH_ERROR = (f'"url" не должeн содержать более {MAX_URL_LENGTH} '
                    'символов.')
SHORT_LENGTH_ERROR = ('Короткая ссылка не должна содержать более '
                      f'{MAX_SHORT_ID_LENGTH} символов.')
INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'
URL_MAP_REPR = (
    'URL_map(id={id!r}, original={original!r}, short={short!r}, '
    'timestamp={timestamp!r}'
)


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_URL_LENGTH), nullable=False)
    short = db.Column(
        db.String(MAX_SHORT_ID_LENGTH), unique=True, nullable=False
    )
    timestamp = db.Column(db.DateTime, default=datetime.now)

    @staticmethod
    def is_short_exists(short):
        return bool(short and URL_map.query.filter_by(short=short).count())

    @staticmethod
    def get_unique_short_id():
        for attempt in range(LIMIT_GENERATE_SHORT_ATTEMTS):
            short = ''.join(
                choices(SHORT_ID_CHARS, k=RANDOM_SHORT_ID_LENGTH)
            )
            if not URL_map.is_short_exists(short):
                return short
        raise GenerateShortError(GENERATE_SHORT_ERROR)

    @staticmethod
    def validate_original(original, validate=True):
        if not validate:
            return original
        original = original or ''
        if not original:
            raise OriginalRequiredError(URL_FIELD_REQUIRED_ERROR)
        if len(original) > MAX_URL_LENGTH:
            OriginalLengthError(MAX_URL_LENGTH, URL_LENGTH_ERROR)
        URLValidator()(original)
        return original

    @staticmethod
    def validate_short(short, exists_check=True):
        short = short or ''
        if not short:
            return short
        if len(short) > MAX_SHORT_ID_LENGTH:
            raise ShortLengthError(MAX_SHORT_ID_LENGTH, SHORT_LENGTH_ERROR)
        if not re.match(SHORT_ID_PATTERN, short):
            raise ValidateShortError(INVALID_SHORT)
        if exists_check and URL_map.is_short_exists(short):
            raise ShortAlreadyExistsError(
                short, UNIQUE_SHORT_ERROR.format(short=short)
            )
        return short

    @staticmethod
    def validate_or_generate_short(short, validate=True):
        if not short:
            return URL_map.get_unique_short_id()
        if not validate:
            return short
        return URL_map.validate_short(short)

    @staticmethod
    def add_to_db(original, short='', validate=True):
        url_map = URL_map(
            original=URL_map.validate_original(original, validate),
            short=URL_map.validate_or_generate_short(short, validate)
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get_by_short_or_404(short):
        return URL_map.query.filter_by(short=short).first_or_404()

    @staticmethod
    def get_by_short_or_none(short):
        return URL_map.query.filter_by(short=short).first()

    def __repr__(self):
        return URL_MAP_REPR.format(
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp.strftime('%d.%m.%Y %H:%M:%S')
        )

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view',
                short=self.short,
                _external=True
            )
        )

    def url_to_dict(self):
        return dict(url=self.original)

    @staticmethod
    def from_dict(data):
        if not data:
            raise APIUsageError(EMPTY_REQUEST_ERROR)
        return dict(original=data.get('url'), short=data.get('custom_id'))
