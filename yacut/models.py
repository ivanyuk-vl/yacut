import re
from datetime import datetime
from random import choices

from flask import url_for

from . import db
from .exceptions import (APIUsageError, GenerateShortError,
                         OriginalLenghtError, OriginalRequiredError,
                         ShortAlreadyExistsError, ShortLenghtError,
                         ValidateShortError)
from .settings import (LIMIT_GENERATE_SHORT_ATTEMTS,
                       MAX_RANDOM_SHORT_ID_LENGTH, MAX_SHORT_ID_LENGTH,
                       MAX_URL_LENGTH, SHORT_ID_CHARS, SHORT_ID_PATTERN)
from .validators import URLValidator

EMPTY_REQUEST_ERROR = 'Отсутствует тело запроса'
GENERATE_SHORT_ERROR = ('Не удалось сгенерировать короткую ссылку. '
                        'Напишите свой вариант.')
# pass tests/test_views.py::test_duplicated_url_in_form:
UNIQUE_SHORT_ERROR = 'Имя {short} уже занято!'
URL_FIELD_REQUIRED_ERROR = '"url" является обязательным полем!'
URL_LENGTH_ERROR = '"url" не должeн содержать более {url_length} символов.'
SHORT_LENGTH_ERROR = ('Короткая ссылка не должна содержать более '
                      '{short_length} символов.')
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

    @classmethod
    def is_short_exists(cls, short):
        return bool(short and cls.query.filter_by(short=short).count())

    @classmethod
    def get_unique_short_id(cls):
        for attempt in range(LIMIT_GENERATE_SHORT_ATTEMTS):
            short = ''.join(
                choices(SHORT_ID_CHARS, k=MAX_RANDOM_SHORT_ID_LENGTH)
            )
            if not cls.is_short_exists(short):
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
            OriginalLenghtError(URL_LENGTH_ERROR.format(MAX_URL_LENGTH))
        URLValidator()(original)
        return original

    @classmethod
    def validate_short(cls, short, exists_check=True):
        short = short or ''
        if len(short) > MAX_SHORT_ID_LENGTH:
            raise ShortLenghtError(
                SHORT_LENGTH_ERROR.format(short_length=MAX_SHORT_ID_LENGTH)
            )
        if not re.match(SHORT_ID_PATTERN, short):
            raise ValidateShortError(INVALID_SHORT)
        if exists_check and cls.is_short_exists(short):
            raise ShortAlreadyExistsError(
                short, UNIQUE_SHORT_ERROR.format(short=short)
            )
        return short

    @classmethod
    def validate_or_generate_short(cls, short, validate=True):
        if not short:
            return cls.get_unique_short_id()
        if not validate:
            return short
        return cls.validate_short(short)

    @classmethod
    def add_to_db(cls, validate=True, **data,):
        url_map = cls(
            original=cls.validate_original(data.get('original'), validate),
            short=cls.validate_or_generate_short(data.get('short'), validate)
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @classmethod
    def get_record_by_short(cls, short):
        return cls.query.filter_by(short=short).first_or_404()

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
