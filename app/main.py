from fastapi import FastAPI
from app.common.database import engine, Base
from app.users.endpoints import router as user_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["user"])