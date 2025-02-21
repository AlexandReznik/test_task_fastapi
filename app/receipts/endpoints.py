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
    receipts = get_receipts(db, user, filters, limit, offset)
    return create_json_response(receipts)


@router.get('/{receipt_id}')
def get_receipt_endpoint(
    receipt_id: int, 
    user=Depends(require_auth), 
    db: Session = Depends(get_db)
):
    receipt = get_receipt_by_id(db, receipt_id)
    if not receipt:
        return raise_not_found_exception(f"Receipt with id {receipt_id} doesn't exist")
    return create_json_response(receipt.to_dict())


@router.get('/receipt-txt/{receipt_id}', response_class=PlainTextResponse)
def get_receipt(receipt_id: int, chars_per_line: int = 32, db: Session = Depends(get_db)):
    receipt = get_receipt_by_id(db, receipt_id)
    if not receipt:
        return raise_not_found_exception(f"Receipt with id {receipt_id} doesn't exist")
    return format_receipt(receipt, chars_per_line)
    