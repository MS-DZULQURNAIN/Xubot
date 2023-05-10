print("Install song.py")
import datetime
import os
from gc import *

import wget
from pyrogram import *
from pyrogram.errors import *
from pyrogram.types import *
from yt_dlp import *

from BdrlMusic import *
from BdrlMusic.config import *
from BdrlMusic.utils.unpack import *
from BdrlMusic.utils.youtube_search import *


async def download_yt(url, as_video=False):
    if as_video:
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
    else:
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "720",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        return f"<b>Gagal Mengunduh \nKesalahan:</b> {str(e)}", None, None, None
    yt_id = ytdl_data["id"]
    name = ytdl_data["title"]
    url = f"https://youtu.be/{yt_id}"
    dur = ytdl_data["duration"]
    uploader = ytdl_data["uploader"]
    views = f"{ytdl_data['view_count']:,}".replace(",", ".")
    thumb_image_path = f"https://img.youtube.com/vi/{yt_id}/hqdefault.jpg"
    file_name = f"{yt_id}.mp4" if as_video else f"{yt_id}.mp3"
    return file_name, name, url, dur, views, uploader, thumb_image_path


@ubot.on_message(filters.command("song", PREFIXES))
async def _(client, message: Message):
    if not message.from_user:
        return
    query = (
        (message.text or message.caption).split(None, 1)[1]
        if len(message.command) != 1
        else None
    )
    if not query:
        return await message.reply_text(
            "❌ <b>Video tidak ditemukan,</b>\nmohon masukan judul video dengan benar.",
        )
    infomsg = await message.reply_text("<b>🔍 Pencarian...</b>", quote=False)
    x = await client.get_inline_bot_results(bot.me.username, f"ytdl {id(message)}")
    for m in x.results:
        await message.reply_inline_bot_result(x.query_id, m.id)
    await infomsg.delete()


@bot.on_inline_query(filters.regex("^ytdl"))
async def owo(client, q):
    m = [obj for obj in get_objects() if id(obj) == int(q.query.split(None, 1)[1])][0]
    results = []
    search = YouTubeSearch(m.text.split(None, 1)[1], max_results=10).to_dict()
    videoid = search[0]["id"]
    title = search[0]["title"]
    duration = search[0]["duration"]
    thumbnail = f"https://img.youtube.com/vi/{videoid}/hqdefault.jpg"
    dl_btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="🔈 Audio ",
                    callback_data=f"ytdl_{videoid}_Audio",
                ),
                InlineKeyboardButton(
                    text="Video 🎥",
                    callback_data=f"ytdl_{videoid}_Video",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🗑 Tutup 🗑",
                    callback_data=f"_cls {m.from_user.id}",
                ),
            ],
        ]
    )
    caption = f"""
<b>🏷 Nama:</b> {title}
<b>🧭 Durasi:</b> {duration}
<b>Pilih Metode Download</b>
"""
    results.append(
        InlineQueryResultPhoto(
            photo_url=thumbnail,
            title=title,
            caption=caption,
            reply_markup=dl_btn,
        )
    )
    await client.answer_inline_query(q.id, cache_time=0, results=results)


@bot.on_callback_query(filters.regex(pattern="ytdl_(.*)_(Video|Audio)"))
async def yt_dl_video(client, cb):
    url = f"https://youtu.be/{cb.matches[0].group(1)}"
    audio_or_video = cb.matches[0].group(2)
    text_download = [
        "<b>Memulai Mendownload\n\nKecepatan pengunduhan mungkin lambat. Mohon tunggu sebentar...</b>",
        "<b>Memulai MengUpload\n\nKecepatan upload bisa lambat. Mohon tunggu sebentar...</b>",
        "<b>Sedang mengirim {}\n\nKecepatan mengirim mungkin lambat, Mohon tunggu sebentar...</b>",
        "<b>💡 Informasi {}</b>\n\n<b>🏷 Nama:</b> {}\n<b>🧭 Durasi:</b> {}\n<b>👀 Dilihat:</b> {}\n<b>📢 Channel:</b> {}\n<b>🔗 Tautan:</b> {}\n\n<b>⚡️️️ Powered By:</b> {}",
    ]
    await cb.edit_message_text(text_download[0])
    if audio_or_video == "Video":
        (
            file_name,
            name,
            url,
            dur,
            views,
            uploader,
            thumb_image_path,
        ) = await download_yt(url, as_video=True)
    else:
        (
            file_name,
            name,
            url,
            dur,
            views,
            uploader,
            thumb_image_path,
        ) = await download_yt(url, as_video=False)
    if not os.path.exists(file_name):
        return await cb.edit_message_text(file_name)
    thumbnail = wget.download(thumb_image_path)
    try:
        await cb.edit_message_text(text_download[1])
    except MessageNotModified:
        await cb.edit_message_text(text_download[2].format(audio_or_video))
    if audio_or_video == "video":
        file_ = InputMediaVideo(
            media=file_name,
            thumb=thumbnail,
            supports_streaming=True,
            duration=dur,
            caption=text_download[3].format(
                audio_or_video,
                name,
                datetime.timedelta(seconds=dur),
                views,
                uploader,
                url,
                "<a href=tg://user?id=1883126074>Bdrl</a>",
            ),
        )
    else:
        file_ = InputMediaAudio(
            media=file_name,
            thumb=thumbnail,
            title=name,
            performer=uploader,
            duration=dur,
            caption=text_download[3].format(
                audio_or_video,
                name,
                datetime.timedelta(seconds=dur),
                views,
                uploader,
                url,
                "<a href=tg://user?id=1883126074>Bdrl</a>",
            ),
        )
    await cb.edit_message_media(file_)
    if os.path.exists(file_name):
        os.remove(file_name)
