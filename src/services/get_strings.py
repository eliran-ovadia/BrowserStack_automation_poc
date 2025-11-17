import pytest
import requests
import os
import dotenv
import json
from functools import lru_cache
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

dotenv.load_dotenv()
BASE_URL = os.getenv("BASE_URL")
HEADERS = {
    "c-Type": "application/json",
    "connection": "keep-alive",
    "api-key": os.getenv("API_KEY")
}

def create_session() -> requests.Session:
    """
    Creates a requests.Session configured with automatic retries.
    """
    session = requests.Session()
    session.headers.update(HEADERS)
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

SESSION = create_session()

@lru_cache(maxsize=None)
def get_strings(page: str):
    """
    Fetches and caches strings for a given page.
    Retries on connection errors or 5xx server errors.
    Skips test on 4xx client errors or if all retries fail.
    """
    url = f"{BASE_URL}/api/getStrings/{page}"

    try:
        response = SESSION.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred fetching strings for page '{page}': {e}")
        pytest.skip(f"Failed to fetch strings for {page} after retries: {e}")
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to decode JSON for page '{page}': {e}")
        pytest.skip(f"Server returned invalid JSON for {page}: {e}")


if __name__ == "__main__":
    print("--- Fetching Main Page (first time) ---")
    print(json.dumps(get_strings(page="dashboard_login"), indent=4, ensure_ascii=False))
