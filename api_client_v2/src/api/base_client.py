import logging
import requests
from urllib.parse import urljoin


class BaseClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.logger = logging.getLogger(self.__class__.__name__)

        # Standard headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _request(self, method, endpoint, **kwargs):
        """Internal wrapper to handle full URLs and logging"""
        url = urljoin(self.base_url, endpoint)

        self.logger.info(f"{method.upper()} {url}")

        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()  # Raises error if status is 4xx or 5xx
            return response
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"API Request failed: {e.response.text}")
            raise

    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._request("POST", endpoint, **kwargs)

    def update_headers(self, new_headers: dict):
        """Helper to inject tokens into the session for future calls"""
        self.session.headers.update(new_headers)