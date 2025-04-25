from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

import jwt as pyjwt

from app_name_snake_case.application.ports.user_id_signing import (
    UserIDSigning,
)
from app_name_snake_case.infrastructure.app_name_snake_case.alias import JWT


@dataclass(kw_only=True, frozen=True, slots=True)
class UserIDSigningAsIdentification(UserIDSigning[UUID | None]):
    async def signed_user_id_when(self, *, user_id: UUID) -> UUID:
        return user_id

    async def user_id_when(self, *, signed_user_id: UUID | None) -> UUID | None:
        return signed_user_id


@dataclass(kw_only=True, frozen=True, slots=True)
class UserIDSigningToHS256JWT(UserIDSigning[JWT]):
    secret: str = field(repr=False)

    async def signed_user_id_when(self, *, user_id: UUID) -> JWT:
        return pyjwt.encode({"id": user_id.hex}, self.secret, algorithm="HS256")

    async def user_id_when(self, *, signed_user_id: JWT) -> UUID | None:
        jwt = signed_user_id

        try:
            user_data: dict[str, Any]
            user_data = pyjwt.decode(jwt, self.secret, algorithms="HS256")
        except pyjwt.DecodeError:
            return None

        user_id_hex: str | None = user_data.get("id")

        if user_id_hex is None:
            return None

        try:
            return UUID(hex=user_id_hex)
        except ValueError:
            return None
