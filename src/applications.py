import json


class App:
    def __init__(self):
        self.routers = {}

    def __call__(self, environ, start_response):
        handler = self.find_handler(environ['PATH_INFO'])
        if handler:
            data = handler()
            response_body = json.dumps(data).encode("utf-8")
            status_code = "200"
        else:
            response_body, status_code = self.not_found_response()

        start_response(
            status_code,
            [
                ("Content-Type", "application/json; charset=utf-8"),
                ("Content-Length", str(len(response_body)))
            ]
        )
        return iter([response_body])

    def router(self, path: str):
        def wrapper(handler):
            self.routers[path] = handler
            return handler
        return wrapper

    def find_handler(self, requested_path: str):
        for path, handler in self.routers.items():
            if path == requested_path:
                return handler
        return None

    def not_found_response(self):
        return b"Not Found", "404"






