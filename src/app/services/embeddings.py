from openai import AsyncOpenAI

from app.core.config import settings

client = AsyncOpenAI(
    base_url=settings.embedding_base_url,
    api_key=settings.embedding_api_key,
    timeout=30,
)


async def embed_texts(texts: list[str]) -> list[list[float]]:
    resp = await client.embeddings.create(model=settings.embedding_model, input=texts)
    expected = settings.embedding_dimensions

    vectors = [d.embedding for d in sorted(resp.data, key=lambda d: d.index)]
    for v in vectors:
        if len(v) != settings.embedding_dimensions:
            raise ValueError(f"embedding has {len(v)} dimensions,expected {expected}")
    return vectors
