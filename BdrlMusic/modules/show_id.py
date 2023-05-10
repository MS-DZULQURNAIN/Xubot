print("Install show_id.py")
from pyrogram import filters
from pyrogram.enums import ChatType

from BdrlMusic import ubot
from BdrlMusic.config import PREFIXES
from BdrlMusic.utils.get_file_id import get_file_id


@ubot.on_message(filters.command(["id"], PREFIXES))
async def showid(client, message):
    chat_type = message.chat.type
    if chat_type == ChatType.PRIVATE:
        user_id = message.chat.id
        await message.reply_text(
            f"<b>ID {message.from_user.first_name} Adalah:</b> <code>{user_id}</code>",
            quote=True,
        )
    elif chat_type in [ChatType.GROUP, ChatType.SUPERGROUP, ChatType.CHANNEL]:
        _id = ""
        _id += (
            f"<b>ID {message.chat.title} Adalah:</b> <code>{message.chat.id}</code>\n\n"
        )
        if message.reply_to_message:
            _id += (
                f"<b>ID {message.reply_to_message.from_user.first_name} Adalah:</b> "
                f"<code>{message.reply_to_message.from_user.id}</code>\n\n"
            )
            file_info = get_file_id(message.reply_to_message)
            if file_info:
                _id += (
                    f"<b>ID {file_info.message_type} Adalah:</b> "
                    f"<code>{file_info.file_id}</code>\n"
                )
        else:
            _id += f"<b>ID {message.from_user.first_name} Adalah:</b> <code>{message.from_user.id}</code>\n\n"
            file_info = get_file_id(message)
            if file_info:
                _id += (
                    f"<b>{file_info.message_type}</b> Adalah: "
                    f"<code>{file_info.file_id}</code>\n"
                )
        m = message.reply_to_message or message
        await m.reply_text(_id, quote=True)
