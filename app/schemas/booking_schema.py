from pydantic import BaseModel
from datetime import date

class BookingCreate(BaseModel):
    farmer_id: int
    machine_id: int
    acres: float
    booking_date: date
    requested_date: date