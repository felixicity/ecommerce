from fastapi import APIRouter,HTTPException,status, Depends
from sqlalchemy.orm import Session
from .. import database,oauth2,models,schemas
from typing import List,Optional

router = APIRouter(prefix="/cart")


@router.get('/',status_code=status.HTTP_200_OK)
def get_all_cart_items(current_user:models.User = Depends(oauth2.get_current_user)):
    return {"cart": current_user.cart}
    

@router.post("/add", status_code=status.HTTP_201_CREATED)
def add_to_cart(
    cart_item: schemas.CartItem,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    item = db.query(models.Product).filter(models.Product.id == cart_item.item_id).first()

    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item does not exist")

    
    # Create the new CartItem object and add it to the database
    new_item = models.CartItem(**cart_item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    # Get the user's cart or create a new cart if one doesn't exist yet
    user_cart = db.query(models.Cart).filter(models.Cart.user_id == current_user.id).first()
    if not user_cart:
        user_cart = models.Cart(user_id=current_user.id, items=[])

    # Add the new item to the user's cart and update the cart in the database
    user_cart.items.append(new_item)
    db.add(user_cart)
    db.commit()

    return new_item



@router.get("/{owner_id}",status_code=status.HTTP_200_OK, response_model=List[schemas.CartOut])
def get_cart_items(owner_id:int, db:Session = Depends(database.get_db)):

    cart_items = db.query(models.Cart).filter(models.Cart.owner_id == owner_id).all()

    return cart_items


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id:int,db:Session = Depends(database.get_db)):
   product_query = db.query(models.Cart).filter(models.Cart.id == id)

   if product_query.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Cannot delete an item that does not exist")
   
   product_query.delete(synchronize_session=False)
   db.commit()


@router.delete("/user/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_products(owner_id:int,db:Session = Depends(database.get_db)):
   product_query = db.query(models.Cart).filter(models.Cart.owner_id == owner_id)

   if product_query.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Cannot delete all items for a user that does not exist")
   
   product_query.delete(synchronize_session=False)
   db.commit()


# @router.put("/{id}", status_code=status.HTTP_205_RESET_CONTENT,response_model=CartOut)
# def update_product(updated_product:Cart,id:int,db:Session = Depends(database.get_db)):
   
#     product_query = db.query(models.Product).filter(models.Product.id == id)

#     if product_query.first() == None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Cannot Update a product that does not exist")
   
#     product_query.update(**updated_product.dict(),synchronize_session=False)
#     db.commit()

    # return product_query.first()