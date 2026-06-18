from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, nullable=False)

    machine_name = Column(String(100))
    machine_type = Column(String(100))

    price_per_acre = Column(DECIMAL(10, 2))

    district = Column(String(100))
    state = Column(String(100))

    availability = Column(Boolean, default=True)

    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )