from urllib.parse import urljoin

from requests.adapters import HTTPAdapter
from requests_toolbelt.sessions import BaseUrlSession


class RequestsSession(BaseUrlSession):
    def __init__(self, base_url=None):
        if base_url:
            self.base_url = base_url + "/"
        super(BaseUrlSession, self).__init__()

    def create_url(self, url):
        return urljoin(self.base_url, url.lstrip("/"))


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, timeout, *args, **kwargs):
        self.timeout = timeout
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def getSession(base_url: str = None, timeout: int = 10, retries: int = 6):
    session = RequestsSession(base_url=base_url)
    adapter = TimeoutHTTPAdapter(timeout=timeout, max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session
