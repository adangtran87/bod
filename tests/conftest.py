import aiosqlite
import pytest


@pytest.mark.asyncio
@pytest.fixture
async def test_db() -> aiosqlite.Connection:
    return aiosqlite.connect("file::memory:")
