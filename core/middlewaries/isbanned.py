from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Awaitable, Callable, Any, Dict
from core.db.db_utils import check_ban

class IsBanned(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        user_id = data["event_from_user"].id
        if not check_ban(user_id):
            return await handler(event, data)