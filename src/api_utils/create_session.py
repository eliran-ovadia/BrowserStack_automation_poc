import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def create_session() -> requests.Session:
    headers = {
        "Content-Type": "application/json",
        "connection": "keep-alive",
    }
    session = requests.Session()
    session.headers.update(headers)
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session
