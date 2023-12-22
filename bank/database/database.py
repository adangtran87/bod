import aiosqlite


async def get_db() -> aiosqlite.Connection:
    return aiosqlite.connect("database.db")
