from flask_wtf import FlaskForm
from wtforms.fields import StringField, URLField
from wtforms.validators import DataRequired, Length, Optional

from .settings import (MAX_URL_ID_LENGTH, MAX_URL_LENGTH, MIN_URL_ID_LENGTH,
                       MIN_URL_LENGHT)

LINK_LABEL = 'Длинная ссылка'
LINK_ID = 'form-title'
REQUIRED_FIELD_MESSAGE = 'Обязательное поле'
ID_LABEL = 'Ваш вариант короткой ссылки'
ID_FOR_ID = 'form-link'


class URLForm(FlaskForm):
    original_link = URLField(
        LINK_LABEL,
        (
            DataRequired(REQUIRED_FIELD_MESSAGE),
            Length(MIN_URL_LENGHT, MAX_URL_LENGTH),
        ),
        id=LINK_ID,
    )
    custom_id = StringField(
        ID_LABEL,
        (Optional(), Length(MIN_URL_ID_LENGTH, MAX_URL_ID_LENGTH)),
        id=ID_FOR_ID,
    )
