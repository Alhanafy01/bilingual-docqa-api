from fastapi import APIRouter, HTTPException

from app.schemas.documents import DocumentCreate, DocumentRead

router = APIRouter(prefix="/documents", tags=["documents"])

_documents: dict[int, DocumentRead] = {}
_next_id: int = 1


@router.post("", status_code=201)
async def create_document(payload: DocumentCreate) -> DocumentRead:
    global _next_id
    document = DocumentRead(id=_next_id, **payload.model_dump())
    _documents[_next_id] = document
    _next_id += 1
    return document


@router.get("")
async def list_documents(limit: int = 100) -> list[DocumentRead]:
    return list(_documents.values())[:limit]


@router.get("/{document_id}")
async def get_document(document_id: int) -> DocumentRead:
    document = _documents.get(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{document_id}", status_code=204)
async def delete_document(document_id: int) -> None:
    if document_id not in _documents:
        raise HTTPException(status_code=404, detail="Document not found")
    del _documents[document_id]
