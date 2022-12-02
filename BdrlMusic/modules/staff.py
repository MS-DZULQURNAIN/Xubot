print("Install staff.py")
from html import escape

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message

from BdrlMusic import ubot
from BdrlMusic.config import PREFIXES


@ubot.on_message(filters.command("staff", PREFIXES) & filters.group)
async def _(client, message: Message):
    chat_id = message.chat.id
    chat_title = message.chat.title
    creator = []
    co_founder = []
    admin = []
    admin_check = [member async for member in message.chat.get_members()]
    for x in admin_check:
        if (
            x.status == ChatMemberStatus.ADMINISTRATOR
            and x.can_promote_members
            and x.title
        ):
            title = escape(x.title)
            co_founder.append(
                f" <b>├</b> <a href='tg://user?id={x.user.id}'>{x.user.first_name}</a> <i>- {title}</i>"
            )
        elif x.status == ChatMemberStatus.ADMINISTRATOR and x.can_promote_members:
            co_founder.append(
                f" <b>├</b> <a href='tg://user?id={x.user.id}'>{x.user.first_name}</a>"
            )
        elif x.status == ChatMemberStatus.ADMINISTRATOR and x.title:
            title = escape(x.title)
            admin.append(
                f" <b>├</b> <a href='tg://user?id={x.user.id}'>{x.user.first_name}</a> <i>- {title}</i>"
            )
        elif x.status == ChatMemberStatus.ADMINISTRATOR:
            admin.append(
                f" <b>├</b> <a href='tg://user?id={x.user.id}'>{x.user.first_name}</a>"
            )
        elif x.status == ChatMemberStatus.OWNER and x.title:
            title = escape(x.title)
            creator.append(
                f" <b>└</b> <a href='tg://user?id={x.user.id}'>{x.user.first_name}</a> <i>- {title}</i>"
            )
        elif x.status == ChatMemberStatus.OWNER:
            creator.append(
                f" <b>└</b> <a href='tg://user?id={x.user.id}'>{x.user.first_name}</a>"
            )
    if not co_founder and not admin:
        result = (
            f"<b>STAFF GRUP</b> <b>{chat_title}</b>\n\n👑 <b>Pendiri</b>\n"
            + "\n".join(creator)
        )
    elif not co_founder and len(admin) > 0:
        res_admin = admin[-1].replace(" ├", " └")
        admin.pop(-1)
        admin.append(res_admin)
        result = (
            f"<b>STAFF GRUP</b> <b>{chat_title}</b>\n\n👑 <b>Pendiri</b>\n"
            + "\n".join(creator)
            + "\n\n"
            "👮🏼 <b>Admin</b>\n" + "\n".join(admin)
        )
    elif len(co_founder) > 0 and not admin:
        resco_founder = co_founder[-1].replace(" ├", " └")
        co_founder.pop(-1)
        co_founder.append(resco_founder)
        result = (
            f"<b>STAFF GRUP</b> <b>{chat_title}</b>\n\n👑 <b>Pendiri</b>\n"
            + "\n".join(creator)
            + "\n\n"
            "⚜️ <b>Wakil Pendiri</b>\n" + "\n".join(co_founder)
        )
    else:
        resco_founder = co_founder[-1].replace(" ├", " └")
        res_admin = admin[-1].replace(" ├", " └")
        co_founder.pop(-1)
        admin.pop(-1)
        co_founder.append(resco_founder)
        admin.append(res_admin)
        result = (
            f"<b>STAFF GRUP</b> <b>{chat_title}</b>\n\n👑 <b>Pendiri</b>\n"
            + "\n".join(creator)
            + "\n\n"
            "⚜️ <b>Wakil Pendiri</b>\n" + "\n".join(co_founder) + "\n\n"
            "👮🏼 <b>Admin</b>\n" + "\n".join(admin)
        )
        await client.send_message(chat_id, result)
