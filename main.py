import asyncio
import logging
import os
import platform
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

LOG_ARGS = dict(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
if platform.system() == "Windows":
    LOG_ARGS["filename"] = "C:\\Users\\LENOVO\\Desktop\\bot3_log.txt"
    LOG_ARGS["filemode"] = "w"
logging.basicConfig(**LOG_ARGS)

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from handlers import router

TOKEN = os.getenv("BOT_TOKEN_2")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN_2 environment variable is not set")
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="Markdown"))
dp = Dispatcher()

async def main():
    dp.include_router(router)
    while True:
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)
        except Exception as e:
            logging.error(f"Connection error: {e}, retrying in 15s")
        await asyncio.sleep(15)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
