from collections.abc import AsyncIterator, Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.db.session import get_session
from app.main import app

test_engine = create_async_engine(settings.test_database_url, poolclass=NullPool)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


async def get_test_session() -> AsyncIterator[AsyncSession]:
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = get_test_session


@pytest.fixture(autouse=True)
async def clean_tables() -> AsyncIterator[None]:
    async with test_engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE chunks, documents RESTART IDENTITY"))
    yield


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as c:
        yield c


async def fake_embed_texts(texts: list[str]) -> list[list[float]]:
    return [[0.0] * settings.embedding_dimensions for _ in texts]


@pytest.fixture(autouse=True)
def no_real_embedings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.services.embeddings.embed_texts", fake_embed_texts)
