from abc import ABC, abstractmethod
from uuid import UUID


class UserIDSigning[SignedIDDataT](ABC):
    @abstractmethod
    async def signed_user_id_when(self, *, user_id: UUID) -> SignedIDDataT:
        ...

    @abstractmethod
    async def user_id_when(
        self, *, signed_user_id: SignedIDDataT
    ) -> UUID | None: ...
