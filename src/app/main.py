from fastapi import FastAPI

from app.core.config import settings
from app.routers import documents

app = FastAPI(title=settings.app_name, version="0.1.0", debug=settings.debug)
app.include_router(documents.router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}
