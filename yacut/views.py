from flask import abort, redirect, render_template

from . import app
from .exceptions import ShortLenghtError, ValidateShortError
from .forms import URLForm
from .models import URL_map


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()

    def _render_template(short=None):
        return render_template('index.html', form=form, short=short)

    if not form.validate_on_submit():
        return _render_template()
    return _render_template(URL_map.add_to_db(
        original=form.original_link.data,
        short=form.custom_id.data,
        validate=False
    ).short)


@app.route('/<string:short>')
def redirect_view(short):
    try:
        return redirect(URL_map.get_record_by_short(
            URL_map.validate_short(short, exists_check=False)
        ).original)
    except (ShortLenghtError, ValidateShortError):
        abort(404)
