from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import TEXT, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunk"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    content: Mapped[str] = mapped_column(TEXT)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB)
    embedding: Mapped[list[float]] = mapped_column(Vector(384))  # dim of sentence-transformers/all-MiniLM-L6-v2
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
