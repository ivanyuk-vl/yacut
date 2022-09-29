from flask_wtf import FlaskForm
from wtforms.fields import StringField, URLField
from wtforms.validators import ValidationError

from .exceptions import (GenerateShortError, OriginalLengthError,
                         OriginalRequiredError, ShortAlreadyExistsError,
                         ShortLengthError, ValidateOriginalError,
                         ValidateShortError)
from .models import URL_map
from .settings import MAX_SHORT_ID_LENGTH, MAX_URL_LENGTH

URL_LABEL = 'Длинная ссылка'
SHORT_ID_LABEL = 'Ваш вариант короткой ссылки'
FIELD_REQUIRED_ERROR = 'Обязательное поле.'
FIELD_LENGTH_ERROR = 'Значение не должно содержать более {length} символов.'


def get_length_validation_error(exc):
    return ValidationError(
        FIELD_LENGTH_ERROR.format(length=exc.max_length)
    )


class OriginalLinkField(URLField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flags.required = True
        self.flags.maxlength = MAX_URL_LENGTH


class CustomIdField(StringField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.flags.maxlength = MAX_SHORT_ID_LENGTH


class URLForm(FlaskForm):
    original_link = OriginalLinkField(
        URL_LABEL,
        id='form-title',
    )
    custom_id = CustomIdField(
        SHORT_ID_LABEL,
        id='form-link',
    )

    def validate_original_link(self, field):
        try:
            URL_map.validate_original(field.data)
        except OriginalRequiredError:
            raise ValidationError(FIELD_REQUIRED_ERROR)
        except OriginalLengthError as exc:
            raise get_length_validation_error(exc)
        except ValidateOriginalError as exc:
            raise ValidationError(exc)

    def validate_custom_id(self, field):
        try:
            URL_map.validate_short(field.data)
        except ShortLengthError as exc:
            raise get_length_validation_error(exc)
        except (GenerateShortError, ShortAlreadyExistsError,
                ValidateShortError) as exc:
            raise ValidationError(exc)
