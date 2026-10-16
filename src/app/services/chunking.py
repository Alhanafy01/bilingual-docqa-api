import re

_SENTENCED_END = re.compile(r"(?<=[.!?؟])\s+")


def _split_sentences(paragraph: str) -> list[str]:
    return [s for s in _SENTENCED_END.split(paragraph) if s]


def _pieces(paragraphs: list[str], max_chars: int) -> list[str]:
    pieces: list[str] = []
    for p in paragraphs:
        if len(p) <= max_chars:
            pieces.append(p)
            continue
        for s in _split_sentences(p):
            if len(s) <= max_chars:
                pieces.append(s)
            else:
                pieces.extend(s[i : i + max_chars] for i in range(0, len(s), max_chars))
    return pieces


def split_text(text: str, max_chars: int = 1200, overlap: int = 150) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""
    for p in _pieces(paragraphs, max_chars):
        if not current:
            current = p
        elif len(current) + 2 + len(p) <= max_chars:
            current = current + "\n\n" + p
        else:
            chunks.append(current)
            current = p
    if current:
        chunks.append(current)
    if overlap and len(chunks) > 1:
        chunks = [chunks[0]] + [
            chunks[i - 1][-overlap:] + "\n\n" + chunks[i] for i in range(1, len(chunks))
        ]
    return chunks
