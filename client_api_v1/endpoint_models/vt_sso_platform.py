class VtSsoPlatform:
    def __init__(self, **kwargs):
        self._sessionId = kwargs.get("sessionId")

    def get_sessionId(self):
        return self._sessionId
