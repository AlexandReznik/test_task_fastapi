from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.common.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey('receipts.id'))
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer)
    total = Column(Float)

    receipt = relationship("Receipt", back_populates='products')

    def to_dict(self):
        return {
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'total': self.total,
        }