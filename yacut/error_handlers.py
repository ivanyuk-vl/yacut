from flask import jsonify, render_template

from . import app, db
from .exceptions import APIUsageError


@app.errorhandler(APIUsageError)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    return render_template('core/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('core/500.html'), 500
