print("Install restrict.py")
from pyrogram import filters
from pyrogram.types import ChatPermissions, Message

from BdrlMusic import ubot
from BdrlMusic.config import PREFIXES
from BdrlMusic.utils import require_admin

# Mute Permissions
mute_permission = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_send_polls=False,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


# Unmute permissions
unmute_permissions = ChatPermissions(
    can_send_messages=True,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_send_polls=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False,
)


@ubot.on_message(
    filters.command(["kick", "ban", "mute", "unmute", "unban"], PREFIXES)
    & filters.group
)
@require_admin("can_restrict_members")
async def _(client, message: Message):
    if message.command[0] == "kick":
        if len(message.command) < 2:
            user = message.reply_to_message.from_user.id
        else:
            user = message.text.split()[1]
        await client.resolve_peer(user)
        get_user = await client.get_users(user)
        await message.chat.ban_member(get_user.id)
        await message.reply(f"Selamat tinggal, {get_user.mention}.")
        await message.chat.unban_member(get_user.id)
    elif message.command[0] == "ban":
        if len(message.command) < 2:
            user = message.reply_to_message.from_user.id
        else:
            user = message.text.split()[1]
        await client.resolve_peer(user)
        get_user = await client.get_users(user)
        await message.chat.ban_member(get_user.id)
        await message.reply(f"{get_user.mention} telah dilarang tanpa batas waktu.")
    elif message.command[0] == "mute":
        if len(message.command) < 2:
            user = message.reply_to_message.from_user.id
        else:
            user = message.text.split()[1]
        await client.resolve_peer(user)
        get_user = await client.get_users(user)
        await client.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=get_user.id,
            permissions=mute_permission,
        )
        await message.reply(f"{get_user.mention} telah dibungkam tanpa batas.")
    elif message.command[0] == "unmute":
        if len(message.command) < 2:
            user = message.reply_to_message.from_user.id
        else:
            user = message.text.split()[1]
        await client.resolve_peer(user)
        get_user = await client.get_users(user)
        await client.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=get_user.id,
            permissions=unmute_permissions,
        )
        await message.reply(
            f"{get_user.mention}, Anda dapat mengirim pesan di sini sekarang."
        )
    elif message.command[0] == "unban":
        if len(message.command) < 2:
            user = message.reply_to_message.from_user.id
        else:
            user = message.text.split()[1]
        await client.resolve_peer(user)
        get_user = await client.get_users(user)
        await message.chat.unban_member(get_user.id)
        await message.reply(
            f"Selamat {get_user.mention} Anda telah dibatalkan pemblokirannya."
            " Ikuti aturannya dan berhati-hatilah mulai sekarang."
        )
