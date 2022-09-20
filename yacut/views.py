from flask import render_template

from . import app
from .forms import URLForm


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    return 'Under construction'
