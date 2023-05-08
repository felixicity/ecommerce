from fastapi import APIRouter, HTTPException, status,Depends
from ..models import User
from ..schemas import UserCreate,CreateUserResponse
from sqlalchemy.orm import Session
from ..database import get_db
from .. import utils,oauth2
from typing import List,Optional


router = APIRouter(
    prefix="/users",
    tags=["Users"]
    )


@router.post("/", status_code = status.HTTP_201_CREATED,response_model= CreateUserResponse)
def create_user(user:UserCreate, db:Session = Depends(get_db)):
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get("/{id}",status_code=status.HTTP_200_OK,response_model= CreateUserResponse)
def get_single_user(id:int,db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_admin)):

    single_user = db.query(User).filter(User.id == id).first()

    print(current_user.role)

    if not single_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"No user with id {id} was found")
    
    return single_user


@router.get("/",status_code=status.HTTP_200_OK,response_model= List[CreateUserResponse])
def get_all_users(db:Session = Depends(get_db) ,limit : int = 10, skip:int = 0, search : Optional[str] = "",current_user = Depends(oauth2.get_current_admin)):

    all_users = db.query(User).filter(User.username.contains(search)).limit(limit).offset(skip).all()


    if not all_users:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail = f"Query couldn't go through")
    
    return all_users


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int,db:Session = Depends( get_db),current_user = Depends(oauth2.get_current_user)):
   user_query = db.query(User).filter(User.id == id)

   if user_query.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Cannot delete a delete that does not exist")
   
   user_query.delete(synchronize_session=False)
   db.commit()


@router.put("/{id}", status_code=status.HTTP_205_RESET_CONTENT,response_model= CreateUserResponse)
def update_user(updated_user:UserCreate,id:int,db:Session = Depends( get_db),current_user = Depends(oauth2.get_current_user)):
   
    user_query = db.query(User).filter(User.id == id)

    if user_query.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"Cannot Update a user that does not exist")
   
    user_query.update(updated_user.dict(),synchronize_session=False)
    db.commit()

    return user_query.first()

