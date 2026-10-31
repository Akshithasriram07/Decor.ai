from pydantic import BaseModel, Field
class CheckoutRequest(BaseModel):
    shipping_name: str = Field(min_length=2, max_length=120)
    shipping_phone: str = Field(min_length=8, max_length=40)
    shipping_address: str = Field(min_length=8, max_length=1000)
class PaymentVerifyRequest(BaseModel):
    order_id: str
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
class OrderItemResponse(BaseModel):
    product_id: str
    name: str
    price: int
    quantity: int
    image: str
class OrderResponse(BaseModel):
    id: str
    total: int
    status: str
    payment_provider: str | None
    payment_reference: str | None
    shipping_name: str
    shipping_phone: str
    shipping_address: str
    created_at: str
    items: list[OrderItemResponse]
