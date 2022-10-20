from src.abstract.transport import AbstractTransport
from src.dto.user import User


class Cache:
    def __init__(self, transport: AbstractTransport) -> None:
        self._tr = transport

    async def keys(self, pattern: str = '*') -> list[str]:
        return await self._tr.keys(pattern)

    async def dall_users(self, pattern: str = '*') -> list[User]:
        keys = await self.keys(pattern)
        if not keys:
            return []
        return [await self._tr.load(k) for k in keys]

    async def all_chat_str(self, pattern: str = '*') -> str:
        data = await self.dall_users(pattern)
        return '\n'.join([i.__str__() for i in data])

    async def get(self, key: tuple[int, int] | str) -> User | None:
        return await self._tr.load(key)

    async def set(self, user: User) -> None:
        await self._tr.save(user)


