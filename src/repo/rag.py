from typing import Annotated

from fastapi import Depends
from sqlalchemy import insert, select

from core.db.manager import SessionDep
from core.db.models import DocumentChunk


class RagRepo:
    def __init__(self, session: SessionDep):
        self.session = session

    async def add_documents(
        self,
        texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, object]],
    ) -> None:
        stmt = insert(DocumentChunk).values(
            [
                {
                    "content": text,
                    "metadata_": metadata,
                    "embedding": embedding,
                }
                for text, metadata, embedding in zip(texts, metadatas, embeddings, strict=True)
            ]
        )
        await self.session.execute(stmt)

    async def similar_documents(
        self,
        embedding: list[float],
        limit: int = 3,
    ) -> list[DocumentChunk]:
        # fmt: off
        stmt = (
            select(DocumentChunk)
            .order_by(DocumentChunk.embedding.cosine_distance(embedding))
            .limit(limit)
        )
        # fmt: on
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


RagRepoDep = Annotated[RagRepo, Depends()]
