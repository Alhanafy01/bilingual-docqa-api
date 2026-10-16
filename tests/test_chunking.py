from app.services.chunking import split_text


def test_short_text_is_one_chunk() -> None:
    assert split_text("Hello world.") == ["Hello world."]


def test_paragraphs_pack_until_full() -> None:
    a, b, c = "a" * 500, "b" * 500, "c" * 500
    chunks = split_text(f"{a}\n\n{b}\n\n{c}", max_chars=1200, overlap=0)
    assert chunks == [f"{a}\n\n{b}", c]


def test_empty_text_gives_no_chunks() -> None:
    assert split_text("") == []


def test_long_paragraph_splits_into_sentences() -> None:
    s1, s2, s3 = "a" * 699 + ".", "b" * 699 + ".", "c" * 699 + "."
    assert split_text(f"{s1} {s2} {s3}", max_chars=1200, overlap=0) == [s1, s2, s3]


def test_oversized_sentence_is_hard_cut() -> None:
    chunks = split_text("x" * 2500, max_chars=1200, overlap=0)
    assert [len(c) for c in chunks] == [1200, 1200, 100]


def test_chunks_overlap_with_previous_tail() -> None:
    a, b = "a" * 500, "b" * 800
    chunks = split_text(f"{a}\n\n{b}", max_chars=1200, overlap=10)
    assert chunks[1].startswith(a[-10:] + "\n\n")
