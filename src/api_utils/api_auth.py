from typing import Callable

import pytest
import requests
import os
import dotenv
import json
from src.api_utils.create_session import SESSION
from endpoint_models.oauth_token import OauthToken
from endpoint_models.dashboard_skip import DashboardSkip
from endpoint_models.vt_sso_platform import VtSsoPlatform

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
OAUTH_BASE_URL = os.getenv("OAUTH_BASE_URL")
USERNAME = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
VT_TOKEN_URL = os.getenv("VT_TOKEN_URL")
SCOPE = os.getenv("SCOPE")
CLIENT_ID = os.getenv("CLIENT_ID")
AUDIENCE = os.getenv("AUDIENCE")


def handle_request(api_call: Callable[[], requests.Response], failure_context: str = "an error has occurred with the client"):
    """
    This function is an exception handler for all api calls
    :param api_call:
    :param failure_context:
    :return: response from the api_call
    """
    try:
        response = api_call()
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        status_code = getattr(e.response, '999')
        if 400 <= status_code < 500:
            pytest.skip(f"Client error ({status_code}) while trying to {failure_context}: {e}")
        else:
            pytest.fail(f"Failed to {failure_context} ({status_code}): {e}")
    except json.decoder.JSONDecodeError as e:
        pytest.skip(f"Server returned invalid JSON while trying to {failure_context}: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error during {failure_context}: {e}")


class ApiAuth:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = SESSION
        self.auth0_access_token = None
        self.vt_sessionId = None
        self.vtToken = None
        self.fmr_token = None
        self.connection_token = None
        self.refresh_tokens()

    def _fetch_auth0_access_token(self):
        url = f"{OAUTH_BASE_URL}/oauth/token"
        payload = {"grant_type": "password", "username": USERNAME, "password": PASSWORD, "scope": SCOPE,
                         "client_id": CLIENT_ID, "audience": AUDIENCE, "api-key": API_KEY}
        api_call = lambda: self.session.post(url, json=payload)
        response = handle_request(api_call=api_call, failure_context="fetch oauth token")
        self.auth0_access_token = OauthToken(**response).get_access_token()

    def _fetch_vt_sessionId(self):
        url = VT_TOKEN_URL
        payload = {'platform':'auth0', 'token': self.auth0_access_token}
        api_call = lambda: self.session.post(url, json=payload)
        response = handle_request(api_call=api_call, failure_context="fetch vt token")
        self.vt_sessionId = VtSsoPlatform(**response).get_sessionId()

    def _fetch_dashboard_skip(self):
        url = f"{BASE_URL}/api/V2/dashboard/skip"
        headers = {"access_token": self.auth0_access_token, "api-key": API_KEY}
        api_call = lambda: self.session.get(url, headers=headers)
        response = handle_request(api_call=api_call)
        dashboard_skip = DashboardSkip(**response)
        self.fmr_token = dashboard_skip.get_fmrToken()
        self.connection_token = dashboard_skip.get_connectionToken()
        self.vtToken = dashboard_skip.get_vtToken()

    def refresh_tokens(self):
        self._fetch_auth0_access_token()
        self._fetch_vt_sessionId()
        self._fetch_dashboard_skip()




if __name__ == "__main__":
    client = ApiAuth()
    x = 1
