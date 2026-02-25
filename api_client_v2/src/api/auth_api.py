from api_client_v2.src.api.base_client import BaseClient
import os


class AuthAPI(BaseClient):
    def __init__(self):
        # We load the URL from env to keep it professional
        base_url = os.getenv("API_BASE_URL", "https://authdev.ibi.co.il")
        super().__init__(base_url)

    def login_and_get_tokens(self, username, password):
        """
        Performs the 2-step authentication flow.
        Updates the session with all required tokens.
        """
        # --- STEP 1: Get Access Token ---
        payload = {
            "grant_type": "password",
            "client_id": os.getenv("CLIENT_ID"),
            "audience": os.getenv("AUDIENCE"),
            "api-key": os.getenv("API_KEY"),
            "username": username,
            "password": password,
            "scope": os.getenv("SCOPE", 'read:sample openid offline_access') # Example scope, adjust if needed
        }

        # Note: OAuth often uses form-data, not JSON.
        # If your API needs form-data, use 'data=' instead of 'json='
        response_1 = self.post("/oauth/token", json=payload)
        data_1 = response_1.json()

        access_token = data_1.get("access_token")
        if not access_token:
            raise ValueError("Failed to retrieve access_token from /oauth/token")

        self.logger.info("Step 1 Complete: Access Token retrieved.")

        # Set the Bearer token for the NEXT request
        self.update_headers({"Authorization": f"Bearer {access_token}"})

        # --- STEP 2: Call Dashboard/Skip ---
        # Since we updated the headers above, this call automatically sends the access_token
        response_2 = self.post("/api/V2/dashboard/skip")
        data_2 = response_2.json()

        # Extract the specific variables you need
        lbid = data_2.get("lbid")
        vt_token = data_2.get("vtToken")
        fmr_token = data_2.get("fmrToken")

        # --- STEP 3: Save them for future use ---
        # We assume these need to be sent as headers in all future requests.
        # If they need to be cookies, requests.Session might have already handled 'lbid'.
        # But explicitly setting them as headers is safe.
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