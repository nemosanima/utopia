import json
from typing import Any


class Response:
    def __init__(
        self,
        storage: dict,
        body: Any = "",
        status_code: int = 200,
        headers: dict = None,
    ) -> None:
        self.headers = self._get_base_headers()
        if headers:
            self._update_headers(headers)

        self.body = body
        if body:
            self._update_body(body)

        self.status_code = status_code
        self._storage = storage

    def __getattr__(self, item):
        return self._storage.get(item)

    def _update_body(self, body: Any) -> None:
        self.body = json.dumps(body).encode("utf-8")
        self._update_headers({"Content-Length": str(len(self.body))})

    def _get_base_headers(self) -> dict:
        return {
            "Content-Type": "text/plain; charset=utf-8",
            "Content-Length": "0",
        }

    def _update_headers(self, headers: dict) -> None:
        self.headers.update(headers)
