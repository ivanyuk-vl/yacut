import re
from datetime import datetime
from random import choices

from flask import url_for

from . import db
from .exceptions import (OriginalRequiredError, ShortExistsError,
                         ValidateShortError)
from .settings import (LIMIT_GENERATE_SHORT_ATTEMTS,
                       MAX_RANDOM_SHORT_ID_LENGTH, MAX_SHORT_ID_LENGTH,
                       MAX_URL_LENGTH, SHORT_ID_CHARS, SHORT_ID_PATTERN)
from .validators import URLValidator

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
        raise Exception()  # FIXME

    @staticmethod
    def validate_original(original):
        if not original:
            raise OriginalRequiredError()
        URLValidator()(original)
        return original

    @classmethod
    def validate_short(cls, short):
        short = short or ''  # FIXME
        if len(short) > MAX_SHORT_ID_LENGTH:
            raise ValidateShortError()  # TODO change exception?
        if not re.match(SHORT_ID_PATTERN, short):
            raise ValidateShortError()
        if cls.is_short_exists(short):
            raise ShortExistsError()
        return short

    @classmethod
    def validate_or_generate_short(cls, short):
        if not short:
            return cls.get_unique_short_id()
        return cls.validate_short(short)

    @classmethod
    def add_to_db(cls, data):
        url_map = cls(
            original=cls.validate_original(data.get('original')),
            short=cls.validate_or_generate_short(data.get('short'))
        )
        db.session.add(url_map)
        db.session.commit()
        return url_map

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

    def from_dict(self, data):
        for field in ('original', 'short'):
            if field in data:
                setattr(self, field, data[field])
