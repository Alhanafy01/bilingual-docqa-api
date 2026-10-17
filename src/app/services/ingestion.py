from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chunk import Chunk
from app.models.document import Document
from app.services import embeddings
from app.services.chunking import split_text


async def ingest_document(document: Document, session: AsyncSession) -> int:
    chunks = split_text(document.content)
    if not chunks:
        return 0
    vectors = await embeddings.embed_texts(chunks)
    for i, (text, vec) in enumerate(zip(chunks, vectors, strict=True)):
        session.add(
            Chunk(document_id=document.id, chunk_index=i, content=text, embedding=vec)
        )

    await session.commit()
    return len(chunks)
