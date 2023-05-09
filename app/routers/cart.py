from fastapi import APIRouter,HTTPException,status, Depends
from sqlalchemy.orm import Session
from .. import database,oauth2,models,schemas
from typing import List,Optional

router = APIRouter(prefix="/cart")


@router.get('/',status_code=status.HTTP_200_OK)
def get_all_cart_items(current_user:models.User = Depends(oauth2.get_current_user)):
    return {"cart": current_user.cart}


# Create a cart for a user

# Add an item to a user's cart
@router.post("/add",status_code=status.HTTP_201_CREATED)
def add_item_to_cart(cart_item: schemas.CartItem, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    # Get the user's cart or create one if it doesn't exist
    cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()
    if not cart:
        cart = models.Cart(user_id = current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Create a new CartItem object and add it to the cart
    item = models.CartItem(**cart_item.dict(), cart_id=cart.id)

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@router.get("/user/{owner_id}",status_code=status.HTTP_200_OK)
def get_cart_items(owner_id:int, db:Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_admin)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == owner_id).first()
    cart_id = cart.id
    cart_items = db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id).all()

    return cart_items


@router.delete("/user/item/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id:int,db:Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_user)):
    product_query = db.query(models.CartItem).filter(models.CartItem.id == id)

    if product_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Cannot delete an item that does not exist")
    
    product_query.delete(synchronize_session=False)
    db.commit()


@router.delete("/user/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_products(owner_id:int,db:Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_user)):
    cart = db.query(models.Cart).filter(models.Cart.user_id == owner_id).first()
    cart_id = cart.id
    cart_query = db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id)

    if cart_query.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Cannot delete all items for a user that does not exist")
   
    cart_query.delete(synchronize_session=False)
    db.commit()

