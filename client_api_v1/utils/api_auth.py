import json
import os
from typing import Callable

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import dotenv
import requests

from client_api_v1.endpoint_models.dashboard_skip import DashboardSkip
from client_api_v1.endpoint_models.oauth_token import OauthToken
from client_api_v1.endpoint_models.vt_sso_platform import VtSsoPlatform

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


class ApiAuth:
    def __init__(self):
        self.base_url = BASE_URL
        self.auth0_access_token = None
        self.vt_session_id = None
        self.vt_token = None
        self.fmr_token = None
        self.connection_token = None
        self.headers = None
        
        self.session = requests.Session()
        self.session_config()
        # refresh_tokens uses self.session, so it must be called after session initialization
        self.refresh_tokens()

    @staticmethod
    def handle_request(api_call: Callable[[], requests.Response], context: str = "an error has occurred with the client"):
        """
        This function is an exception handler for all api calls
        :param api_call:
        :param context:
        :return: response from the api_call
        """
        try:
            response = api_call()
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            status_code = e.response.status_code if e.response else None
            print(f"Error in {context}: {e}, Status Code: {status_code}")
            raise e
        except json.decoder.JSONDecodeError as e:
            print(f"JSON Decode Error in {context}: {e}")
            raise e
        except Exception as e:
            print(f"Unexpected Error in {context}: {e}")
            raise e

    def get_base_url(self):
        return self.base_url

    def get_session(self):
        return self.session

    def get_auth0_access_token(self):
        return self.auth0_access_token

    def get_vt_session_id(self):
        return self.vt_session_id

    def get_vt_token(self):
        return self.vt_token

    def get_fmr_token(self):
        return self.fmr_token

    def get_connection_token(self):
        return self.connection_token

    def _fetch_auth0_access_token(self):
        url = f"{OAUTH_BASE_URL}/oauth/token"
        payload = {"grant_type": "password", "username": USERNAME, "password": PASSWORD, "scope": SCOPE,
                   "client_id": CLIENT_ID, "audience": AUDIENCE, "api-key": API_KEY}
        api_call = lambda: self.session.post(url, json=payload)
        response = self.handle_request(api_call=api_call, context="fetch oauth token")
        self.auth0_access_token = OauthToken(**response).get_access_token()

    def _fetch_vt_session_id(self):
        url = VT_TOKEN_URL
        payload = {'platform': 'auth0', 'token': self.auth0_access_token}
        api_call = lambda: self.session.post(url, json=payload)
        response = self.handle_request(api_call=api_call, context="fetch vt token")
        self.vt_session_id = VtSsoPlatform(**response).get_sessionId()

    def _fetch_dashboard_skip(self):
        url = f"{BASE_URL}/api/V2/dashboard/skip"
        headers = {"access_token": self.auth0_access_token, "api-key": API_KEY}
        api_call = lambda: self.session.get(url, headers=headers)
        response = self.handle_request(api_call=api_call)
        dashboard_skip = DashboardSkip(**response)
        self.fmr_token = dashboard_skip.get_fmrToken()
        self.connection_token = dashboard_skip.get_connectionToken()
        self.vt_token = dashboard_skip.get_vtToken()

    def refresh_tokens(self):
        self._fetch_auth0_access_token()
        self._fetch_vt_session_id()
        self._fetch_dashboard_skip()
        self.headers = {
            "Content-Type": "application/json",
            "connection": "keep-alive",
            'Authorization': self.vt_token,
            'fmr_token': self.fmr_token,
            'access_token': self.auth0_access_token,
            'connection_token': self.connection_token,
        }
        self.session.headers.update(self.headers)

    def get_auth_headers(self):
        return self.headers

    def session_config(self):
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)