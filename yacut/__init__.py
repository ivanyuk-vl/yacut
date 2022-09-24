from flask import Flask
from flask_babel import Babel
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from settings import Config

app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)
babel.localeselector(lambda: app.config.get('LANGUAGE'))
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import api_views, cli_commands, models, views
