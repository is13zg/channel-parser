from pyrogram import Client
import settings.config as config
import asyncio
import create_bot
import inspect
from pyrogram.errors.exceptions.bad_request_400 import MsgIdInvalid
from pyrogram.errors.exceptions import BadRequest
from pyrogram.errors.exceptions.flood_420 import FloodWait
from random import randint

PERMANENTLY_EMPTY_CONST = 50


async def parse(channel_name: str, chat_id: int = config.Owner_id) -> list:
    try:
        cl = Client(name="me_client", api_id=config.api_id, api_hash=config.api_hash)
        await cl.start()
        res = []
        headers = ["id", "date", "type", "views", "forwards", "reactions", "comments", "url"]
        res.append(headers)
        permanently_empty = 0

        parse_chat_info = await cl.get_chat(channel_name)
        parse_chat_id = parse_chat_info.id
        await cl.join_chat(channel_name)

        if type(parse_chat_id) == int:
            if parse_chat_id < 0:
                await create_bot.bot.send_message(chat_id=chat_id, text=f"{channel_name} id is {parse_chat_id}...",
                                                  disable_notification=True)
        else:
            await create_bot.bot.send_message(chat_id=chat_id,
                                              text=f" can't get {channel_name} id is {parse_chat_id}...",
                                              disable_notification=True)

    except FloodWait as e:
        await create_bot.send_error_message(__name__, inspect.currentframe().f_code.co_name,
                                            f" channel {channel_name} \n msg_id={parse_chat_id} \n FloodWait: {e}")
        await asyncio.sleep(randint(28, 40))
        parse_chat_info = await cl.get_chat(channel_name)
        parse_chat_id = parse_chat_info.id

    except Exception as e:
        await create_bot.send_error_message(__name__, inspect.currentframe().f_code.co_name,
                                            f" channel {channel_name} \n msg_id={parse_chat_id} \n Exception: {e}")

    id = 1
    while True:
        try:
            old_id = id
            ms = await cl.get_messages(chat_id=parse_chat_id, message_ids=id)
            if not ms.empty:
                if ms.service:
                    permanently_empty = 0
                    id += 1
                    continue

                permanently_empty = 0
                td = {'id': id, "date": ms.date.date().strftime("%d.%m.%Y"), "type": None, 'views': -1, 'forwards': -1,
                      'reactions': -1, 'comments': -1, 'url': "https://t.me/" + channel_name}

                if ms.media:
                    td["type"] = str(ms.media).replace("MessageMediaType.", "")
                elif ms.poll:
                    td["type"] = str(ms.poll).replace("MessageMediaType.", "")
                else:
                    td["type"] = "text"

                td["views"] = ms.views
                td["forwards"] = ms.forwards
                if ms.reactions:
                    ls = ms.reactions.__dict__["reactions"]
                    count = 0
                    for x in ls:
                        count += x.count
                    td["reactions"] = count
                try:
                    # x = await asyncio.gather(cl.get_discussion_replies_count(chat_id=parse_chat_id, message_id=id))
                    td["comments"] = await cl.get_discussion_replies_count(chat_id=parse_chat_id, message_id=id)
                except MsgIdInvalid as e:
                    pass
                td["url"] = "https://t.me/" + channel_name + "/" + str(id)
                res.append(list(td.values()))

            else:
                if permanently_empty == PERMANENTLY_EMPTY_CONST:
                    await cl.leave_chat(channel_name)
                    await cl.stop()
                    return res
                permanently_empty += 1
                id += 1
                continue

            id += 1
            if id % 30 == 0:
                await asyncio.sleep(randint(4, 10))
            await asyncio.sleep(randint(3, 10) / 10)

            if id % 100 == 0:
                await create_bot.bot.send_message(chat_id=chat_id, text=f"parse about {id} posts in {channel_name}...",
                                                  disable_notification=True)
        except BadRequest as e:
            await create_bot.send_error_message(__name__, inspect.currentframe().f_code.co_name,
                                                f" channel {channel_name} \n msg_id={id} \n BadRequest: {e}")
            id = old_id
        except FloodWait as e:
            await create_bot.send_error_message(__name__, inspect.currentframe().f_code.co_name,
                                                f" channel {channel_name} \n msg_id={id} \n FloodWait: {e}")
            await asyncio.sleep(randint(28, 40))
            id = old_id

        except Exception as e:
            await create_bot.send_error_message(__name__, inspect.currentframe().f_code.co_name,
                                                f" channel {channel_name} \n msg_id={id} \n Exception: {e}")
