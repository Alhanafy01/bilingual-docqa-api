from app.services.chunking import split_text


def test_short_text_is_one_chunk() -> None:
    assert split_text("Hello world.") == ["Hello world."]


def test_paragraphs_pack_until_full() -> None:
    a, b, c = "a" * 500, "b" * 500, "c" * 500
    chunks = split_text(f"{a}\n\n{b}\n\n{c}", max_chars=1200)
    assert chunks == [f"{a}\n\n{b}", c]


def test_empty_text_gives_no_chunks() -> None:
    assert split_text("") == []
