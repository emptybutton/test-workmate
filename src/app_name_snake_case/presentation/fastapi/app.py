import asyncio
from collections.abc import AsyncIterator, Coroutine, Iterable
from contextlib import asynccontextmanager, suppress
from typing import Any, cast

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import APIRouter, FastAPI
from fastapi.openapi.constants import REF_TEMPLATE
from pydantic import BaseModel

from app_name_snake_case.presentation.fastapi.tags import tags_metadata


type FastAPIAppCoroutines = Iterable[Coroutine[Any, Any, Any]]
type FastAPIAppRouters = Iterable[APIRouter]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    with suppress(asyncio.CancelledError):
        async with asyncio.TaskGroup() as tasks:
            for coroutine in cast("FastAPIAppCoroutines", app.state.coroutines):
                tasks.create_task(coroutine)

            yield

            await app.state.dishka_container.close()
            raise asyncio.CancelledError


class _FastAPIWithAdditionalModels(FastAPI):
    __additional_model_types: tuple[type[BaseModel], ...] = tuple()

    def openapi(self) -> dict[str, Any]:
        if self.openapi_schema is not None:
            return self.openapi_schema

        schema = super().openapi()

        for model_type in self.__additional_model_types:
            schema["components"]["schemas"][model_type.__name__] = (
                model_type.model_json_schema(ref_template=REF_TEMPLATE)
            )

        return schema


async def app_from(container: AsyncContainer) -> FastAPI:
    author_url = "https://github.com/emptybutton"
    repo_url = f"{author_url}/app_name_snake_case"
    version = "0.1.0"

    app = _FastAPIWithAdditionalModels(
        title="app-name-kebab-case",
        version=version,
        summary="app_name_description.",
        openapi_tags=tags_metadata,
        contact={"name": "Alexander Smolin", "url": author_url},
        license_info={
            "name": "Apache 2.0",
            "url": f"{repo_url}/blob/main/LICENSE",
        },
        lifespan=lifespan,
        root_path=f"/api/{version}",
    )

    coroutines = await container.get(FastAPIAppCoroutines)
    routers = await container.get(FastAPIAppRouters)

    app.state.coroutines = coroutines

    for router in routers:
        app.include_router(router)

    setup_dishka(container=container, app=app)

    return app
