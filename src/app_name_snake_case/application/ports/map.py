from abc import ABC, abstractmethod

from effect import LifeCycle

from app_name_snake_case.entities.core.user import User


type MappableEntityLifeCycle = LifeCycle[User]


class NotUniqueUserNameError(Exception): ...


class Map(ABC):
    @abstractmethod
    async def __call__(
        self,
        effect: MappableEntityLifeCycle,
        /,
    ) -> None:
        """
        :raises iam.application.ports.map.NotUniqueUserNameError:
        """
