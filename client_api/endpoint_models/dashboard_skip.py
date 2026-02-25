class DashboardSkip:
    def __init__(self, **kwargs):
        self._vtToken = kwargs.get("vtToken")
        self._fmToken = kwargs.get("fmrToken")
        self._connectionToken = kwargs.get("connectionToken")

    def get_vtToken(self):
        return self._vtToken

    def get_fmrToken(self):
        return self._fmToken

    def get_connectionToken(self):
        return self._connectionToken
