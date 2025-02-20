from pydantic import BaseModel


class ProductBaseSchema(BaseModel):
    name: str
    price: float
    quantity: int

    class Config:
        from_attributes = True


class ProductCreateSchema(ProductBaseSchema):
    pass


class ProductSchema(ProductBaseSchema):
    id: int
    total: float
