from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.products.model import Product
from app.receipts.model import Receipt
from app.receipts.schemas import ReceiptCreateSchema
from app.users.model import User
from app.common.common_utils import calculate_product_total


def create_receipt(db: Session, user: User, receipt_data: ReceiptCreateSchema):
    """
    Creates a new receipt and associated products in the database.

    Args:
        db (Session): The database session to use for transactions.
        user (User): The user who is creating the receipt.
        receipt_data (ReceiptCreateSchema): The data for creating the receipt, 
        including payment and products.

    Returns:
        Receipt: The created receipt object with products and total amounts.

    Raises:
        HTTPException: If the payment amount is insufficient.
    """
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
        product_total = calculate_product_total(product.price, product.quantity)
        db_product = Product(
            name=product.name,
            price=product.price,
            quantity=product.quantity,
            receipt_id=db_receipt.id,
            total=product_total
        )
        products.append({
            'name': product.name,
            'price': product.price,
            'quantity': product.quantity,
            'total': product_total
        })
        db.add(db_product)
        total += product_total

    if db_receipt.amount < total:
        db.rollback() 
        raise HTTPException(
            status_code=400, 
            detail=f"Insufficient payment: required {total}, but received {db_receipt.amount}"
        )
    
    db_receipt.total = total
    db_receipt.rest = db_receipt.amount - total
    db.commit()

    return db_receipt


def get_receipts(db: Session, user: User, filters, limit: int, offset: int):
    """
    Retrieves a list of receipts for a specific user with optional filters.

    Args:
        db (Session): The database session to use for queries.
        user (User): The user whose receipts to retrieve.
        filters (Filter): The filter object to apply to the query.
        limit (int): The maximum number of receipts to retrieve.
        offset (int): The number of receipts to skip from the start.

    Returns:
        List[dict]: A list of receipt dictionaries.
    """
    query = filters.filter(db.query(Receipt).filter(
        Receipt.user_id == user.id)).limit(limit).offset(offset)
    return [receipt.to_dict() for receipt in query]


def get_receipt_by_id(db: Session, receipt_id: int):
    """
    Retrieves a receipt by its ID.

    Args:
        db (Session): The database session to use for the query.
        receipt_id (int): The ID of the receipt to retrieve.

    Returns:
        Receipt: The receipt object, or None if not found.
    """
    return db.query(Receipt).filter_by(id=receipt_id).first()
