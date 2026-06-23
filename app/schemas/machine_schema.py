from pydantic import BaseModel
from typing import Optional

class MachineCreate(BaseModel):
    owner_id: int
    machine_name: str
    machine_type: str
    price_per_acre: float
    district: str
    state: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    availability: bool