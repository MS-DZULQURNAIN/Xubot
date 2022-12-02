print("Install gcast.py")
import asyncio

from pyrogram import filters
from pyrogram.errors import BadRequest
from pyrogram.types import Message

from BdrlMusic import ubot
from BdrlMusic.config import *


@ubot.on_message(filters.user(OWNER_ID) & filters.command(["gcast", "send"], PREFIXES))
@ubot.on_message(filters.me & filters.command(["gcast", "send"], PREFIXES))
async def _(client, message: Message):
    if message.command[0] == "gcast":
        sent = 0
        failed = 0
        msg = await message.reply("(|==•==|)")
        async for dialog in client.get_dialogs():
            try:
                if message.reply_to_message:
                    await message.reply_to_message.copy(dialog.chat.id)
                else:
                    if len(message.command) < 2:
                        await msg.delete()
                        return await message.reply(
                            "mohon balas sesuatu atau ketik sesuatu"
                        )
                    await client.send_message(
                        dialog.chat.id, message.text.split(None, 1)[1]
                    )
                sent = sent + 1
                await msg.edit(
                    f"🔄 Sedang Mengirim Pesan Global\n\n✅ Berhasil Terkirim: {sent} \n❌ Gagal Terkirim: {failed}"
                )
                await asyncio.sleep(0.5)
            except:
                failed = failed + 1
                await msg.edit(
                    f"🔄 Sedang Mengirim Pesan Global\n\n✅ Berhasil Terkirim: {sent} \n❌ Gagal Terkirim: {failed}"
                )
        await msg.delete()
        return await message.reply(
            f"💬 Mengirim Pesan Global Selesai\n\n✅ Berhasil Terkirim: {sent} \n❌ Gagal Terkirim: {failed}"
        )
    if message.command[0] == "send":
        if message.reply_to_message:
            if len(message.command) < 2:
                chat_id = message.chat.id
            else:
                chat_id = message.text.split()[1]
            await message.reply_to_message.copy(chat_id)
            tm = await message.reply(f"✅ Berhasil Dikirim Ke {chat_id}")
            await asyncio.sleep(2.5)
            await message.delete()
            await tm.delete()
            return
        try:
            chat_id = message.text.split()[1]
            chat_send = message.text.split(None, 2)[2]
        except TypeError as e:
            await message.reply(f"{e}")
        if len(chat_send) >= 2:
            try:
                await client.send_message(chat_id, chat_send)
                tm = await message.reply(f"✅ Berhasil Dikirim Ke {chat_id}")
                await asyncio.sleep(2.5)
                await message.delete()
                await tm.delete()
            except BadRequest as t:
                await message.reply(f"{t}")
