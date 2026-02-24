import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    primary_color: Mapped[str | None] = mapped_column(String(7), nullable=True)
    plan: Mapped[str] = mapped_column(String(50), nullable=False, server_default="free")
    settings: Mapped[dict] = mapped_column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    users: Mapped[list["User"]] = relationship("User", back_populates="tenant")  # noqa: F821
    vehicles: Mapped[list["Vehicle"]] = relationship("Vehicle", back_populates="tenant")  # noqa: F821
    documents: Mapped[list["Document"]] = relationship("Document", back_populates="tenant")  # noqa: F821
    document_chunks: Mapped[list["DocumentChunk"]] = relationship("DocumentChunk", back_populates="tenant")  # noqa: F821
    search_logs: Mapped[list["SearchLog"]] = relationship("SearchLog", back_populates="tenant")  # noqa: F821
    api_keys: Mapped[list["ApiKey"]] = relationship("ApiKey", back_populates="tenant")  # noqa: F821
    conversations: Mapped[list["Conversation"]] = relationship("Conversation", back_populates="tenant")  # noqa: F821
