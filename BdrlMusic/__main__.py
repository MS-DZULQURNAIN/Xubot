from asyncio import get_event_loop_policy

from pyrogram.errors import RPCError
from pyrogram.methods.utilities.idle import idle

from BdrlMusic import Ubot, bot, ubot
from BdrlMusic.core.functions.plugins import loadPlugins
from BdrlMusic.utils.dbfunctions import get_userbots, remove_ubot


async def main():
    await bot.start()
    await ubot.start()
    for _ubot in await get_userbots():
        ubot_ = Ubot(**_ubot)
        try:
            await ubot_.start()
        except RPCError:
            await remove_ubot(int(_ubot["name"]))
            print(f"✅ {_ubot['name']} Berhasil Dihapus Dari Database")
    await loadPlugins()
    await idle()


if __name__ == "__main__":
    get_event_loop_policy().get_event_loop().run_until_complete(main())
