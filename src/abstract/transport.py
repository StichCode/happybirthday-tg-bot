from abc import ABC, abstractmethod

from src.dto.user import User


class AbstractTransport(ABC):

    @abstractmethod
    async def keys(self, chat_id: int | None = None) -> list[str]: ...

    @abstractmethod
    async def load(self, key: tuple[int, int] | str) -> User | None: ...

    @abstractmethod
    async def save(self, user: User) -> None: ...

