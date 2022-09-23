import re

from flask import abort, redirect, render_template
from sqlalchemy.exc import IntegrityError

from . import app, db
from .forms import SHORT_ID_PATTERN, URLForm
from .models import URL_map
from .settings import MAX_SHORT_ID_LENGTH
from .utils import get_unique_short_id

EXCEPTION_SEARCH_DATA = ('UNIQUE', 'URL_map.short')
UNIQUE_SHORT_ID_ERROR = 'Имя "{short}" уже занято.'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    url_map = URL_map(
        original=form.original_link.data,
        short=form.custom_id.data or get_unique_short_id()
    )
    db.session.add(url_map)
    try:
        db.session.commit()  # FIXME
    except IntegrityError as exc:
        if all(data in exc.args[0] for data in EXCEPTION_SEARCH_DATA):
            form.custom_id.errors.append(UNIQUE_SHORT_ID_ERROR)
            # FIXME query short_id count -> True -> already exist
        else:
            raise IntegrityError(exc)
        return render_template('index.html', form=form)
    return render_template('index.html', form=form, short=url_map.short)


@app.route('/<path:short>')
def redirect_view(short):
    if (
        len(short) > MAX_SHORT_ID_LENGTH or
        not re.match(SHORT_ID_PATTERN, short)
    ):
        abort(404)
    return redirect(
        URL_map.query.filter_by(short=short).first_or_404().original  # FIXME
    )
