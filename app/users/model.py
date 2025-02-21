from sqlalchemy import Column, Index, Integer, String
from sqlalchemy.orm import relationship

from app.common.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    login = Column(String, unique=True)
    password = Column(String)

    receipts = relationship("Receipt", back_populates='user')

    __table_args__ = (
        Index('ix_user_login', 'login'),  
    )