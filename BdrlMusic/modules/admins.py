print("Install admins.py")
from asyncio import QueueEmpty

from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.exceptions import NoActiveGroupCall, NotInGroupCallError

from BdrlMusic import ubot
from BdrlMusic.config import PREFIXES
from BdrlMusic.core.pytgcalls import queues
from BdrlMusic.utils import require_admin


@ubot.on_message(filters.command("pause", PREFIXES) & filters.group)
@require_admin("can_manage_video_chats")
async def _(client, message: Message):
    chat_id = message.chat.id
    await client.call_py.pause_stream(chat_id)
    await message.reply_text(
        "⏸ <b>Lagu dijeda.</b>\n\n• Untuk melanjutkan pemutaran, gunakan <b>perintah</b> » /resume.",
        quote=False,
    )


@ubot.on_message(filters.command("resume", PREFIXES) & filters.group)
@require_admin("can_manage_video_chats")
async def _(client, message: Message):
    chat_id = message.chat.id
    await client.call_py.resume_stream(chat_id)
    await message.reply_text(
        "▶️ <b>Melanjutkan pemutaran lagu yang dijeda.</b>\n\n• Untuk menjeda pemutaran, gunakan <b>perintah</b> » /pause.",
        quote=False,
    )


@ubot.on_message(filters.command(["end", "stop"], PREFIXES) & filters.group)
@require_admin("can_manage_video_chats")
async def _(client, message: Message):
    chat_id = message.chat.id
    try:
        queues.clear(chat_id)
    except QueueEmpty:
        pass
    try:
        await client.call_py.leave_group_call(chat_id)
        await message.reply_text(
            "✅ <i>Userbot telah terputus dari obrolan video.</i>", quote=False
        )
    except (NotInGroupCallError, NoActiveGroupCall):
        pass


@ubot.on_message(filters.command(["skip", "next"], PREFIXES) & filters.group)
@require_admin("can_manage_video_chats")
async def _(client, message: Message):
    chat_id = message.chat.id
    queues.task_done(chat_id)
    await client.call_py.change_stream(chat_id, queues.get(chat_id)["file"])
    await message.reply_text(
        "⏭ <b>Anda telah melompat ke music/video berikutnya.</b>", quote=False
    )
