from flask_wtf import FlaskForm
from wtforms.fields import StringField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from .settings import MAX_SHORT_ID_LENGTH, MAX_URL_LENGTH

URL_LABEL = 'Длинная ссылка'
ID_FOR_URL = 'form-title'
SHORT_ID_LABEL = 'Ваш вариант короткой ссылки'
# SHORT_ID_PATTERN = r"^[\w\-.~:/?#[\]@!$&'()*+,;=]+$"  # FIXME
SHORT_ID_PATTERN = r'^[0-9A-Za-z]+$'
WRONG_SHORT_ID = 'Указано недопустимое имя для короткой ссылки'  # FIXME
ID_FOR_SHORT_ID = 'form-link'


class URLForm(FlaskForm):
    original_link = URLField(
        URL_LABEL,
        (DataRequired(), Length(max=MAX_URL_LENGTH), URL()),
        id=ID_FOR_URL,
    )
    custom_id = StringField(
        SHORT_ID_LABEL,
        (
            Optional(),
            Length(max=MAX_SHORT_ID_LENGTH),
            Regexp(SHORT_ID_PATTERN, message=WRONG_SHORT_ID),
        ),
        id=ID_FOR_SHORT_ID,
    )
