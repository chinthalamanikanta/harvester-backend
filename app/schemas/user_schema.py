from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    phone: str
    # password: str
    role: str


class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    role: str

    class Config:
        from_attributes = True