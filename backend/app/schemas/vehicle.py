import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.common import PaginatedResponse


class VehicleCreate(BaseModel):
    """Schema for creating a new vehicle."""

    vin: str | None = Field(None, max_length=17)
    stock_number: str | None = None
    year: int | None = Field(None, ge=1900, le=2100)
    make: str | None = None
    model: str | None = None
    trim: str | None = None
    body_style: str | None = None
    engine_type: str | None = None
    engine_cylinders: int | None = None
    displacement_l: float | None = None
    horsepower: int | None = None
    torque: int | None = None
    drive_type: str | None = None
    transmission: str | None = None
    fuel_type: str | None = None
    exterior_color: str | None = None
    interior_color: str | None = None
    mileage: int | None = Field(None, ge=0)
    price: Decimal | None = Field(None, ge=0)
    msrp: Decimal | None = Field(None, ge=0)
    condition: str | None = None
    accident_count: int = 0
    owner_count: int = 0
    title_status: str | None = None
    has_recalls: bool = False
    factory_options: list[str] = []
    packages: list[str] = []
    safety_features: list[str] = []
    nhtsa_raw: dict | None = None
    status: str = "active"
    notes: str | None = None

    model_config = {"from_attributes": True}


class VehicleUpdate(BaseModel):
    """Schema for partially updating a vehicle. All fields are optional."""

    vin: str | None = Field(None, max_length=17)
    stock_number: str | None = None
    year: int | None = Field(None, ge=1900, le=2100)
    make: str | None = None
    model: str | None = None
    trim: str | None = None
    body_style: str | None = None
    engine_type: str | None = None
    engine_cylinders: int | None = None
    displacement_l: float | None = None
    horsepower: int | None = None
    torque: int | None = None
    drive_type: str | None = None
    transmission: str | None = None
    fuel_type: str | None = None
    exterior_color: str | None = None
    interior_color: str | None = None
    mileage: int | None = Field(None, ge=0)
    price: Decimal | None = Field(None, ge=0)
    msrp: Decimal | None = Field(None, ge=0)
    condition: str | None = None
    accident_count: int | None = None
    owner_count: int | None = None
    title_status: str | None = None
    has_recalls: bool | None = None
    factory_options: list[str] | None = None
    packages: list[str] | None = None
    safety_features: list[str] | None = None
    nhtsa_raw: dict | None = None
    status: str | None = None
    notes: str | None = None

    model_config = {"from_attributes": True}


class VehicleResponse(BaseModel):
    """Full vehicle response schema."""

    id: uuid.UUID
    tenant_id: uuid.UUID
    vin: str | None = None
    stock_number: str | None = None
    year: int | None = None
    make: str | None = None
    model: str | None = None
    trim: str | None = None
    body_style: str | None = None
    engine_type: str | None = None
    engine_cylinders: int | None = None
    displacement_l: float | None = None
    horsepower: int | None = None
    torque: int | None = None
    drive_type: str | None = None
    transmission: str | None = None
    fuel_type: str | None = None
    exterior_color: str | None = None
    interior_color: str | None = None
    mileage: int | None = None
    price: Decimal | None = None
    msrp: Decimal | None = None
    condition: str | None = None
    accident_count: int = 0
    owner_count: int = 0
    title_status: str | None = None
    has_recalls: bool = False
    factory_options: list = []
    packages: list = []
    safety_features: list = []
    nhtsa_raw: dict | None = None
    status: str = "active"
    notes: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class VehicleListResponse(PaginatedResponse[VehicleResponse]):
    """Paginated list of vehicles."""

    pass


class VinDecodeRequest(BaseModel):
    """Request to decode a VIN number."""

    vin: str = Field(..., min_length=17, max_length=17, description="17-character VIN")


class VinDecodeResponse(BaseModel):
    """Response from VIN decoding."""

    vin: str
    year: int | None = None
    make: str | None = None
    model: str | None = None
    trim: str | None = None
    body_style: str | None = None
    engine_type: str | None = None
    engine_cylinders: int | None = None
    displacement_l: float | None = None
    horsepower: int | None = None
    torque: int | None = None
    drive_type: str | None = None
    transmission: str | None = None
    fuel_type: str | None = None
    raw_data: dict | None = None
