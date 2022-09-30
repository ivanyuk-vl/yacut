from flask import abort, redirect, render_template

from . import app
from .exceptions import ShortLengthError, ValidateShortError
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
        form.original_link.data,
        form.custom_id.data,
        validate=False
    ).short)


@app.route('/<string:short>')
def redirect_view(short):
    try:
        return redirect(URL_map.get_by_short_or_404(
            URL_map.validate_short(short, exists_check=False)
        ).original)
    except (ShortLengthError, ValidateShortError):
        abort(404)
