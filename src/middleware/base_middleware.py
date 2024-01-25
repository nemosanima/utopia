from ..request import Request
from ..response import Response


class BaseMiddleware:
    def to_request(self, request: Request) -> None:
        pass

    def to_response(self, response: Response) -> None:
        pass
