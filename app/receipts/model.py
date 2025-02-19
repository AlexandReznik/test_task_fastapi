# from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer
# from sqlalchemy.orm import relationship

# from app.common.database import Base


# class Receipt(Base):
#     __tablename__ = 'receipts'

#     id = Column(Integer, primary_key=True)
#     type = Column(Enum('cash', 'cashless', name='payment_type'), nullable=False)
#     amount = Column(Float, nullable=False)
#     total = Column(Float)
#     products = relationship('Product', back_populates='receipt')
#     created_at = Column(DateTime)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     user = relationship('User', back_populates='receipts')
#     rest = Column(Float)
