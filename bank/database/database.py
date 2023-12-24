import aiosqlite


async def get_db() -> aiosqlite.Connection:
    return aiosqlite.connect("database.db")


# TODO: Update get_db to use this pattern instead
async def rest_db():
    """Return a database connection for use as a dependency.
    This connection has the Row row factory automatically attached."""

    db = await aiosqlite.connect("database.db")
    # Provide a smarter version of the results. This keeps from having to unpack
    # tuples manually.
    db.row_factory = aiosqlite.Row

    try:
        yield db
    finally:
        await db.close()
