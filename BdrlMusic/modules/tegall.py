print("Install tagall.py")
import asyncio
from random import shuffle

from pyrogram import filters
from pyrogram.types import Message

from BdrlMusic import ubot
from BdrlMusic.config import PREFIXES

tagallgcid = []


@ubot.on_message(filters.command(["tagall", "batal"], PREFIXES) & filters.group)
async def _(client, message: Message):
    if message.command[0] == "tagall":
        if message.chat.id in tagallgcid:
            return
        tagallgcid.append(message.chat.id)
        text = message.text.split(None, 1)[1] if len(message.command) != 1 else ""
        users = [
            member.user.mention
            async for member in message.chat.get_members()
            if not (member.user.is_bot or member.user.is_deleted)
        ]
        shuffle(users)
        m = message.reply_to_message or message
        for output in [users[i : i + 5] for i in range(0, len(users), 5)]:
            if message.chat.id not in tagallgcid:
                break
            await asyncio.sleep(1.5)
            await m.reply_text(
                ", ".join(output) + "\n\n" + text, quote=bool(message.reply_to_message)
            )
        try:
            tagallgcid.remove(message.chat.id)
        except Exception:
            pass
    elif message.command[0] == "batal":
        if message.chat.id not in tagallgcid:
            return await message.reply_text("lol")
        try:
            tagallgcid.remove(message.chat.id)
        except Exception:
            pass
        await message.reply_text("ok tagall berhasil dibatalkan")
