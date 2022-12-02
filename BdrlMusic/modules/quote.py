print("Install quote.py")
import sys
import traceback
from functools import wraps
from io import BytesIO
from traceback import format_exc

import aiohttp
from pyrogram import filters
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from Python_ARQ import ARQ

from BdrlMusic import ubot
from BdrlMusic.config import PREFIXES

aiohttpsession = aiohttp.ClientSession()
arq = ARQ("arq.hamker.dev", "ZCHJFR-MWTULN-FVQPSZ-YNIABJ-ARQ", aiohttpsession)


def split_limits(text):
    if len(text) < 2048:
        return [text]

    lines = text.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line
    else:
        result.append(small_msg)

    return result


def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            await client.send_message(message.chat.id, "error")
            return
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            error_feedback = split_limits(
                "**ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n".format(
                    0 if not message.from_user else message.from_user.id,
                    0 if not message.chat else message.chat.id,
                    message.text or message.caption,
                    "".join(errors),
                ),
            )
            for x in error_feedback:
                await client.send_message(message.chat.id, x)
            raise err

    return capture


async def quotify(messages: list):
    response = await arq.quotly(messages)
    if not response.ok:
        return [False, response.result]
    sticker = response.result
    sticker = BytesIO(sticker)
    sticker.name = "sticker.webp"
    return [True, sticker]


def getArg(message) -> str:
    arg = message.text.strip().split(None, 1)[1].strip()
    return arg


def isArgInt(message) -> bool:
    count = getArg(message)
    try:
        count = int(count)
        return [True, count]
    except ValueError:
        return [False, 0]


@ubot.on_message(filters.command("q", PREFIXES))
@capture_err
async def _(client, message):
    if not message.reply_to_message.text:
        return await message.reply_text("Membalas Pesan Untuk Mengutipnya !")
    m = await message.reply_text("`Membuat kutipan Pesan...`")
    if len(message.command) < 2:
        messages = [message.reply_to_message]

    elif len(message.command) == 2:
        arg = isArgInt(message)
        if arg[0]:
            if arg[1] < 2 or arg[1] > 10:
                return await m.edit("Argumen harus antara 2-10.")
            count = arg[1]
            messages = await client.get_messages(
                message.chat.id,
                [
                    i
                    for i in range(
                        message.reply_to_message.id,
                        message.reply_to_message.id + count,
                    )
                ],
                replies=0,
            )
        else:
            if getArg(message) != "r":
                return await m.edit("**SORRY**`")
            reply_message = await client.get_messages(
                message.chat.id,
                message.reply_to_message.id,
                replies=1,
            )
            messages = [reply_message]
    else:
        await m.edit("**ERROR**")
        return
    try:
        sticker = await quotify(messages)
        if not sticker[0]:
            await message.reply_text(sticker[1])
            return await m.delete()
        sticker = sticker[1]
        await message.reply_sticker(sticker)
        await m.delete()
        sticker.close()
    except Exception as e:
        await m.edit(
            "Ada yang salah saat mengutip pesan, bisa"
            + " Kesalahan ini biasanya terjadi ketika ada "
            + " pesan yang berisi sesuatu selain teks."
        )
        e = format_exc()
        print(e)
