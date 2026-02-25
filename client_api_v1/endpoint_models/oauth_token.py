class OauthToken:
    def __init__(self, **kwargs):
        self._access_token = kwargs.get("access_token")

    def get_access_token(self):
        return self._access_token
