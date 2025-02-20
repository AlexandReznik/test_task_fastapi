from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


def create_json_response(data, status_code=status.HTTP_200_OK):
    return JSONResponse(status_code=status_code, content=data)

def raise_not_found_exception(detail: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
