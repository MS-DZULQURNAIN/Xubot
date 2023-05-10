from logging import *
from typing import Callable

from pyrogram import Client
from pyrogram.enums import ParseMode
from pyrogram.handlers import MessageHandler
from pyromod import listen
from pytgcalls import PyTgCalls
from rich.logging import RichHandler

from .config import *

basicConfig(
    level=INFO,
    format="%(filename)s:%(lineno)s %(levelname)s: %(message)s",
    datefmt="%m-%d %H:%M",
    handlers=[RichHandler()],
)
console = StreamHandler()
console.setLevel(ERROR)
console.setFormatter(Formatter("%(filename)s:%(lineno)s %(levelname)s: %(message)s"))
getLogger("").addHandler(console)
bot = Client(
    name="BdrlMusicubot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode=ParseMode.HTML,
)


class Ubot(Client):
    __module__ = "pyrogram.client"
    _ubot = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs, parse_mode=ParseMode.HTML)
        self.call_py = PyTgCalls(self)

    def on_message(self, filters=None, group=0):
        def decorator(func: Callable) -> Callable:
            for ub in self._ubot:
                ub.add_handler(MessageHandler(func, filters), group)
            return func

        return decorator

    def pytgcalls_decorator(self):
        def decorator(func):
            for ub in self._ubot:
                if func.__name__ != "stream_end":
                    ub.call_py.on_kicked()(func)
                    ub.call_py.on_closed_voice_chat()(func)
                    ub.call_py.on_left()(func)
                else:
                    ub.call_py.on_stream_end()(func)
            return func

        return decorator

    async def start(self):
        await super().start()
        await self.call_py.start()
        if self not in self._ubot:
            self._ubot.append(self)


ubot = Ubot(
    name="ubot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
)
