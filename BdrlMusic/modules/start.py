print("Install start.py")
import asyncio
from datetime import datetime
from time import time

from pyrogram import filters
from pyrogram.errors import MessageDeleteForbidden, QueryIdInvalid
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from youtubesearchpython import VideosSearch

from BdrlMusic import bot, ubot
from BdrlMusic.config import OWNER_ID, PREFIXES
from BdrlMusic.utils.unpack import unpackInlineMessage

START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ("Minggu", 60 * 60 * 24 * 7),
    ("Hari", 60 * 60 * 24),
    ("Jam", 60 * 60),
    ("Menit", 60),
    ("Detik", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount} {unit}{"" if amount == 1 else ""}')
    return ", ".join(parts)


def YouTube_Search(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        id = data["id"]
        songname = data["title"]
        duration = data["duration"]
        url = f"https://youtu.be/{id}"
        views = data["viewCount"]["text"]
        channel = data["channel"]["name"]
        thumbnail = data["thumbnails"][0]["url"].split("?")[0]
        return [id, songname, duration, url, views, channel, thumbnail]
    except Exception as e:
        print(e)
        return 0


@ubot.on_message(filters.user(OWNER_ID) & filters.command("ping", PREFIXES))
@ubot.on_message(filters.me & filters.command("ping", PREFIXES))
async def _(_, message: Message):
    await _.get_me()
    start = time()
    current_time = datetime.utcnow()
    ping_ = await message.reply("⚡")
    delta_ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await asyncio.sleep(3)
    await ping_.edit("0% ▒▒▒▒▒▒▒▒▒▒")
    await asyncio.sleep(0.1)
    await ping_.edit("20% ██▒▒▒▒▒▒▒▒")
    await asyncio.sleep(0.1)
    await ping_.edit("40% ████▒▒▒▒▒▒")
    await asyncio.sleep(0.0)
    await ping_.edit("60% ██████▒▒▒▒")
    await asyncio.sleep(0.1)
    await ping_.edit("80% ████████▒▒")
    await asyncio.sleep(0.1)
    await ping_.edit("100% ██████████")
    await asyncio.sleep(0.1)
    _ping = f"""
<b>╭❏ PONG!!🏓
├ Pinger - {delta_ping * 1000:.3f} ms
╰ Aktif - {uptime}</b>
"""
    await ping_.edit(_ping)


@bot.on_message(filters.command("start", PREFIXES) & filters.private, group=2)
async def _(_, message: Message):
    if "InfoLagu" in message.text:
        return
    if "songDL" in message.text:
        return
    start = time()
    current_time = datetime.utcnow()
    ping_ = await message.reply("⚡")
    delta_ping = time() - start
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await asyncio.sleep(3)
    await ping_.edit("0% ▒▒▒▒▒▒▒▒▒▒")
    await asyncio.sleep(0.1)
    await ping_.edit("20% ██▒▒▒▒▒▒▒▒")
    await asyncio.sleep(0.1)
    await ping_.edit("40% ████▒▒▒▒▒▒")
    await asyncio.sleep(0.0)
    await ping_.edit("60% ██████▒▒▒▒")
    await asyncio.sleep(0.1)
    await ping_.edit("80% ████████▒▒")
    await asyncio.sleep(0.1)
    await ping_.edit("100% ██████████")
    await asyncio.sleep(0.1)
    try:
        OWNER = OWNER_ID[0]
    except:
        OWNER = None
    _ping = f"""
<b>╭❏ PONG!!🏓
├ Pinger - {delta_ping * 1000:.3f} ms
╰ Aktif - {uptime}</b>
"""
    await ping_.edit(
        _ping,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🧑‍💻 Owner", user_id=OWNER),
                    InlineKeyboardButton("Tutup 🗑", callback_data="_cls"),
                ]
            ]
        ),
    )


@bot.on_message(filters.regex("^/start (?P<any>.+)") & filters.private)
async def _(_, message: Message):
    txt = message.matches[0]["any"]
    vid_id = txt.split("_", 1)[1]
    get_info = await message.reply("<b>🔍 Sedang Mencari Informasi</b>")
    search = YouTube_Search(f"https://youtu.be/{vid_id}")
    videoid = search[0]
    title = search[1]
    duration = search[2]
    url = search[3]
    views = search[4]
    thumbnail = search[6]
    if "InfoLagu" in txt:
        await message.reply_photo(
            thumbnail,
            caption="💡 <b>Informasi Trek</b>\n\n🏷 <b>Nama:</b> {judul}\n⏱ <b>Durasi:</b> {durasi}\n👀 <b>Dilihat:</b> {views}\n🔗 <b>Tautan:</b> {link}\n\n⚡️️ <i>Powered by {owner}</i>".format(
                judul=title,
                durasi=duration,
                views=views,
                link=url,
                owner="<a href=tg://user?id=1883126074>Bdrl</a>",
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🗑 Tutup 🗑",
                            callback_data="_cls",
                        )
                    ],
                ]
            ),
        )
        await get_info.delete()
    if "songDL" in txt:
        await message.reply_photo(
            thumbnail,
            caption=f"""
<b>🏷 Nama:</b> {title}
<b>🧭 Durasi:</b> {duration}

<b>Pilih Metode Download</b>
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔈 Unduh Audio ",
                            callback_data=f"ytdl_{videoid}_Audio",
                        ),
                        InlineKeyboardButton(
                            "Unduh Video 🎥",
                            callback_data=f"ytdl_{videoid}_Video",
                        ),
                    ],
                    [InlineKeyboardButton("🗑 Tutup 🗑", callback_data="_cls")],
                ]
            ),
        )
        await get_info.delete()


@bot.on_callback_query(filters.regex("^_cls"))
async def _(_, cq: CallbackQuery):
    try:
        await cq.answer()
    except QueryIdInvalid:
        pass
    try:
        if cq.message:
            await cq.message.delete()
        if cq.from_user and cq.from_user.id == int(cq.data.split(None, 1)[1]):
            unPacked = unpackInlineMessage(cq.inline_message_id)
            for ub in ubot._ubot:
                try:
                    await ub.delete_messages(unPacked.chat_id, unPacked.message_id)
                except Exception:
                    pass
                else:
                    break
    except MessageDeleteForbidden:
        pass
