"""
API endpoints for Shipment resources.

Provides full CRUD access to the shipments table:
    POST   /            – Create a new shipment
    GET    /            – List all shipments (with pagination)
    GET    /{id}        – Retrieve a single shipment
    PUT    /{id}        – Update an existing shipment
    DELETE /{id}        – Remove a shipment
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.shipment import ShipmentCreate, ShipmentResponse, ShipmentUpdate
from app.services.shipment import (
    create_shipment,
    delete_shipment,
    get_shipment_by_id,
    get_shipments,
    update_shipment,
)

logger = logging.getLogger(__name__)

router = APIRouter()


# ---------------------------------------------------------------------------
# POST /shipments
# ---------------------------------------------------------------------------
@router.post(
    "/",
    response_model=ShipmentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new shipment",
    description="Validates the request body and creates a new shipment record. "
                "Returns 409 if the `shipment_id` already exists.",
)
def create_shipment_endpoint(
    payload: ShipmentCreate,
    db: Session = Depends(get_db),
) -> ShipmentResponse:
    """
    Create a new shipment record.

    Args:
        payload: Validated shipment creation data.
        db: SQLAlchemy database session (injected).

    Returns:
        The created shipment with all database-generated fields.

    Raises:
        HTTPException 409: If a shipment with the same shipment_id exists.
    """
    try:
        return create_shipment(db=db, payload=payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A shipment with shipment_id '{payload.shipment_id}' already exists.",
        )


# ---------------------------------------------------------------------------
# GET /shipments
# ---------------------------------------------------------------------------
@router.get(
    "/",
    response_model=list[ShipmentResponse],
    status_code=status.HTTP_200_OK,
    summary="List all shipments",
    description="Returns a paginated list of shipment records. "
                "Use `skip` and `limit` query parameters for pagination.",
)
def list_shipments_endpoint(
    skip: int = Query(default=0, ge=0, description="Records to skip"),
    limit: int = Query(default=100, ge=1, le=500, description="Max records to return"),
    db: Session = Depends(get_db),
) -> list[ShipmentResponse]:
    """
    Retrieve all shipment records with optional pagination.

    Args:
        skip: Number of records to skip (default 0).
        limit: Maximum number of records to return (default 100, max 500).
        db: SQLAlchemy database session (injected).

    Returns:
        A list of ShipmentResponse objects (may be empty).
    """
    return get_shipments(db=db, skip=skip, limit=limit)


# ---------------------------------------------------------------------------
# GET /shipments/{id}
# ---------------------------------------------------------------------------
@router.get(
    "/{shipment_id}",
    response_model=ShipmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a shipment by ID",
    description="Returns a single shipment record identified by its database ID. "
                "Returns 404 if the shipment does not exist.",
)
def get_shipment_endpoint(
    shipment_id: int,
    db: Session = Depends(get_db),
) -> ShipmentResponse:
    """
    Retrieve a single shipment by its primary key.

    Args:
        shipment_id: Database primary key of the shipment.
        db: SQLAlchemy database session (injected).

    Returns:
        The matching ShipmentResponse.

    Raises:
        HTTPException 404: If no shipment with the given ID exists.
    """
    db_shipment = get_shipment_by_id(db=db, shipment_id=shipment_id)
    if db_shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {shipment_id} not found.",
        )
    return db_shipment


# ---------------------------------------------------------------------------
# PUT /shipments/{id}
# ---------------------------------------------------------------------------
@router.put(
    "/{shipment_id}",
    response_model=ShipmentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a shipment",
    description="Applies partial updates to an existing shipment. "
                "Only fields included in the request body are modified. "
                "Returns 404 if the shipment does not exist, "
                "or 409 if the updated `shipment_id` conflicts with another record.",
)
def update_shipment_endpoint(
    shipment_id: int,
    payload: ShipmentUpdate,
    db: Session = Depends(get_db),
) -> ShipmentResponse:
    """
    Update an existing shipment record.

    Args:
        shipment_id: Database primary key of the shipment to update.
        payload: Validated update data (all fields optional).
        db: SQLAlchemy database session (injected).

    Returns:
        The updated ShipmentResponse.

    Raises:
        HTTPException 404: If no shipment with the given ID exists.
        HTTPException 409: If the updated shipment_id already exists.
    """
    db_shipment = get_shipment_by_id(db=db, shipment_id=shipment_id)
    if db_shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {shipment_id} not found.",
        )
    try:
        return update_shipment(db=db, db_shipment=db_shipment, payload=payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A shipment with shipment_id '{payload.shipment_id}' already exists.",
        )


# ---------------------------------------------------------------------------
# DELETE /shipments/{id}
# ---------------------------------------------------------------------------
@router.delete(
    "/{shipment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a shipment",
    description="Permanently removes a shipment record. "
                "Returns 404 if the shipment does not exist.",
)
def delete_shipment_endpoint(
    shipment_id: int,
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a shipment record by its primary key.

    Args:
        shipment_id: Database primary key of the shipment to delete.
        db: SQLAlchemy database session (injected).

    Raises:
        HTTPException 404: If no shipment with the given ID exists.
    """
    db_shipment = get_shipment_by_id(db=db, shipment_id=shipment_id)
    if db_shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with id {shipment_id} not found.",
        )
    delete_shipment(db=db, db_shipment=db_shipment)
