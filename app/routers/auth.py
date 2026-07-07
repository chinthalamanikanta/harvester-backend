from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database import SessionLocal
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.utils.security import hash_password
from app.utils.security import verify_password
from app.utils.jwt_handler import create_access_token
from fastapi import UploadFile, File
import os


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    new_user = User(
        name=user.name,
        phone=user.phone,
        password="",
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users 


@router.post("/login")
def login(
    phone: str,
    # password: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.phone == phone
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # if not verify_password(password, user.password):
    #     raise HTTPException(
    #         status_code=401,
    #         detail="Invalid password"
    #     )

    # token = create_access_token(
    # {
    #     "user_id": user.id,
    #     "role": user.role
    # }
# )

    return {
        # "access_token": token,
        # "token_type": "bearer",
        "user_id": user.id,
        "role": user.role
    }

@router.get("/user/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "name": user.name,
        "phone": user.phone,
        "role": user.role,
        "profile_image": user.profile_image
    }

@router.put("/user/{user_id}")
def update_user(
    user_id: int,
    user_data: dict,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.name = user_data["name"]
    user.phone = user_data["phone"]

    db.commit()

    return {
        "message": "Profile updated"
    }



@router.post("/upload-profile/{user_id}")
def upload_profile(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Create uploads folder if not exists
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/profile_{user_id}.jpg"

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user:
        user.profile_image = file_path
        db.commit()

    return {
        "message": "Profile image uploaded",
        "profile_image": file_path
    }

@router.put("/save-token/{user_id}")
def save_token(
    user_id: int,
    token: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.fcm_token = token

    db.commit()

    return {
        "message": "Token Saved"
    }