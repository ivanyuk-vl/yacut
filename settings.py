import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI',
        default='sqlite:///db.sqlite3'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv(
        'SECRET_KEY',
        default='=vmk*r%v*_--m4++_*6&gl0mf55^e#4e+16e7@nqgeukt4&&w*'
    )
