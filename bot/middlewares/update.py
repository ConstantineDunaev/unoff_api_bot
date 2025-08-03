from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from logging import getLogger
from db import connection_context

logger = getLogger('UPDATE_MIDDLEWARE')


class UpdateMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        logger.debug("%s", event.model_dump(exclude_none=True))
        async with connection_context() as connection:
            data['connection'] = connection
            result = await handler(event, data)
            return result
