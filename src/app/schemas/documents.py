from typing import Literal

from pydantic import BaseModel, Field

Language = Literal["en", "ar"]


class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    language: Language
    content: str = Field(min_length=1)


class DocumentRead(DocumentCreate):
    id: int
