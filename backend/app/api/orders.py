from uuid import uuid4
import hmac, hashlib, base64, json
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.api.deps import DB, CurrentUser
from app.models import CartItem, Order, OrderItem, Notification
from app.schemas.order import *
from app.core.config import settings
import httpx

router=APIRouter(prefix="/api/orders",tags=["Orders & Payments"])

def cart_rows(db,user_id):
    return db.scalars(select(CartItem).where(CartItem.user_id==user_id)).all()

@router.post("/checkout")
def checkout(payload: CheckoutRequest,user:CurrentUser,db:DB):
    rows=cart_rows(db,user.id)
    if not rows: raise HTTPException(400,"Your cart is empty")
    subtotal=sum(r.product.price*r.quantity for r in rows if r.product)
    shipping=0 if subtotal>=50000 else 499
    total=subtotal+shipping
    order=Order(id=str(uuid4()),user_id=user.id,total=total,status="payment_pending",
                payment_provider="razorpay" if settings.razorpay_key_id else "demo",
                shipping_name=payload.shipping_name,shipping_phone=payload.shipping_phone,shipping_address=payload.shipping_address)
    db.add(order); db.flush()
    for r in rows:
        if r.product:
            db.add(OrderItem(id=str(uuid4()),order_id=order.id,product_id=r.product_id,name=r.product.name,
                             price=r.product.price,quantity=r.quantity,image=r.product.image))
    payment=None
    if settings.razorpay_key_id and settings.razorpay_key_secret:
        auth=(settings.razorpay_key_id,settings.razorpay_key_secret)
        response=httpx.post("https://api.razorpay.com/v1/orders",
                            auth=auth,json={"amount":total*100,"currency":"INR","receipt":order.id},timeout=30)
        response.raise_for_status()
        payment=response.json()
        order.payment_reference=payment["id"]
    if payment is None:
        order.status = "paid"
        order.payment_reference = "demo-payment"
        for row in rows:
            db.delete(row)
        db.add(
            Notification(
                id=str(uuid4()),
                user_id=user.id,
                title="Order confirmed",
                message=f"Demo order {order.id[:8]} has been confirmed.",
            )
        )

    db.commit()
    return {
        "order_id": order.id,
        "amount": total,
        "currency": "INR",
        "payment_provider": order.payment_provider,
        "razorpay_order": payment,
    }

@router.post("/verify")
def verify(payload:PaymentVerifyRequest,user:CurrentUser,db:DB):
    order=db.scalar(select(Order).where(Order.id==payload.order_id,Order.user_id==user.id))
    if not order: raise HTTPException(404,"Order not found")
    if not settings.razorpay_key_secret: raise HTTPException(400,"Razorpay is not configured")
    message=f"{payload.razorpay_order_id}|{payload.razorpay_payment_id}".encode()
    expected=hmac.new(settings.razorpay_key_secret.encode(),message,hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected,payload.razorpay_signature): raise HTTPException(400,"Payment signature verification failed")
    order.status="paid"; order.payment_reference=payload.razorpay_payment_id
    for r in cart_rows(db,user.id): db.delete(r)
    db.add(Notification(id=str(uuid4()),user_id=user.id,title="Order confirmed",message=f"Order {order.id[:8]} has been confirmed."))
    db.commit()
    return {"message":"Payment verified","order_id":order.id,"status":"paid"}

@router.get("",response_model=list[OrderResponse])
def orders(user:CurrentUser,db:DB):
    rows=db.scalars(select(Order).where(Order.user_id==user.id).order_by(Order.created_at.desc())).all()
    return [{"id":o.id,"total":o.total,"status":o.status,"payment_provider":o.payment_provider,
             "payment_reference":o.payment_reference,"shipping_name":o.shipping_name,"shipping_phone":o.shipping_phone,
             "shipping_address":o.shipping_address,"created_at":o.created_at.isoformat(),
             "items":[{"product_id":i.product_id,"name":i.name,"price":i.price,"quantity":i.quantity,"image":i.image} for i in o.items]} for o in rows]
