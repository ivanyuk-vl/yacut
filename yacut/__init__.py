from flask import Flask
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy

from settings import Config

app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)
babel.localeselector(lambda: app.config.get('LANGUAGE'))
db = SQLAlchemy(app)

from . import api_views, cli_commands, models, views
