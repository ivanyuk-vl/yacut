from flask_wtf import FlaskForm
from wtforms.fields import StringField, URLField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from .exceptions import (GenerateShortError, OriginalLenghtError,
                         OriginalRequiredError, ShortAlreadyExistsError,
                         ShortLenghtError, ValidateOriginalError,
                         ValidateShortError)
from .models import URL_map
from .settings import MAX_SHORT_ID_LENGTH, MAX_URL_LENGTH

URL_LABEL = 'Длинная ссылка'
SHORT_ID_LABEL = 'Ваш вариант короткой ссылки'


class URLForm(FlaskForm):
    original_link = URLField(
        URL_LABEL,
        (DataRequired(), Length(max=MAX_URL_LENGTH)),
        id='form-title',
    )
    custom_id = StringField(
        SHORT_ID_LABEL,
        (
            Optional(),
            Length(max=MAX_SHORT_ID_LENGTH),
        ),
        id='form-link',
    )

    def validate_original_link(self, field):
        try:
            URL_map.validate_original(field.data)
        except (OriginalLenghtError, OriginalRequiredError):
            pass
        except ValidateOriginalError as exc:
            raise ValidationError(exc)

    def validate_custom_id(self, field):
        try:
            URL_map.validate_short(field.data)
        except ShortLenghtError:
            pass
        except (GenerateShortError, ShortAlreadyExistsError,
                ValidateShortError) as exc:
            raise ValidationError(exc)
