import json

import aioredis
from loguru import logger

from src.abstract.transport import AbstractTransport
from src.dto.user import User


class RedisTransport(AbstractTransport):
    def __init__(self, url: str) -> None:
        self.redis = aioredis.from_url(url, encoding="utf-8", decode_responses=True)

    async def keys(self, pattern: str = '*') -> list[str]:
        return await self.redis.keys(pattern=pattern)

    async def load(self, key: tuple[int, int] | str) -> User | None:
        if isinstance(key, tuple):
            key = '{0}_{1}'.format(*key)
        u = await self.redis.get(key)
        try:
            if u:
                return User(**json.loads(u))
        except Exception as ex:
            logger.exception(ex)

    async def save(self, user: User) -> None:
        await self.redis.set(user.rkey(), user.json())
