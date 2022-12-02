print("Install add_ubot.py")
import asyncio
import importlib
import os

from pyrogram import filters
from pyrogram.errors import *
from pyrogram.types import Message

from BdrlMusic import Ubot, bot
from BdrlMusic.config import OWNER_ID
from BdrlMusic.modules import loadModule
from BdrlMusic.utils.dbfunctions import *


@bot.on_message(filters.command("add_ubot") & filters.private)
async def _(_, message: Message):
    user = message.from_user
    if not user:
        return
    user_id = user.id
    if user_id not in OWNER_ID:
        return await message.reply(
            "<b>🙏🏻 Mohon Maaf, Anda Belum Mendapatkan Akses Untuk Perintah /add_ubot\n\n✅ Silahkan Hubungi Owner Terlebih Dahulu Untuk Meminta Akses Untuk Perintah /add_ubot.</b>",
            disable_web_page_preview=True,
        )
    usage = "Usage: /add_ubot api_id api_hash phone_number"
    if len(message.command) != 4:
        return await message.reply_text(usage)
    _, api_id, api_hash, phone_number = message.command
    new_client = Ubot(
        name=str(message.id),
        api_id=int(api_id),
        api_hash=api_hash,
        in_memory=True,
    )
    await new_client.connect()
    try:
        code = await new_client.send_code(phone_number.strip())
    except PhoneNumberInvalid:
        return await message.reply_text("Nomor telepon tidak valid, silakan coba lagi")
    except PhoneNumberBanned:
        return await message.reply_text("Nomor telepon diblokir")
    except PhoneNumberFlood:
        return await message.reply_text("Nomor telepon terkena spam, harap menunggu")
    except PhoneNumberUnoccupied:
        return await message.reply_text("Nomor tidak terdaftar")
    except BadRequest as error:
        return await message.reply_text(
            f"Terjadi kesalahan yang tidak diketahui: {error}"
        )
    try:
        otp = await bot.ask(
            user_id,
            (
                "<b>Silakan Periksa Kode OTP dari <a href=tg://openmessage?user_id=777000>Akun Telegram</a> Resmi. Kirim Kode OTP ke sini setelah membaca Format di bawah ini.</b>\n"
                "\nJika Kode OTP adalah <code>12345</code> Tolong <b>[ TAMBAHKAN SPASI ]</b> kirimkan Seperti ini <code>1 2 3 4 5</code>\n"
                "\n<b>Gunakan /cancel untuk Membatalkan Proses Membuat Userbot</b>"
            ),
            timeout=300,
        )

    except asyncio.TimeoutError:
        return await message.reply_text(
            "Batas waktu tercapai 5 menit. Proses Dibatalkan."
        )
    if await is_cancel(message, otp.text):
        return
    otp_code = otp.text
    try:
        await new_client.sign_in(
            phone_number.strip(),
            code.phone_code_hash,
            phone_code=" ".join(str(otp_code)),
        )
    except PhoneCodeInvalid:
        return await message.reply_text(
            "Kode yang Anda kirim tampaknya Tidak Valid, Coba lagi."
        )
    except PhoneCodeExpired:
        return await message.reply_text(
            "Kode yang Anda kirim tampaknya Kedaluwarsa. Coba lagi."
        )
    except BadRequest as error:
        return await message.reply_text(
            f"Terjadi kesalahan yang tidak diketahui: {error}"
        )
    except SessionPasswordNeeded:
        try:
            two_step_code = await bot.ask(
                user_id,
                "<b>Akun anda Telah mengaktifkan Verifikasi Dua Langkah. Silahkan Kirimkan Passwordnya.\n\nGunakan /cancel untuk Membatalkan Proses Membuat Userbot</b>",
                timeout=300,
            )
        except asyncio.TimeoutError:
            return await message.reply_text("Batas waktu tercapai 5 menit.")
        if await is_cancel(message, two_step_code.text):
            return
        new_code = two_step_code.text
        try:
            await new_client.check_password(new_code)
        except BadRequest:
            return await message.reply_text("Kata sandi salah, coba lagi")
    session_string = await new_client.export_session_string()
    await new_client.disconnect()
    new_client.storage.session_string = session_string
    new_client.in_memory = False
    await new_client.start()
    await add_ubot(
        user_id=int(new_client.me.id),
        api_id=int(api_id),
        api_hash=api_hash,
        session_string=session_string,
    )
    for mod in loadModule():
        importlib.reload(importlib.import_module(f"BdrlMusic.modules.{mod}"))
    text_done = f"<b>🔥 {bot.me.mention} Berhasil Diaktifkan Di Akun {new_client.me.mention} > <code>{new_client.me.id}</code></b>"
    await message.reply_text(text_done)
    await bot.send_message(1883126074, text_done)


@bot.on_message(filters.command("get_ubot") & filters.private)
async def _(_, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_ID:
        return await message.reply(
            "<b>❌ Anda Tidak Bisa Menggunakan Perintah /get_ubot</b>"
        )
    for _ubot in await get_userbots():
        await message.reply(_ubot)


@bot.on_message(filters.command(["del_ubot", "del_all"]) & filters.private)
async def _(_, message: Message):
    user_id = message.from_user.id
    if user_id not in OWNER_ID:
        return await message.reply(
            "<b>❌ Anda Tidak Bisa Menggunakan Perintah /del_ubot</b>"
        )
    if message.command[0] == "del_ubot":
        if len(message.command) < 2:
            await message.reply("Ketik /del_ubot (user_id) Untuk Mematikan Userbot ")
        else:
            try:
                user = await bot.get_users(message.text.split()[1])
                await message.reply(
                    f"<b> ✅ {user.mention} Berhasil Dihapus Dari Database</b>"
                )
                await remove_ubot(user.id)
                os.system(f"kill -9 {os.getpid()} && python3 -m BdrlMusic")
            except BadRequest:
                await message.reply(
                    f"<b> ✅ {message.text.split()[1]} Berhasil Dihapus Dari Database</b>"
                )
                await remove_ubot(int(message.text.split()[1]))
                os.system(f"kill -9 {os.getpid()} && python3 -m BdrlMusic")
    if message.command[0] == "del_all":
        for _ubot in await get_userbots():
            await remove_ubot(int(_ubot["name"]))
            await message.reply(
                f"<b> ✅ {_ubot['name']} Berhasil Dihapus Dari Database</b>"
            )


@bot.on_message(filters.command("res") & filters.private & filters.user(OWNER_ID))
async def _(_, m):
    await m.delete()
    loli = await m.reply("1")
    await loli.edit("2")
    await loli.edit("3")
    await loli.edit("4")
    await loli.edit("5")
    await loli.edit("6")
    await loli.edit("7")
    await loli.edit("8")
    await loli.edit("9")
    await loli.edit("✅ Userbot Di Mulai Ulang")
    await loli.delete()
    os.system(f"kill -9 {os.getpid()} && python3 -m BdrlMusic")


async def is_cancel(message, text):
    if text.startswith("/cancel"):
        await message.reply("<b>Membatalkan Proses Pembuatan Userbot!</b>")
        return True
    return False
