import json


from .router import Router
from .request import Request


class App:
    def __init__(self):
        self.routers = {}

    def __call__(self, environ, start_response):

        router = self.find_router(environ['PATH_INFO'])
        if not router:
            response_body, status_code = self.not_found_response()
        else:
            if environ["REQUEST_METHOD"] not in router.methods:
                response_body, status_code = self.method_not_allowed_response()
            else:
                request = Request(environ)
                handler = router.handler
                data = handler(request)
                response_body = json.dumps(data).encode("utf-8")
                status_code = "200"

        start_response(
            status_code,
            [
                ("Content-Type", "application/json; charset=utf-8"),
                ("Content-Length", str(len(response_body)))
            ]
        )
        return iter([response_body])

    def router(self, path: str, methods: list[str]):
        def wrapper(handler):
            self.routers[path] = Router(handler, methods)
            return handler
        return wrapper

    def find_router(self, request_path: str):
        return self.routers.get(request_path)

    def not_found_response(self):
        return b"Not Found", "404"

    def method_not_allowed_response(self):
        return b"Method Not Allowed", "405"
