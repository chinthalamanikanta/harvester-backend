from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.database import SessionLocal
from app.models.machine import Machine
from app.schemas.machine_schema import MachineCreate

router = APIRouter(
    prefix="/api/machines",
    tags=["Machines"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/add")
def add_machine(
    machine: MachineCreate,
    db: Session = Depends(get_db)
):

    new_machine = Machine(
        owner_id=machine.owner_id,
        machine_name=machine.machine_name,
        machine_type=machine.machine_type,
        price_per_acre=machine.price_per_acre,
        district=machine.district,
        state=machine.state,
        latitude=machine.latitude,
        longitude=machine.longitude
        
    )

    db.add(new_machine)
    db.commit()
    db.refresh(new_machine)

    return {
        "message": "Machine added successfully",
        "machine_id": new_machine.id
    }

@router.get("/")
def get_all_machines(
    db: Session = Depends(get_db)
):
    machines = db.query(Machine).all()
    return machines


@router.put("/{machine_id}")
def update_machine(
    machine_id: int,
    machine_data: MachineCreate,
    db: Session = Depends(get_db)
):

    machine = db.query(Machine).filter(
        Machine.id == machine_id
    ).first()

    if not machine:
        raise HTTPException(
            status_code=404,
            detail="Machine not found"
        )

    machine.machine_name = machine_data.machine_name
    machine.machine_type = machine_data.machine_type
    machine.price_per_acre = machine_data.price_per_acre
    machine.district = machine_data.district
    machine.state = machine_data.state
    machine.availability = machine_data.availability

    db.commit()

    return {
        "message": "Machine updated successfully"
    }

@router.get("/owner/{owner_id}")
def get_owner_machines(
    owner_id: int,
    db: Session = Depends(get_db)
):

    machines = db.query(Machine).filter(
        Machine.owner_id == owner_id
    ).all()

    return machines

@router.get("/search")
def search_machines(
    state: str,
    district: str,
    db: Session = Depends(get_db)
):

    machines = db.query(Machine).filter(
        Machine.state == state,
        Machine.district == district,
        Machine.availability == 1
    ).all()

    return machines