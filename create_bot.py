from aiogram import Bot, Dispatcher, Router
import settings.config as config

TOKEN = config.BotToken
dp = Dispatcher()
router = Router()
bot = Bot(TOKEN, parse_mode="HTML")


async def send_error_message(name, func, exc):
    await bot.send_message(config.Owner_id, f"Module: {name}\n"
                                                   f"Func: {func}\n"
                                                   f"Excep: {exc}\n")


def print_error_message(name, func, exc):
    print(f"Module: {name}\n"
          f"Func: {func}\n"
          f"Excep: {exc}\n")
