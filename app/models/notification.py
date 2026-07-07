from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.database import Base

class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer)

    title = Column(String(255))

    message = Column(String(500))

    is_read = Column(Boolean, default=False)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )