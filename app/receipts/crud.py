from datetime import datetime

from sqlalchemy.orm import Session

from app.products.model import Product
from app.receipts.model import Receipt
from app.receipts.schemas import ReceiptCreateSchema
from app.users.model import User


def create_receipt(db: Session, user: User, receipt_data: ReceiptCreateSchema):
    products = []
    total = 0

    db_receipt = Receipt(
        type=receipt_data.payment.type,
        amount=receipt_data.payment.amount,
        created_at=datetime.now(),
        user_id=user.id
    )
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)

    for product in receipt_data.products:
        db_product = Product(
            name=product.name,
            price=product.price,
            quantity=product.quantity,
            receipt_id=db_receipt.id,
            total=product.price * product.quantity
        )
        products.append({
            'name': product.name,
            'price': product.price,
            'quantity': product.quantity,
            'total': product.price * product.quantity
        })
        db.add(db_product)
        total += product.price * product.quantity

    db_receipt.total = total
    db_receipt.rest = db_receipt.amount - total
    db.commit()

    return db_receipt


def get_receipts(db: Session, user: User, filters, limit: int, offset: int):
    query = filters.filter(db.query(Receipt).filter(Receipt.user_id == user.id)).limit(limit).offset(offset)
    return [receipt.to_dict() for receipt in query]


def get_receipt_by_id(db: Session, receipt_id: int):
    return db.query(Receipt).filter_by(id=receipt_id).first()
