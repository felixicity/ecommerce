from sqlalchemy import event
from . import models

@event.listens_for(models.User, "after_insert")
def create_empty_cart(mapper, connection, target):
    new_cart = models.Cart(user_id=target.id, items=[])
    connection.add(new_cart)
    connection.commit()
