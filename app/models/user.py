from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    phone = Column(String(15), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    role = Column(String(20), nullable=False)
    profile_image = Column(String, nullable=True)
    
    profile_image = Column(
    String(255),
    nullable=True
)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )