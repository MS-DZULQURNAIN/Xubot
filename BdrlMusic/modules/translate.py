print("Install translate.py")
import os

import gtts
from gpytranslate import Translator
from pyrogram import filters

from BdrlMusic import ubot
from BdrlMusic.config import PREFIXES


@ubot.on_message(filters.command(["tts"], PREFIXES))
async def _(_, message):
    if len(message.command) == 1:
        await message.delete()
        return
    if message.command[-1] not in gtts.lang.tts_langs():
        language = "id"
        words_to_say = " ".join(message.command[1:])
    else:
        language = message.command[-1]
        words_to_say = " ".join(message.command[1:-1])
    speech = gtts.gTTS(words_to_say, lang=language)
    speech.save("text_to_speech.oog")
    try:
        await _.send_voice(chat_id=message.chat.id, voice="text_to_speech.oog")
    except ChatSendMediaForbidden:
        await message.edit_text(
            "Pesan Suara tidak diizinkan di sini.\nSalin yang dikirim ke Pesan Tersimpan."
        )
        await _.send_voice(chat_id="me", voice="text_to_speech.oog")
        await asyncio.sleep(2)
    try:
        os.remove("text_to_speech.oog")
    except FileNotFoundError:
        pass
    await message.delete()


@ubot.on_message(filters.command(["tr", "tl"], PREFIXES))
async def _(client, message):
    trans = Translator()
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("Balas pesan untuk menerjemahkannya!")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = (
        f"<b>Diterjemahkan dari {source} ke {dest}</b>:\n"
        f"<code>{translation.text}</code>"
    )
    await message.reply_text(reply)
