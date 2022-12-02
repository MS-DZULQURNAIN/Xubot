import asyncio

from pyrogram import filters
from pyrogram.types import Message

from BdrlMusic import ubot
from BdrlMusic.config import PREFIXES


@ubot.on_message(filters.command("sg", PREFIXES))
async def sangmata(client, message: Message):
    m = message.reply_to_message or message
    if len(message.command) < 2:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.text.split()[1]
    chat = "@SangMataInfo_bot"
    apn = await m.reply(f"<b>🔎 Memeriksa Histori > {user_id}</b>")
    sent = await client.send_message(chat, f"/search_id {user_id}")
    await sent.delete()
    await apn.delete()
    async for msg in c.get_chat_history(chat, 4):
        for msg in msgs:
            if not msg.text:
                continue
            await asyncio.sleep(2)
            await msg.delete()
            if msg.text.startswith("No records found"):
                await apn.delete()
                return await message.reply_text(
                    "Tidak ada catatan yang ditemukan untuk pengguna ini"
                )
            if msg.text.startswith("🔗") or str(user_id) not in msg.text:
                continue
            await m.reply(msg.text)
