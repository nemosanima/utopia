from typing import Callable, Iterator

from parse import parse

from .middleware.base_middleware import BaseMiddleware
from .middleware.middewares import basic_middlewares
from .request import Request
from .response import Response
from .router import Router


class Utopia:
    def __init__(
        self,
        middlewares: list[BaseMiddleware] = None
    ) -> None:
        self.routers = {}
        self.middlewares = basic_middlewares
        if middlewares:
            self.middlewares = basic_middlewares.extend(middlewares)

    def __call__(
        self, environ: dict,
        start_response: Callable
    ) -> Iterator[bytes]:
        request = Request(environ)
        router, kwargs = self.find_router(environ["PATH_INFO"])
        if not router:
            response_body, status_code = self.not_found_response()
        else:
            if environ["REQUEST_METHOD"] not in router.methods:
                response_body, status_code = self.method_not_allowed_response()
            else:
                handler = router.handler
                response_body = handler(request, **kwargs)
                status_code = 200

        response = Response(request._storage, response_body, status_code)
        self.process_middlewares(request, response)

        start_response(str(response.status_code), response.headers.items())
        return iter([response.body])

    def router(self, path: str, methods: list[str]) -> Callable:
        def wrapper(handler):
            self.routers[path] = Router(handler, methods)
            return handler

        return wrapper

    def find_router(
        self,
        request_path: str
    ) -> tuple[Router, dict] | tuple[None, None]:
        for path, router in self.routers.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return router, parse_result.named
        return None, None

    def process_middlewares_to_request(self, request: Request) -> None:
        for middleware in self.middlewares:
            middleware().to_request(request)

    def process_middlewares_to_response(self, response: Response) -> None:
        for middleware in self.middlewares:
            middleware().to_response(response)

    def process_middlewares(self, request: Request, response: Response) -> None:
        self.process_middlewares_to_request(request)
        self.process_middlewares_to_response(response)

    def not_found_response(self) -> tuple[str, int]:
        return "Not Found", 404

    def method_not_allowed_response(self) -> tuple[str, int]:
        return "Method Not Allowed", 405
