from collections.abc import Iterator

from fastapi import APIRouter

from app_name_snake_case.presentation.fastapi.routes.healthcheck import (
    healthcheck_router,
)
from app_name_snake_case.presentation.fastapi.routes.register_user import (
    register_user_router,
)
from app_name_snake_case.presentation.fastapi.routes.view_user import (
    view_user_router,
)


all_routers = (
    healthcheck_router,
    view_user_router,
    register_user_router,
)


class UnknownRouterError(Exception): ...


def ordered(*routers: APIRouter) -> Iterator[APIRouter]:
    for router in all_routers:
        if router not in routers:
            raise UnknownRouterError

        yield router
