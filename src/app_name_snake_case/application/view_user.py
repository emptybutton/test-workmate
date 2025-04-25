from dataclasses import dataclass

from app_name_snake_case.application.ports.transaction import Transaction
from app_name_snake_case.application.ports.user_id_signing import UserIDSigning
from app_name_snake_case.application.ports.user_views import UserViews


@dataclass(kw_only=True, frozen=True, slots=True)
class ViewUser[SignedUserIDT, UserViewT, UserViewWithIDT]:
    user_id_signing: UserIDSigning[SignedUserIDT]
    user_views: UserViews[UserViewT, UserViewWithIDT]
    transaction: Transaction

    async def __call__(
        self, signed_user_id: SignedUserIDT | None
    ) -> UserViewWithIDT:
        if signed_user_id is None:
            user_id = None
        else:
            user_id = await self.user_id_signing.user_id_when(
                signed_user_id=signed_user_id
            )

        async with self.transaction:
            return await self.user_views.view_of_user_with_id(user_id)
