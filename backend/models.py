from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    name : str
    description : str
    price : int 
    category : set
    size : List[str]
    color : List[str]
    image : str


class Order(BaseModel):
    user_email : str
    product_name : str
    quantity : int


class CartItem(BaseModel):
    user_email : str
    product_name : str
    quantity : int
        