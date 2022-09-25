from flask_wtf import FlaskForm
from wtforms.fields import StringField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp

from .settings import MAX_SHORT_ID_LENGTH, MAX_URL_LENGTH, SHORT_ID_PATTERN

URL_LABEL = 'Длинная ссылка'
SHORT_ID_LABEL = 'Ваш вариант короткой ссылки'
SHORT_ID_NAME_ERROR = 'Указано недопустимое имя для короткой ссылки'


class URLForm(FlaskForm):
    original_link = URLField(
        URL_LABEL,
        (DataRequired(), Length(max=MAX_URL_LENGTH), URL()),
        id='form-title',
    )
    custom_id = StringField(
        SHORT_ID_LABEL,
        (
            Optional(),
            Length(max=MAX_SHORT_ID_LENGTH),
            Regexp(SHORT_ID_PATTERN, message=SHORT_ID_NAME_ERROR),
        ),
        id='form-link',
    )
