import pytest
import requests
import os
import dotenv
import json
from functools import lru_cache
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
AUTH_DEV = os.getenv("AUTH_DEV")
USERNAME = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
VT_TOKEN_URL = os.getenv("VT_TOKEN_URL")
HEADERS = {
    "Content-Type": "application/json",
    "connection": "keep-alive",
    "api-key": API_KEY
}

def _create_session() -> requests.Session:
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

SESSION = _create_session()

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
        print(f"fetched strings for page {page} succesfully")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred fetching strings for page '{page}': {e}")
        pytest.skip(f"Failed to fetch strings for {page} after retries: {e}")
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to decode JSON for page '{page}': {e}")
        pytest.skip(f"Server returned invalid JSON for {page}: {e}")

def post_auth():
    url = f"{AUTH_DEV}/oauth/token"
    payload = {"grant_type": "password",
               "username": USERNAME,
               "password": PASSWORD,
               "scope": "read:sample openid offline_access",
               "client_id": os.getenv("CLIENT_ID"),
               "audience": os.getenv("AUDIENCE")
            }
    try:
        response = SESSION.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("An error occurred fetching token for authentication")
        #pytest.fail(f"Failed to fetch token for authentication: {e}")
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to decode JSON for auth token: {e}")
        #pytest.fail(f"Server returned invalid JSON for auth token: {e}")

def post_skip_dashboard():
    skip_dashboard_url = f"{BASE_URL}/api/V2/dashboard/skip"
    auth = post_auth()
    vt_headers = {
        "Content-Type": "application/json",
        "connection": "keep-alive"
    }
    vt_payload = {
        "platform": "auth0-sso",
        "token": auth["access_token"],
    }
    skip_dashboard_headers = {
        'access_token': auth["access_token"],
    }
    try:
        vt_response = SESSION.post(VT_TOKEN_URL, json=vt_payload, headers=vt_headers)
        vt_response.raise_for_status()
        SESSION.headers.update(skip_dashboard_headers)
        skip_dashboard_response = SESSION.get(skip_dashboard_url)
        skip_dashboard_response.raise_for_status()
        return skip_dashboard_response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred fetching VT token: {e}")
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to decode JSON for VT token: {e}")




if __name__ == "__main__":
    # print("--- Fetching Main Page (first time) ---")
    # print(json.dumps(get_strings(page="dual_portfolio"), indent=4, ensure_ascii=False))
    #print(json.dumps(post_auth_dev(), indent=4))
    print(json.dumps(post_skip_dashboard(), indent=4))
