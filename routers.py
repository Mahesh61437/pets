from fastapi import APIRouter

# from common import constants
from fastapi.types import DecoratedCallable
from typing import Any, Callable


class CustomRouter(APIRouter):
    def api_route(
        self, path: str, *, include_in_schema: bool = True, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        if path.endswith("/"):
            path = path[:-1]

        add_path = super().api_route(
            path, include_in_schema=include_in_schema, **kwargs
        )

        alternate_path = path + "/"
        add_alternate_path = super().api_route(
            alternate_path, include_in_schema=False, **kwargs
        )

        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            add_alternate_path(func)
            return add_path(func)

        return decorator

# router = CustomRouter(prefix=constants.API_PREFIX)
router = CustomRouter()
# router.include_router(core_router)