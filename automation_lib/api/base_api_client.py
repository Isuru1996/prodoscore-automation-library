import requests


class BaseApiClient:
    def __init__(self, base_url, default_headers=None):
        self.base_url = base_url
        self.default_headers = default_headers or {"Accept": "application/json"}

    def get(self, endpoint, **kwargs):
        headers = {**self.default_headers, **kwargs.pop("headers", {})}
        return requests.get(f"{self.base_url}{endpoint}", headers=headers, **kwargs)

    def post(self, endpoint, data=None, json=None, **kwargs):
        headers = {**self.default_headers, **kwargs.pop("headers", {})}
        return requests.post(
            f"{self.base_url}{endpoint}",
            data=data,
            json=json,
            headers=headers,
            **kwargs,
        )

    # Add put, delete, etc. as needed
