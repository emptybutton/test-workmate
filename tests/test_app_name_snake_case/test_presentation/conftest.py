from dishka import AsyncContainer, Provider, Scope, make_async_container
from pytest import fixture


@fixture
def container() -> AsyncContainer:
    provider = Provider(scope=Scope.APP)

    return make_async_container(provider)
