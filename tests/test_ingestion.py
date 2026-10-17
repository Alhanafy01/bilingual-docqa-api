from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chunk import Chunk
from app.models.document import Document
from app.services.ingestion import ingest_document


async def test_ingest_writes_one_chunk_per_piece(session: AsyncSession) -> None:
    doc = Document(title="t", language="en", content="a" * 500 + "\n\n" + "b" * 800)
    session.add(doc)
    await session.commit()
    await session.refresh(doc)

    written = await ingest_document(doc, session)

    assert written == 2
    count = await session.scalar(select(func.count()).select_from(Chunk))
    assert count == 2
