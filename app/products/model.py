from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.common.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer)
    receipt_id = Column(Integer, ForeignKey('receipts.id'))
    receipt = relationship('Receipt', back_populates='products')
    total = Column(Float)
