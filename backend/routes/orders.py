from fastapi import APIRouter
from ..models import Order
from ..database import orders_collection

router = APIRouter(prefix = "/order", tags = ["Order"])

router.post("")
def place_order(order : Order):
    order_data = order.model_dump()
    orders_collection.insert_one(order_data)
    return {"message" : "Order placed successfully!"}
