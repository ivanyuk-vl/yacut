import re
from datetime import datetime

from flask import url_for

from . import db
from .settings import MAX_SHORT_ID_LENGTH, MAX_URL_LENGTH, SHORT_ID_PATTERN

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
        return bool(URL_map.query.filter_by(short=short).count())

    @staticmethod
    def validate_short(short):
        if not short:
            return short  # add random generated short
        if len(short) > MAX_SHORT_ID_LENGTH:
            raise Exception()
        if not re.match(SHORT_ID_PATTERN, short):
            raise Exception()
        if URL_map.is_short_exists(short):
            raise Exception()
        return short

    @staticmethod
    def add_to_db(data):
        if not data:
            raise Exception()
        if 'original' not in data:
            raise Exception()
        short = URL_map.validate_short(data.get('short'))
        short  # FIXME

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
