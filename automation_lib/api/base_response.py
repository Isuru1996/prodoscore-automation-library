class BaseApiResponse:
    def __init__(self, response):
        self.status_code = response.status_code
        self.headers = response.headers
        self.raw = response
        try:
            self.data = response.json()
        except Exception:
            self.data = None
