"""
API endpoints for Shipment resources.

Provides read access to the shipments table. Additional CRUD operations
will be added in later phases as business logic is implemented.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.shipment import Shipment
from app.schemas.shipment import ShipmentResponse

router = APIRouter()


@router.get(
    "/",
    response_model=list[ShipmentResponse],
    summary="List all shipments",
    description="Returns every shipment record in the database. "
                "Returns an empty list when no shipments exist yet.",
)
def get_shipments(db: Session = Depends(get_db)) -> list[ShipmentResponse]:
    """
    Retrieve all shipment records from the database.

    Args:
        db: SQLAlchemy database session (injected by FastAPI).

    Returns:
        A list of ShipmentResponse objects (may be empty).
    """
    shipments: list[Shipment] = db.query(Shipment).all()
    return shipments
