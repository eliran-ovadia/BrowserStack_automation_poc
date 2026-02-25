from api_client_v2.src.api.base_client import BaseClient
import os


class AuthAPI(BaseClient):
    def __init__(self):
        # We load the URL from env to keep it professional
        self.auth_domain = os.getenv("OAUTH_BASE_URL")
        self.api_domain = os.getenv("BASE_URL")
        super().__init__(default_base_url=self.api_domain)

    def login_flow(self, username, password):
        """
        Performs the 2-step authentication flow.
        Updates the session with all required tokens.
        """
        # --- STEP 1: Get Access Token ---
        payload = {
            "grant_type": "password",
            "client_id": os.getenv("CLIENT_ID"),
            "audience": os.getenv("AUDIENCE"),
            "username": username,
            "password": password,
            "scope": os.getenv("SCOPE", 'read:sample openid offline_access') # Example scope, adjust if needed
        }
        auth_endpoint = f"{self.auth_domain}/oauth/token"
        response_1 = self.post(auth_endpoint, json=payload)
        data_1 = response_1.json()

        access_token = data_1.get("access_token", '')
        if not access_token:
            raise ValueError("Failed to retrieve access_token from /oauth/token")

        self.update_headers({"access_token": f"Bearer {access_token}", "api-key": os.getenv('API_KEY')})
        self.logger.info("Step 1 Complete: Access Token retrieved.")

        # --- STEP 2: Call Dashboard/Skip ---
        # Since we updated the headers above, this call automatically sends the access_token
        response_2 = self.get("/api/V2/dashboard/skip")
        data_2 = response_2.json()

        # Extract the specific variables you need
        lbid = data_2.get("lbid")
        vt_token = data_2.get("vtToken")
        fmr_token = data_2.get("fmrToken")

        token_headers = {
            "lbid": lbid,
            "vtToken": vt_token,
            "fmrToken": fmr_token
        }
        # Remove None values just in case one is missing
        clean_headers = {k: v for k, v in token_headers.items() if v}

        self.update_headers(clean_headers)
        self.logger.info("Step 2 Complete: Auth Tokens (lbid, vt, fmr) configured.")

        return clean_headers