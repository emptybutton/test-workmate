from dishka import Provider, Scope, make_async_container, provide

from app_name_snake_case.main.common.di import CommonProvider
from app_name_snake_case.presentation.fastapi.app import (
    FastAPIAppCoroutines,
    FastAPIAppRouters,
)
from app_name_snake_case.presentation.fastapi.routers import all_routers


class FastAPIProvider(Provider):
    scope = Scope.APP

    @provide
    def provide_routers(self) -> FastAPIAppRouters:
        return all_routers

    @provide
    def provide_coroutines(self) -> FastAPIAppCoroutines:
        return []


container = make_async_container(FastAPIProvider(), CommonProvider())
