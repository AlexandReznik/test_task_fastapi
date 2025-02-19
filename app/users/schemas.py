from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    login: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)


class UserResponse(BaseModel):
    login: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    token: str


class UserAuth(BaseModel):
    login: str
    password: str
