from importlib import import_module
from logging import getLogger

from BdrlMusic.modules import loadModule

getLogger(__name__)


async def loadPlugins():
    modules = loadModule()
    for mod in modules:
        import_module(f"BdrlMusic.modules.{mod}")
    print("Bdrl Music (userbot) telah diaktifkan")
