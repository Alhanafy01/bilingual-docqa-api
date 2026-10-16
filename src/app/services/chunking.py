def split_text(text: str, max_chars: int = 1200) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""
    for p in paragraphs:
        if not current:
            current = p
        elif len(current) + 2 + len(p) <= max_chars:
            current = current + "\n\n" + p
        else:
            chunks.append(current)
            current = p
    if current:
        chunks.append(current)
    return chunks
