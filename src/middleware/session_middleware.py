from uuid import uuid4

from ..request import Request
from ..response import Response


class SessionMiddleware:
    def to_request(self, request: Request) -> None:
        session = request.cookies.get("session_id")
        if session:
            request._storage["session_id"] = session.value

    def to_response(self, response: Response) -> None:
        if not response.session_id:
            response._update_headers({"Set-Cookie": f"session_id={uuid4()}"})
