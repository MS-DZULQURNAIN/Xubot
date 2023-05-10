from motor.motor_asyncio import AsyncIOMotorClient

from BdrlMusic.config import MONGO_URL

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongodb = mongo_client.ubotmusik
ubotdb = mongodb.ubot


async def add_ubot(user_id, api_id, api_hash, session_string):
    return await ubotdb.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "api_id": api_id,
                "api_hash": api_hash,
                "session_string": session_string,
            }
        },
        upsert=True,
    )


async def remove_ubot(user_id: int):
    return await ubotdb.delete_one({"user_id": user_id})


async def get_userbots() -> list:
    data = []
    async for ubot in ubotdb.find({"user_id": {"$exists": 1}}):
        data.append(
            dict(
                name=str(ubot["user_id"]),
                api_id=ubot["api_id"],
                api_hash=ubot["api_hash"],
                session_string=ubot["session_string"],
            )
        )
    return data
