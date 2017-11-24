class ApiError(Exception):

    def __init__(self, url, status_code=None, data=None):
        super().__init__()
        self.url = url
        self.status_code = status_code
        self.data = data


class RasError(Exception):
    """
    RAS domain-specific errors.

    status_code defaults to 500, and is overridden at the point of raising by providing a custom status_code value.
    """
    status_code = 500

    def __init__(self, errors, status_code=None):
        """The ctor accepts either a string describing the error, or a list of strings
        if there are multiple lines of description.
        """
        self.errors = errors if isinstance(errors, list) else [errors]
        self.status_code = status_code or RasError.status_code

    def to_dict(self):
        return {'errors': self.errors}
