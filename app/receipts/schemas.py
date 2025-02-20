from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.products.schemas import ProductCreateSchema, ProductSchema


class PaymentSchema(BaseModel):
    type: str
    amount: float

    class Config:
        from_attributes = True


class ReceiptBaseSchema(BaseModel):
    products: List[ProductCreateSchema]

    class Config:
        from_attributes = True


class ReceiptCreateSchema(ReceiptBaseSchema):
    payment: PaymentSchema


class ReceiptSchema(ReceiptBaseSchema):
    id: int
    products: List[ProductSchema]
    total: float
    rest: float
    created_at: datetime
    type: str
    amount: float


class PersonalReceipts(BaseModel):
    receipts: List[ReceiptSchema]