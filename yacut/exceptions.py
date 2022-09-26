class APIUsageError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


class ValidateOriginalError(ValueError):
    pass


class ValidateShortError(ValueError):
    pass


class OriginalRequiredError(ValueError):
    pass


class ShortAlreadyExistsError(Exception):
    def __init__(self, short, *args):
        super().__init__(*args)
        self.short = short


class ShortLenghtError(ValueError):
    pass


class OriginalLenghtError(ValueError):
    pass


class GenerateShortError(Exception):
    pass
