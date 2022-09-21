from flask import render_template

from . import app, db
from .forms import URLForm
from .models import URL_map


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    db.session.add(URL_map(
        original=form.original_link.data,
        short=form.custom_id.data
    ))
    db.session.commit()  # FIXME
    return 'Under construction'
