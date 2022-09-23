from datetime import datetime

from flask import url_for

from . import db
from .settings import MAX_SHORT_ID_LENGTH, MAX_URL_LENGTH


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_URL_LENGTH), nullable=False)
    short = db.Column(
        db.String(MAX_SHORT_ID_LENGTH), unique=True, nullable=False
    )
    timestamp = db.Column(db.DateTime, default=datetime.now)

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
        for api_key, field in (('url', 'original'), ('short_id', 'short')):
            if api_key in data:
                setattr(self, field, data[api_key])
