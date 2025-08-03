from aiogram.filters import BaseFilter, StateFilter
from config import Config


class IsAdmin(BaseFilter):
    async def __call__(self, *arg, **kwargs):
        user = kwargs.get('event_from_user')
        if not user:
            return False
        return user.id in Config.TELEGRAM_USERS
