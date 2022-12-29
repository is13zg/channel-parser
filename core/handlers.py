from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Router
import create_bot
import inspect
import core.parse as parser
import asyncio
import random
import utils.gsheet_by_lib

router = Router()


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    try:
        await message.answer(
            text="to parse any channel write \n/parse [one or more channel names or links] \n\n Пример: <pre>/parse https://t.me/TheBadComedian iskander_ahmadullin </pre>",
            parse_mode="HTML")
        return
    except Exception as e:
        await create_bot.send_error_message(__name__, inspect.currentframe().f_code.co_name, e)


@router.message(Command(commands=["parse"]))
async def command_parse_handler(message: Message) -> None:
    try:
        channels = message.text.split()
        if len(channels) == 1:
            await message.answer(f"Write any channels to parse")
            return
        if len(channels) > 1:
            channels = channels[1:]
            for channel in channels:
                if "https://t.me/" in channel:
                    channel = channel.replace("https://t.me/", "")
                elif "http://t.me/" in channel:
                    channel = channel.replace("http://t.me/", "")
                elif "t.me/" in channel:
                    channel = channel.replace("t.me/", "")

                await message.answer(f"star parsing {channel} ...", disable_notification=True,
                                     disable_web_page_preview=True)
                res = await parser.parse(channel, message.from_user.id)
                await utils.gsheet_by_lib.add_data_to_worksheet(channel, res)
                await message.answer(
                    f'Channels {channel} data in <a href="https://docs.google.com/spreadsheets/d/1FaeM9Rge76zFLa2V42BvzCxOhRl6V-bOVq0W7jtPvJs/edit?usp=sharing">google sheet</a>',
                    parse_mode="HTML", disable_notification=True, disable_web_page_preview=True)

                if channel != channels[-1]:
                    await asyncio.sleep(random.randint(60, 120))

            await message.answer(f"parsing finished")

    except Exception as e:
        await create_bot.send_error_message(__name__, inspect.currentframe().f_code.co_name, e)
