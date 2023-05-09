from fastapi import APIRouter,HTTPException,status, Depends
from sqlalchemy.orm import Session
from .. import models,database,oauth2
from typing import List,Optional
from .. schemas import Order,OrderOut,OrderCreated,OrderCreate

router = APIRouter(prefix="/order")


@router.post('/',status_code=status.HTTP_201_CREATED, response_model=OrderCreated)
def add_to_order(order:OrderCreate , db:Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_user)):
    order_item = models.Order(user_id = current_user.id,**order.dict())
    
    db.add(order_item)
    db.commit()
    db.refresh(order_item)

    return order_item
    
@router.get("/",status_code=status.HTTP_200_OK , response_model=List[OrderOut])
def get_order_items( db:Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_admin)):

    order_items = db.query(models.Order).all()


    if not order_items:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = f"Query couldn't go through")
    
    return order_items

@router.get("/{user_id}",status_code=status.HTTP_200_OK , response_model=List[OrderCreated])
def get_order_items(user_id:int ,db:Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_user)):

    order_items = db.query(models.Order).filter(models.Order.user_id == user_id).all()


    if not order_items:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = f"Query couldn't go through")
    
    return order_items


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id:int,db:Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_admin)):
   product_query = db.query(models.Order).filter(models.Order.id == id)

   if product_query.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Cannot delete a delete that does not exist")
   
   product_query.delete(synchronize_session=False)
   db.commit()


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_products(id:int,db:Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_admin)):
   product_query = db.query(models.Order).filter(models.Order.user_id == id)

   if product_query.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Cannot delete a delete that does not exist")
   
   product_query.delete(synchronize_session=False)
   db.commit()


@router.put("/{id}", status_code=status.HTTP_205_RESET_CONTENT,response_model=OrderOut)
def update_product(updated_order:Order,id:int,db:Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_user)):
   
    order_query = db.query(models.Order).filter(models.Order.id == id)

    if order_query.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Cannot Update a order that does not exist")
   
    order_query.update(**updated_order.dict(),synchronize_session=False)
    db.commit()

    return order_query.first()