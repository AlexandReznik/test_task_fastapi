from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.receipts.model import Receipt


def create_json_response(data, status_code=status.HTTP_200_OK):
    """
    Creates a JSON response.

    Args:
        data (dict): The data to be included in the response body.
        status_code (int): The HTTP status code (default is 200).

    Returns:
        JSONResponse: The JSON response with the provided data and status code.
    """
    return JSONResponse(status_code=status_code, content=data)


def raise_not_found_exception(detail: str):
    """
    Raises an HTTP 404 Not Found exception with a custom detail message.

    Args:
        detail (str): The detail message to be sent in the exception.

    Raises:
        HTTPException: Raises a 404 HTTPException with the provided detail message.
    """
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def calculate_product_total(price: float, quantity: int) -> float:
    """
    Calculates the total price for a product.

    Args:
        price (float): The price of a single unit of the product.
        quantity (int): The number of units of the product.

    Returns:
        float: The total price (price * quantity).
    """
    return price * quantity


def format_receipt(receipt: Receipt, line_width: int) -> str:
    """
    Formats a receipt into a string representation.

    Args:
        receipt (Receipt): The receipt object to format.
        line_width (int): The width of the lines in the formatted receipt.

    Returns:
        str: The formatted receipt as a string.
    """
    lines = []
    
    payment_types = {"cash": "Готівка", "cashless": "Картка"}
    payment_type = payment_types.get(receipt.type.lower(), receipt.type)  

    lines.append(receipt.user.username.center(line_width))
    lines.append("=" * line_width)

    for product in receipt.products:
        product_dict = product.to_dict()
        quantity_price = f"{product_dict['quantity']} x {product_dict['price']}"
        total = f"{product_dict['total']:.2f}"
        
        lines.append(f"{quantity_price.ljust(line_width // 2)}{total.rjust(line_width // 2)}")
        lines.append(product_dict['name'])
        lines.append("-" * line_width)

    lines.append("=" * line_width)

    lines.append(f"{'СУМА'.ljust(line_width - 7)}{receipt.total:7.2f}")
    lines.append(payment_type.ljust(line_width - 7) + f"{receipt.amount:.2f}".rjust(7))  
    lines.append(f"{'Решта'.ljust(line_width - 7)}{receipt.rest:7.2f}")

    lines.append("=" * line_width)
    lines.append(receipt.created_at.strftime("%d.%m.%Y %H:%M").center(line_width))
    lines.append("Дякуємо за покупку!".center(line_width))

    return "\n".join(lines)