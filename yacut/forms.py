from flask_wtf import FlaskForm
from wtforms.fields import URLField
from wtforms.validators import DataRequired, Length, Optional

from .settings import MAX_URL_ID_LENGTH

LINK_LABEL = 'Длинная ссылка'
REQUIRED_FIELD_MESSAGE = 'Обязательное поле'
ID_LABEL = 'Ваш вариант короткой ссылки'


class URLForm(FlaskForm):
    original_link = URLField(
        LINK_LABEL,
        (DataRequired(REQUIRED_FIELD_MESSAGE))
    )
    custom_id = URLField(
        ID_LABEL,
        (Optional(), Length(1, MAX_URL_ID_LENGTH))
    )
