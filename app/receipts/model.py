from sqlalchemy import (Column, DateTime, Enum, Float, ForeignKey, Index,
                        Integer)
from sqlalchemy.orm import relationship

from app.common.database import Base


class Receipt(Base):
    __tablename__ = 'receipts'

    id = Column(Integer, primary_key=True)
    type = Column(Enum('cash', 'cashless', name='payment_type'), nullable=False)
    amount = Column(Float, nullable=False)
    total = Column(Float)
    created_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    rest = Column(Float)

    user = relationship("User", back_populates='receipts')
    products = relationship("Product", back_populates='receipt')

    __table_args__ = (
        Index('ix_receipt_total', 'total'),  
        Index('ix_receipt_created_at', 'created_at'),  
    )

    def to_dict(self):
        return {
            'id': self.id,
            'products': [product.to_dict() for product in self.products],
            'payment': {
                'type': self.type,
                'amount': self.amount
            },
            'total': self.total,
            'rest': self.rest,
            'created_at': self.created_at.isoformat(),
        }