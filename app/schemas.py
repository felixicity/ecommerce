from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing  import Optional,List


class Product(BaseModel):
    name:str
    description: str
    category: str
    image_url:str
    price:float
    quantity:int


class ProductCreate(Product):
    discount:int

class ProductResponse(Product):
    id:int
    created_at:datetime
    class Config():
        orm_mode = True


class User(BaseModel):
    email:EmailStr

class UserCreate(User):
   password:str

class CreateUserResponse(User):
    id:int
    created_at:datetime
    
    class Config():
        orm_mode = True

class UserLogin(User):
    password:str

class Admin(BaseModel):
    name:str
    email:EmailStr
    password:str
    
class AdminCreate(Admin):
    role:str

class AdminCreateResponse(Admin):
    id:int
    name:str
    role:str

    class Config():
        orm_mode = True

class AdminLogin(Admin):
    pass

class CartItem(BaseModel):
    item_id:int
    quantity:int
    cart_id:int
    
class Cart(BaseModel):
    user_id:int
    items:List[CartItem] = []

class CartOut(Cart):
     id:int
     owner_details:CreateUserResponse

     class Config():
        orm_mode = True

class Token(BaseModel):
    access_token:str
    token_type: str

class TokenData(BaseModel):
    id:int
    created_at: Optional[str] = None

    
class Order(BaseModel):
    amount: float
    currency:str
    item_id:int
    user_id:int
    status:Optional[str]

class OrderCreated(Order):
    id:int
    status:str

    class Config():
        orm_mode = True

class OrderOut(Order):
    id:int
    status:str
    user_details:CreateUserResponse

    class Config():
        orm_mode = True