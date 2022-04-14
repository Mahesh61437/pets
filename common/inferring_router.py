import json
from typing import Callable, Any, Optional, Dict, List, Union
from typing import TYPE_CHECKING, get_type_hints

from fastapi import APIRouter
from fastapi import status as http_status_codes
from fastapi.routing import APIRoute
from pydantic.main import BaseModel
from starlette.responses import Response


class JSONResponse(Response):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:

        self.status_code = content.pop('status_code', http_status_codes.HTTP_200_OK)

        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=True,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")


class JSONResponseModel(BaseModel):
    total: Optional[int]
    page: Optional[int]
    count: Optional[int]
    status: Optional[bool] = True
    data: Optional[Union[List[Any], Dict]]
    message: Optional[str] = "Successful"
    previous: Optional[str]
    next: Optional[str]
    status_code: Optional[int] = http_status_codes.HTTP_200_OK


class Route(APIRoute):
    def __init__(self, path: str, endpoint: Callable[..., Any], **kwargs: Any) -> None:
        kwargs['response_model'] = JSONResponseModel
        super().__init__(path, endpoint, **kwargs)


class InferringRouter(APIRouter):
    """
    Overrides the route decorator logic to use the annotated return type as the `response_model` if unspecified.
    """

    def __init__(self, **kwargs: Any) -> None:
        kwargs['route_class'] = Route
        kwargs['default_response_class'] = JSONResponse
        super().__init__(**kwargs)

    if not TYPE_CHECKING:  # pragma: no branch

        def add_api_route(self, path: str, endpoint: Callable[..., Any], **kwargs: Any) -> None:
            if kwargs.get("response_model") is None:
                kwargs["response_model"] = get_type_hints(endpoint).get("return")
            return super().add_api_route(path, endpoint, **kwargs)
