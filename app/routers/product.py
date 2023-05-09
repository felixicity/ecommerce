from fastapi import APIRouter,HTTPException,status, Depends
from sqlalchemy.orm import Session
from .. import models,database,oauth2
from typing import List,Optional
from .. schemas import ProductResponse,ProductCreate


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/",status_code=status.HTTP_200_OK, response_model=List[ProductResponse])
def get_products(db:Session= Depends(database.get_db),limit : int = 50, skip:int = 0, search : Optional[str] = "",current_user = Depends(oauth2.get_current_admin)):

    products = db.query(models.Product).filter( models.Product.name.contains(search)).limit(limit).offset(skip).all()
    
    if not products:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail=f"you cannot perform this operation")
    
    return products



@router.post("/", status_code = status.HTTP_201_CREATED, response_model = ProductResponse)
def create_product(product: ProductCreate , db:Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_admin)):
    new_product = models.Product(**product.dict())


    if not new_product:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,detail=f"you cannot perform this operation")
    
    db.add(new_product)
    db.commit() 
    db.refresh(new_product)
    return new_product



@router.get("/{id}" ,status_code=status.HTTP_200_OK,response_model = ProductResponse)
def get_single_product(id:int, db: Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_admin)):

    single_product = db.query(models.Product).filter(models.Product.id == id).first()
    
    if not single_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"No product with id {id} was found")
    
    return single_product

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id:int,db:Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_admin)):
   product_query = db.query(models.Product).filter(models.Product.id == id)

   if product_query.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Cannot delete a delete that does not exist")
   
   product_query.delete(synchronize_session=False)
   db.commit()


@router.put("/{id}", status_code=status.HTTP_205_RESET_CONTENT,response_model=ProductResponse)
def update_product(updated_product:ProductCreate,id:int,db:Session = Depends(database.get_db),current_user = Depends(oauth2.get_current_admin)):
   
    product_query = db.query(models.Product).filter(models.Product.id == id)

    if product_query.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Cannot Update a product that does not exist")
   
    product_query.update(updated_product.dict(),synchronize_session=False)
    db.commit()

    return product_query.first()
