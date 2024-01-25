import json
from typing import Any
from urllib.parse import parse_qs


class Request:
    def __init__(self, environ: dict) -> None:
        self.path = environ.get('PATH_INFO')
        self.method = environ.get('REQUEST_METHOD')
        self.GET = parse_qs(environ.get('QUERY_STRING'))
        self.POST = self._get_post(environ)

    def _get_post(self, environ: dict) -> Any | None:
        content_length = int(environ.get("CONTENT_LENGTH", 0))
        if content_length > 0:
            body_bytes = environ["wsgi.input"].read(content_length)
            return json.loads(body_bytes.decode("utf-8"))
        return None
