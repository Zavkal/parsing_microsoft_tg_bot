from aiogram import BaseMiddleware
from typing import Callable, Any, Awaitable

class DBMiddleware(BaseMiddleware):
    def __init__(self, db):
        self.db = db

    async def __call__(self, handler: Callable, event: Any, data: dict[str, Any]):
        data['db'] = self.db
        await handler(event, data)