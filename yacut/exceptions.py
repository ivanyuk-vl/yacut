class APIUsageError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


class ValidateOriginalError(ValueError):  # FIXME
    pass


class ValidateShortError(ValueError):  # FIXME
    pass


class OriginalRequiredError(ValueError):
    pass


class ShortExistsError(Exception):  # FIXME find parent
    pass  # TODO add short_id_name
