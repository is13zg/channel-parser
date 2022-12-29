import logging
from create_bot import bot, dp
from core import handlers
import asyncio

logger = logging.getLogger(__name__)


async def main() -> None:
    dp.include_router(handlers.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
