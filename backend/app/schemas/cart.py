from pydantic import BaseModel, Field
class CartAdd(BaseModel):
    product_id: str
    quantity: int = Field(default=1, ge=1, le=20)
class CartUpdate(BaseModel):
    quantity: int = Field(ge=1, le=20)
class CartItemResponse(BaseModel):
    id: str
    product_id: str
    quantity: int
    name: str
    price: int
    image: str
    line_total: int
class CartResponse(BaseModel):
    items: list[CartItemResponse]
    subtotal: int
    shipping: int
    total: int
