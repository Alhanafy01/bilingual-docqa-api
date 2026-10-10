from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Language = Literal["en", "ar"]


class DocumentCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(min_length=1, max_length=100)
    language: Language
    content: str = Field(min_length=1)


class DocumentRead(DocumentCreate):
    id: int
