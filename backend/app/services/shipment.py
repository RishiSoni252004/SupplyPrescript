"""
Service layer for Shipment CRUD operations.

Encapsulates all database interactions so that API endpoint handlers
remain thin and focused on HTTP concerns (request parsing, response
formatting, status codes).

All functions accept a SQLAlchemy `Session` and return ORM model
instances or `None`.
"""

import logging
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.shipment import Shipment
from app.schemas.shipment import ShipmentCreate, ShipmentUpdate

logger = logging.getLogger(__name__)


def create_shipment(db: Session, payload: ShipmentCreate) -> Shipment:
    """
    Persist a new Shipment record.

    Args:
        db: Active database session.
        payload: Validated shipment creation data.

    Returns:
        The newly created Shipment ORM instance (with id populated).

    Raises:
        IntegrityError: If the shipment_id already exists.
    """
    db_shipment = Shipment(**payload.model_dump())
    db.add(db_shipment)
    try:
        db.commit()
        db.refresh(db_shipment)
        logger.info("Created shipment id=%s shipment_id='%s'", db_shipment.id, db_shipment.shipment_id)
    except IntegrityError:
        db.rollback()
        logger.warning("Duplicate shipment_id='%s'", payload.shipment_id)
        raise
    return db_shipment


def get_shipments(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Shipment]:
    """
    Retrieve a paginated list of Shipment records.

    Args:
        db: Active database session.
        skip: Number of records to skip (for pagination).
        limit: Maximum number of records to return.

    Returns:
        List of Shipment ORM instances (may be empty).
    """
    return (
        db.query(Shipment)
        .order_by(Shipment.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_shipment_by_id(db: Session, shipment_id: int) -> Optional[Shipment]:
    """
    Retrieve a single Shipment by its primary key.

    Args:
        db: Active database session.
        shipment_id: Database primary key (`id` column).

    Returns:
        The matching Shipment ORM instance, or ``None`` if not found.
    """
    return db.query(Shipment).filter(Shipment.id == shipment_id).first()


def update_shipment(
    db: Session,
    db_shipment: Shipment,
    payload: ShipmentUpdate,
) -> Shipment:
    """
    Apply partial updates to an existing Shipment record.

    Only fields explicitly provided in the payload (i.e., not ``None``)
    are updated.  The ``updated_at`` timestamp is refreshed automatically
    by the ORM column default.

    Args:
        db: Active database session.
        db_shipment: The existing Shipment ORM instance to update.
        payload: Validated update data (all fields optional).

    Returns:
        The updated Shipment ORM instance.

    Raises:
        IntegrityError: If the updated shipment_id conflicts with another record.
    """
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_shipment, field, value)
    try:
        db.commit()
        db.refresh(db_shipment)
        logger.info("Updated shipment id=%s", db_shipment.id)
    except IntegrityError:
        db.rollback()
        logger.warning(
            "Integrity error while updating shipment id=%s", db_shipment.id,
        )
        raise
    return db_shipment


def delete_shipment(db: Session, db_shipment: Shipment) -> None:
    """
    Permanently remove a Shipment record from the database.

    Args:
        db: Active database session.
        db_shipment: The Shipment ORM instance to delete.
    """
    shipment_id = db_shipment.id
    db.delete(db_shipment)
    db.commit()
    logger.info("Deleted shipment id=%s", shipment_id)
