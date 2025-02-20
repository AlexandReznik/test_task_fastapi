from fastapi import FastAPI
from app.common.database import engine, Base
from app.users.endpoints import router as user_router
from app.receipts.endpoints import router as receipt_router

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(receipt_router, prefix="/receipt", tags=["receipt"])

Base.metadata.create_all(bind=engine)