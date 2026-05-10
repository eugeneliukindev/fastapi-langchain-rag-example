from typing import Annotated

from fastapi import APIRouter, Depends, Query, UploadFile

from service.rag import RagService

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile, service: Annotated[RagService, Depends()]):
    await service.upload_pdf(file)


@router.get("/ask-pdf")
async def ask_pdf(q: Annotated[str, Query(min_length=1)], service: Annotated[RagService, Depends()]):
    return await service.ask_pdf(q)
