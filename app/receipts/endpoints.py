from fastapi import APIRouter, Depends, Query
from fastapi.responses import PlainTextResponse
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session

from app.common.common_utils import (create_json_response, format_receipt,
                                     raise_not_found_exception)
from app.common.database import get_db
from app.common.dependencies import require_auth
from app.receipts.crud import create_receipt, get_receipt_by_id, get_receipts
from app.receipts.filters import ReceiptFilter
from app.receipts.schemas import ReceiptCreateSchema


router = APIRouter()


@router.post('/')
def create_receipt_endpoint(
    receipt: ReceiptCreateSchema,
    user=Depends(require_auth),
    db: Session = Depends(get_db)
):
    """
    Creates a new receipt for a user.

    Args:
        receipt (ReceiptCreateSchema): The data to create the receipt.
        user (User): The authenticated user creating the receipt.
        db (Session): The database session to interact with the database.

    Returns:
        JSONResponse: The created receipt data in JSON format.
    """
    db_receipt = create_receipt(db, user, receipt)
    return create_json_response(db_receipt.to_dict())


@router.get('/')
def receipts_list(
    user=Depends(require_auth),
    db: Session = Depends(get_db),
    filters: ReceiptFilter = FilterDepends(ReceiptFilter),
    limit: int = Query(100, ge=0),
    offset: int = Query(0, ge=0)
):
    """
    Retrieves a list of receipts for a specific user with optional filters and pagination.

    Args:
        user (User): The authenticated user whose receipts to retrieve.
        db (Session): The database session to interact with the database.
        filters (ReceiptFilter): Optional filter object to filter the receipts.
        limit (int): The maximum number of receipts to retrieve (default is 100).
        offset (int): The number of receipts to skip from the start (default is 0).

    Returns:
        JSONResponse: A list of receipts in JSON format.
    """
    receipts = get_receipts(db, user, filters, limit, offset)
    return create_json_response(receipts)


@router.get('/{receipt_id}')
def get_receipt_endpoint(
    receipt_id: int, 
    user=Depends(require_auth), 
    db: Session = Depends(get_db)
):
    """
    Retrieves a specific receipt by its ID.

    Args:
        receipt_id (int): The ID of the receipt to retrieve.
        user (User): The authenticated user making the request.
        db (Session): The database session to interact with the database.

    Returns:
        JSONResponse: The requested receipt data in JSON format.

    Raises:
        HTTPException: If the receipt is not found.
    """
    receipt = get_receipt_by_id(db, receipt_id)
    if not receipt:
        return raise_not_found_exception(f"Receipt with id {receipt_id} doesn't exist")
    return create_json_response(receipt.to_dict())


@router.get('/receipt-txt/{receipt_id}', response_class=PlainTextResponse)
def get_receipt(receipt_id: int, chars_per_line: int = 32, db: Session = Depends(get_db)):
    """
    Retrieves a formatted text version of a specific receipt.

    Args:
        receipt_id (int): The ID of the receipt to retrieve in text format.
        chars_per_line (int): The number of characters per line for formatting (default is 32).
        db (Session): The database session to interact with the database.

    Returns:
        str: The receipt data in a formatted plain text version.

    Raises:
        HTTPException: If the receipt is not found.
    """
    receipt = get_receipt_by_id(db, receipt_id)
    if not receipt:
        return raise_not_found_exception(f"Receipt with id {receipt_id} doesn't exist")
    return format_receipt(receipt, chars_per_line)