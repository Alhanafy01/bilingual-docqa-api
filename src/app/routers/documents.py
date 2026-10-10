from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.document import Document
from app.schemas.documents import DocumentCreate, DocumentRead

router = APIRouter(prefix="/documents", tags=["documents"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("", status_code=201)
async def create_document(
    payload: DocumentCreate,
    session: SessionDep,
) -> DocumentRead:
    document = Document(**payload.model_dump())
    session.add(document)
    await session.commit()
    await session.refresh(document)
    return DocumentRead.model_validate(document)


@router.get("")
async def list_documents(
    session: SessionDep,
    limit: int = 10,
) -> list[DocumentRead]:
    result = await session.execute(select(Document).limit(limit))
    return [DocumentRead.model_validate(d) for d in result.scalars().all()]


@router.get("/{document_id}")
async def get_document(
    document_id: int,
    session: SessionDep,
) -> DocumentRead:
    document = await session.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return DocumentRead.model_validate(document)


@router.delete("/{document_id}", status_code=204)
async def delete_document(
    document_id: int,
    session: SessionDep,
) -> None:
    document = await session.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    await session.delete(document)
    await session.commit()
