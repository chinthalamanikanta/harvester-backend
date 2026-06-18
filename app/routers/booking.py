from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.machine import Machine
from app.database import SessionLocal
from app.models.booking import Booking
from app.schemas.booking_schema import BookingCreate
from app.models.user import User
from app.models.machine import Machine
from sqlalchemy import Column, Date
requested_date = Column(Date)
router = APIRouter(
    prefix="/api/bookings",
    tags=["Bookings"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db)
):

    new_booking = Booking(
        farmer_id=booking.farmer_id,
        machine_id=booking.machine_id,
        acres=booking.acres,
        booking_date=booking.booking_date,
        requested_date=booking.requested_date
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return {
        "message": "Booking created successfully",
        "booking_id": new_booking.id
    }

@router.get("/")
def get_all_bookings(
    db: Session = Depends(get_db)
):
    bookings = db.query(Booking).all()
    return bookings

@router.put("/{booking_id}/accept")
def accept_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    booking.status = "ACCEPTED"

    db.commit()

    return {
        "message": "Booking accepted"
    }

@router.put("/{booking_id}/reject")
def reject_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    booking.status = "REJECTED"

    db.commit()

    return {
        "message": "Booking rejected"
    }

@router.get("/farmer/{farmer_id}")
def get_farmer_bookings(
    farmer_id: int,
    db: Session = Depends(get_db)
):

    results = (
        db.query(
            Booking,
            Machine.machine_name.label("machine_name"),
            User.name.label("owner_name"),
            User.phone.label("owner_phone")
        )
        .join(
            Machine,
            Booking.machine_id == Machine.id
        )
        .join(
            User,
            Machine.owner_id == User.id
        )
        .filter(
            Booking.farmer_id == farmer_id
        )
        .all()
    )

    response = []

    for booking, machine_name, owner_name, owner_phone in results:

        response.append({
            "id": booking.id,
            "machine_name": machine_name,
            "owner_name": owner_name,
            "owner_phone": owner_phone,
            "acres": booking.acres,
            "requested_date": booking.requested_date,
            "status": booking.status
        })

    return response


@router.get("/owner/{owner_id}")
def get_owner_bookings(
    owner_id: int,
    db: Session = Depends(get_db)
):

    results = (
        db.query(
            Booking,
            User.name.label("farmer_name"),
            User.phone.label("farmer_phone"),
            Machine.machine_name.label("machine_name")
        )
        .join(
            Machine,
            Booking.machine_id == Machine.id
        )
        .join(
            User,
            Booking.farmer_id == User.id
        )
        .filter(
            Machine.owner_id == owner_id
        )
        .all()
    )

    response = []

    for booking, farmer_name, farmer_phone, machine_name in results:

        response.append({
            "id": booking.id,
            "farmer_name": farmer_name,
            "farmer_phone": farmer_phone,
            "machine_name": machine_name,
            "acres": booking.acres,
            "requested_date": booking.requested_date,
            "status": booking.status
        })

    return response

@router.get("/owner/{owner_id}/stats")
def owner_dashboard_stats(
    owner_id: int,
    db: Session = Depends(get_db)
):

    bookings = (
        db.query(Booking)
        .join(
            Machine,
            Booking.machine_id == Machine.id
        )
        .filter(
            Machine.owner_id == owner_id
        )
        .all()
    )

    total_bookings = len(bookings)

    pending = len([
        b for b in bookings
        if b.status == "PENDING"
    ])

    accepted = len([
        b for b in bookings
        if b.status == "ACCEPTED"
    ])

    earnings = 0

    for booking in bookings:

        if booking.status == "ACCEPTED":

            machine = db.query(Machine).filter(
                Machine.id == booking.machine_id
            ).first()

            earnings += (
                booking.acres *
                float(machine.price_per_acre)
            )

    return {
        "total_bookings": total_bookings,
        "pending_requests": pending,
        "accepted_jobs": accepted,
        "earnings": earnings
    }