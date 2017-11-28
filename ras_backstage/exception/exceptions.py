class ApiError(Exception):

    def __init__(self, url, status_code=None, data=None):
        super().__init__()
        self.url = url
        self.status_code = status_code
        self.data = data
