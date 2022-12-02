print("Install whois.py")
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.types import Message, User

from BdrlMusic import ubot
from BdrlMusic.config import PREFIXES


def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


infotext = (
    "<b><a href=tg://user?id={user_id}>{full_name}</a></b>\n"
    " <b>• ID Pengguna:</b> <code>{user_id}</code>\n"
    " <b>• Nama Depan:</b> <code>{first_name}</code>\n"
    " <b>• Nama Belakang:</b> <code>{last_name}</code>\n"
    " <b>• Username:</b> {username}\n"
    " <b>• DC:</b> {dc_id}\n"
    " <b>• Status:</b> {status}\n"
    " <b>• Apakah Penipu:</b> {scam}\n"
    " <b>• Apakah Bot:</b> {bot}\n"
    " <b>• Apakah Premium:</b> {premium}\n"
    " <b>• Diverifikasi:</b> {verifies}\n"
    " <b>• Apakah Kontak:</b> {contact}\n"
    " <b>• Total Grup yang Sama:</b> {common}"
)


@ubot.on_message(filters.command(["whois", "info"], PREFIXES))
async def who_is(client, message: Message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except RPCError:
            pass
    try:
        await message.delete()
        user = await client.get_users(get_user)
        msg = await message.reply(
            f"<b>🔄 Sedang Mengumpulkan Data Dari {user.mention}</b>"
        )
        await msg.delete()
    except RPCError:
        await message.reply("Saya tidak tahu Pengguna itu.")
        return
    common = await client.get_common_chats(user.id)
    # countpf = await client.get_chat_photos_count(user.id)
    async for pfp in client.get_chat_photos(user.id, 1):
        if pfp:
            await client.send_photo(
                message.chat.id,
                pfp.file_id,
                caption=infotext.format(
                    full_name=FullName(user),
                    user_id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name or "",
                    username=user.username or "",
                    dc_id=user.dc_id or "1",
                    status=user.status or "None",
                    premium=user.is_premium,
                    scam=user.is_scam,
                    bot=user.is_bot,
                    verifies=user.is_verified,
                    contact=user.is_contact,
                    common=len(common),
                ),
                reply_to_message_id=message.reply_to_message.id
                if message.reply_to_message
                else None,
            )
        else:
            await message.reply(
                infotext.format(
                    full_name=FullName(user),
                    user_id=user.id,
                    first_name=user.first_name,
                    last_name=user.last_name or "",
                    username=user.username or "",
                    dc_id=user.dc_id or "1",
                    status=user.status or "None",
                    premium=user.is_premium,
                    scam=user.is_scam,
                    bot=user.is_bot,
                    verifies=user.is_verified,
                    contact=user.is_contact,
                    common=len(common),
                ),
                disable_web_page_preview=True,
            )
