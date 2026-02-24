import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False
    )

    # Identification
    vin: Mapped[str | None] = mapped_column(String(17), nullable=True)
    stock_number: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Basic info
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    make: Mapped[str | None] = mapped_column(String(100), nullable=True)
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    trim: Mapped[str | None] = mapped_column(String(100), nullable=True)
    body_style: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Engine / Powertrain
    engine_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    engine_cylinders: Mapped[int | None] = mapped_column(Integer, nullable=True)
    displacement_l: Mapped[float | None] = mapped_column(Float, nullable=True)
    horsepower: Mapped[int | None] = mapped_column(Integer, nullable=True)
    torque: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Drivetrain
    drive_type: Mapped[str | None] = mapped_column(String(20), nullable=True)
    transmission: Mapped[str | None] = mapped_column(String(50), nullable=True)
    fuel_type: Mapped[str | None] = mapped_column(String(30), nullable=True)

    # Appearance & condition
    exterior_color: Mapped[str | None] = mapped_column(String(50), nullable=True)
    interior_color: Mapped[str | None] = mapped_column(String(50), nullable=True)
    mileage: Mapped[int | None] = mapped_column(Integer, nullable=True)
    price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    msrp: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    condition: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # History
    accident_count: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    owner_count: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )
    title_status: Mapped[str | None] = mapped_column(String(30), nullable=True)
    has_recalls: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )

    # Features (JSONB arrays)
    factory_options: Mapped[list] = mapped_column(
        JSONB, nullable=False, server_default=text("'[]'::jsonb")
    )
    packages: Mapped[list] = mapped_column(
        JSONB, nullable=False, server_default=text("'[]'::jsonb")
    )
    safety_features: Mapped[list] = mapped_column(
        JSONB, nullable=False, server_default=text("'[]'::jsonb")
    )

    # Raw data
    nhtsa_raw: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Status
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default="active"
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Full-text search
    search_vector = mapped_column(TSVECTOR, nullable=True)

    # Timestamps
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
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="vehicles")  # noqa: F821
    documents: Mapped[list["Document"]] = relationship("Document", back_populates="vehicle")  # noqa: F821
    document_chunks: Mapped[list["DocumentChunk"]] = relationship("DocumentChunk", back_populates="vehicle")  # noqa: F821

    __table_args__ = (
        Index("ix_vehicles_tenant_id", "tenant_id"),
        Index("ix_vehicles_vin", "vin"),
        Index("ix_vehicles_tenant_status", "tenant_id", "status"),
        Index("ix_vehicles_search_vector", "search_vector", postgresql_using="gin"),
    )
