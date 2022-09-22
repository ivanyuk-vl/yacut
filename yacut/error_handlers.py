from flask import jsonify, render_template

from . import app, db


class APIUsageError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.statuscode = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(APIUsageError)
def invalid_api_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)  # FIXME
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)  # FIXME
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
