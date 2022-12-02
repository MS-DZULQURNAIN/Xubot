import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")
MONGO_URL = os.getenv("MONGO_URL")
OWNER_ID = list(map(int, os.getenv("OWNER_ID", "id_1 id_2 dan_seterusnya").split()))
SUDO_USERS = list(map(int, os.getenv("SUDO_USERS", "").split()))
PREFIXES = [
    "°",
    "`",
    "|",
    "•",
    "√",
    "¶",
    "∆",
]
