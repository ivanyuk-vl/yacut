from wtforms.validators import URL, ValidationError

INVALID_URL_ERROR = 'Неверный URL.'


class URLValidator(URL):
    def __init__(self):
        super().__init__()

    def __call__(self, url):
        match = self.regex.match(url or '')
        if not (match or self.validate_hostname(match.group('host'))):
            raise ValidationError(INVALID_URL_ERROR)
