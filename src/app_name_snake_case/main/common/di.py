from collections.abc import AsyncIterator

from dishka import AnyOf, Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from app_name_snake_case.application.ports.clock import Clock
from app_name_snake_case.application.ports.map import Map
from app_name_snake_case.application.ports.transaction import Transaction
from app_name_snake_case.application.ports.user_id_signing import (
    UserIDSigning,
)
from app_name_snake_case.application.ports.user_views import UserViews
from app_name_snake_case.application.ports.users import Users
from app_name_snake_case.application.register_user import RegisterUser
from app_name_snake_case.application.view_user import ViewUser
from app_name_snake_case.infrastructure.adapters.clock import LocalHostClock
from app_name_snake_case.infrastructure.adapters.map import MapToPostgres
from app_name_snake_case.infrastructure.adapters.transaction import (
    in_postgres_transaction_when,
)
from app_name_snake_case.infrastructure.adapters.user_id_signing import (
    UserIDSigningToHS256JWT,
)
from app_name_snake_case.infrastructure.adapters.users import InPostgresUsers
from app_name_snake_case.infrastructure.app_name_snake_case.alias import JWT
from app_name_snake_case.infrastructure.typenv.envs import Envs
from app_name_snake_case.presentation.adapters.user_views import (
    UserSchemasFromPostgres,
)
from app_name_snake_case.presentation.fastapi.schemas.output import UserSchema


class CommonProvider(Provider):
    provide_envs = provide(source=Envs.load, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def provide_postgres_engine(self, envs: Envs) -> AsyncEngine:
        return create_async_engine(envs.postgres_url)

    @provide(scope=Scope.REQUEST)
    async def provide_postgres_session(
        self, engine: AsyncEngine
    ) -> AsyncIterator[AsyncSession]:
        session = AsyncSession(
            engine,
            autoflush=False,
            expire_on_commit=False,
            autobegin=False,
        )

        async with session:
            yield session

    @provide(scope=Scope.APP)
    def provide_user_id_signing(
        self, envs: Envs
    ) -> AnyOf[UserIDSigningToHS256JWT, UserIDSigning[JWT]]:
        return UserIDSigningToHS256JWT(secret=envs.jwt_secret)

    @provide(scope=Scope.REQUEST)
    def provide_users(
        self, session: AsyncSession
    ) -> AnyOf[InPostgresUsers, Users]:
        return InPostgresUsers(session=session)

    provide_clock = provide(
        LocalHostClock,
        provides=AnyOf[LocalHostClock, Clock],
        scope=Scope.APP,
    )

    provide_map = provide(
        MapToPostgres,
        provides=AnyOf[Map, MapToPostgres],
        scope=Scope.REQUEST,
    )

    @provide(scope=Scope.REQUEST)
    def provide_transaction(
        self, session: AsyncSession
    ) -> Transaction:
        return in_postgres_transaction_when(session=session)

    provide_user_views = provide(
        UserSchemasFromPostgres,
        provides=AnyOf[
            UserViews[UserSchema, UserSchema | None], UserSchemasFromPostgres
        ],
        scope=Scope.REQUEST,
    )

    provide_register_user = provide(
        RegisterUser[JWT, UserSchema, UserSchema | None],
        provides=RegisterUser[str, UserSchema, UserSchema | None],
        scope=Scope.REQUEST
    )
    provide_view_user = provide(
        ViewUser[JWT, UserSchema, UserSchema | None],
        provides=ViewUser[str, UserSchema, UserSchema | None],
        scope=Scope.REQUEST,
    )
