from wtforms.validators import URL

from .exceptions import ValidateOriginalError

INVALID_URL_ERROR = 'Неверный URL.'


class URLValidator(URL):
    def __init__(self):
        super().__init__()

    def __call__(self, url):
        match = self.regex.match(url or '')
        if not(match and self.validate_hostname(match.group('host'))):
            raise ValidateOriginalError(INVALID_URL_ERROR)
