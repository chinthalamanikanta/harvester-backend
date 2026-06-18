from pydantic import BaseModel

class MachineCreate(BaseModel):
    owner_id: int
    machine_name: str
    machine_type: str
    price_per_acre: float
    district: str
    state: str
    availability: bool