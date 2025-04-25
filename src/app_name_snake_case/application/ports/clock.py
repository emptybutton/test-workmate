from abc import ABC, abstractmethod

from app_name_snake_case.entities.time.time import Time


class Clock(ABC):
    @abstractmethod
    async def get_current_time(self) -> Time: ...
