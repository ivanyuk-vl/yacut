from flask_wtf import FlaskForm
from wtforms.fields import StringField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from .settings import MAX_URL_ID_LENGTH, MAX_URL_LENGTH

LINK_LABEL = 'Длинная ссылка'
ID_FOR_LINK = 'form-title'
ID_LABEL = 'Ваш вариант короткой ссылки'
ID_PATTERN = r"^[\w\-.~:/?#[\]@!$&'()*+,;=%]{1,16}$"  # FIXME
ID_FOR_ID = 'form-link'


class URLForm(FlaskForm):
    original_link = URLField(
        LINK_LABEL,
        (DataRequired(), Length(max=MAX_URL_LENGTH), URL()),
        id=ID_FOR_LINK,
    )
    custom_id = StringField(
        ID_LABEL,
        (Optional(), Length(max=MAX_URL_ID_LENGTH), Regexp(ID_PATTERN)),
        id=ID_FOR_ID,
    )
