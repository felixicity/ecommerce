from sqlalchemy import Boolean, Column, ForeignKey, Integer,String,JSON
from sqlalchemy.orm import relationship,Mapped
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from typing import List

from .database import Base



    

class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key= True, nullable=False)
    name = Column(String,nullable=False)
    email = Column(String, nullable=False,unique=True)
    password = Column(String, nullable=False)
    role = Column(String, server_default="admin", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
                        nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key= True, nullable=False,index=True)
    email = Column(String, nullable=False,unique=True,index=True)
    password = Column(String, nullable=False)
    isActive = Column(Boolean, default=True)
    isAdmin = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    cart = relationship("Cart", uselist = False, back_populates="user")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, nullable=False)
    status = Column(String, server_default="pending", nullable=False)
    amount = Column(Integer,nullable=False)
    currency = Column(String,nullable=False)
    item_id= Column(Integer,ForeignKey("products.id",ondelete="CASCADE"),nullable=False)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    user_details= relationship("User")

class CartItem(Base):
    __tablename__ = 'cart_item'
    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"),nullable=False)
    quantity = Column(Integer)
    cart_id = Column(Integer, ForeignKey("cart.id", ondelete="CASCADE") ,nullable=False)
    cart= relationship("Cart", back_populates='items')

class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False)
    items= relationship("CartItem", back_populates='cart')
    user = relationship("User",back_populates="cart")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))



