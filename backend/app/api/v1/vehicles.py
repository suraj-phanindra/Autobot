import uuid
from math import ceil

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth import get_current_tenant_id, get_current_user
from app.core.exceptions import NotFoundError
from app.db.session import get_db
from app.models.vehicle import Vehicle
from app.schemas.auth import CurrentUser
from app.schemas.vehicle import (
    VehicleCreate,
    VehicleListResponse,
    VehicleResponse,
    VehicleUpdate,
    VinDecodeRequest,
    VinDecodeResponse,
)

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.get("/", response_model=VehicleListResponse)
async def list_vehicles(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    make: str | None = Query(None, description="Filter by make"),
    model: str | None = Query(None, description="Filter by model"),
    year: int | None = Query(None, description="Filter by year"),
    status: str = Query("active", description="Filter by status"),
    tenant_id: uuid.UUID = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db),
) -> VehicleListResponse:
    """List vehicles for the current tenant with optional filtering and pagination."""
    base_query = select(Vehicle).where(
        Vehicle.tenant_id == tenant_id,
        Vehicle.status == status,
    )

    if make:
        base_query = base_query.where(Vehicle.make.ilike(f"%{make}%"))
    if model:
        base_query = base_query.where(Vehicle.model.ilike(f"%{model}%"))
    if year:
        base_query = base_query.where(Vehicle.year == year)

    # Count total
    count_query = select(func.count()).select_from(base_query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar_one()

    # Fetch page
    offset = (page - 1) * page_size
    items_query = (
        base_query.order_by(Vehicle.created_at.desc()).offset(offset).limit(page_size)
    )
    result = await db.execute(items_query)
    vehicles = result.scalars().all()

    return VehicleListResponse(
        items=[VehicleResponse.model_validate(v) for v in vehicles],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=ceil(total / page_size) if total > 0 else 0,
    )


@router.post("/", response_model=VehicleResponse, status_code=201)
async def create_vehicle(
    vehicle_in: VehicleCreate,
    tenant_id: uuid.UUID = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db),
) -> VehicleResponse:
    """Create a new vehicle record."""
    vehicle = Vehicle(
        tenant_id=tenant_id,
        **vehicle_in.model_dump(),
    )
    db.add(vehicle)
    await db.flush()
    await db.refresh(vehicle)
    return VehicleResponse.model_validate(vehicle)


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: uuid.UUID,
    tenant_id: uuid.UUID = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db),
) -> VehicleResponse:
    """Get a single vehicle by ID."""
    result = await db.execute(
        select(Vehicle).where(
            Vehicle.id == vehicle_id,
            Vehicle.tenant_id == tenant_id,
        )
    )
    vehicle = result.scalar_one_or_none()
    if vehicle is None:
        raise NotFoundError(f"Vehicle {vehicle_id} not found.")
    return VehicleResponse.model_validate(vehicle)


@router.patch("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: uuid.UUID,
    vehicle_in: VehicleUpdate,
    tenant_id: uuid.UUID = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db),
) -> VehicleResponse:
    """Partially update a vehicle."""
    result = await db.execute(
        select(Vehicle).where(
            Vehicle.id == vehicle_id,
            Vehicle.tenant_id == tenant_id,
        )
    )
    vehicle = result.scalar_one_or_none()
    if vehicle is None:
        raise NotFoundError(f"Vehicle {vehicle_id} not found.")

    update_data = vehicle_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(vehicle, field, value)

    await db.flush()
    await db.refresh(vehicle)
    return VehicleResponse.model_validate(vehicle)


@router.delete("/{vehicle_id}", status_code=204)
async def delete_vehicle(
    vehicle_id: uuid.UUID,
    tenant_id: uuid.UUID = Depends(get_current_tenant_id),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Soft-delete a vehicle by setting its status to 'archived'."""
    result = await db.execute(
        select(Vehicle).where(
            Vehicle.id == vehicle_id,
            Vehicle.tenant_id == tenant_id,
        )
    )
    vehicle = result.scalar_one_or_none()
    if vehicle is None:
        raise NotFoundError(f"Vehicle {vehicle_id} not found.")

    vehicle.status = "archived"
    await db.flush()


@router.post("/decode-vin", response_model=VinDecodeResponse)
async def decode_vin(
    request: VinDecodeRequest,
    current_user: CurrentUser = Depends(get_current_user),
) -> VinDecodeResponse:
    """Decode a VIN number to extract vehicle information.

    This is a placeholder that will be connected to the NHTSA vPIC API
    and enriched with additional data sources.
    """
    return VinDecodeResponse(
        vin=request.vin,
        year=None,
        make=None,
        model=None,
        trim=None,
        body_style=None,
        engine_type=None,
        engine_cylinders=None,
        displacement_l=None,
        horsepower=None,
        torque=None,
        drive_type=None,
        transmission=None,
        fuel_type=None,
        raw_data={"message": "VIN decode not yet implemented. Will connect to NHTSA vPIC API."},
    )
