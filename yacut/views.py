import re

from flask import abort, redirect, render_template

from . import app, db
from .forms import SHORT_ID_PATTERN, URLForm
from .models import URL_map
from .settings import MAX_SHORT_ID_LENGTH
from .utils import get_unique_short_id

# pass tests/test_views.py::test_duplicated_url_in_form:
UNIQUE_SHORT_ID_ERROR = 'Имя {short} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()

    def get_render_result(short=None):
        return render_template('base.html', form=form, short=short)

    if not form.validate_on_submit():
        return get_render_result()
    if (
        form.custom_id.data and
        URL_map.query.filter_by(short=form.custom_id.data).count()
    ):
        form.custom_id.errors.append(
            UNIQUE_SHORT_ID_ERROR.format(short=form.custom_id.data)
        )
        return get_render_result()
    url_map = URL_map(
        original=form.original_link.data,
        short=form.custom_id.data or get_unique_short_id()
    )
    db.session.add(url_map)
    db.session.commit()
    return get_render_result(short=url_map.short)


@app.route('/<string:short>')
def redirect_view(short):
    if (
        len(short) > MAX_SHORT_ID_LENGTH or
        not re.match(SHORT_ID_PATTERN, short)
    ):
        abort(404)
    return redirect(
        URL_map.query.filter_by(short=short).first_or_404().original
    )
