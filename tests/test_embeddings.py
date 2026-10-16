from app.core.config import settings
from app.services import embeddings


async def test_embed_texts_returns_one_vector_per_text() -> None:
    vectors = await embeddings.embed_texts(["a", "b"])
    assert len(vectors) == 2
    assert all(len(v) == settings.embedding_dimensions for v in vectors)
    assert vectors[0][0] == 0.0  # the fake returns zeros; a real model never would
