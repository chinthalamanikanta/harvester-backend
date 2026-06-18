from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey
from app.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("users.id"))
    machine_id = Column(Integer, ForeignKey("machines.id"))
    acres = Column(Float)

    booking_date = Column(Date)

    requested_date = Column(Date)

    status = Column(String(20), default="PENDING")