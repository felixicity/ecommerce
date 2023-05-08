from fastapi import APIRouter,Depends,status,HTTPException
from .. import schemas,database,utils,oauth2
from sqlalchemy.orm import Session
from typing import List,Optional
from ..models import Admin

router = APIRouter(prefix='/admin', tags=["Admin"])

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.AdminCreateResponse,)
def admin_login(admin:schemas.AdminCreate, db:Session = Depends(database.get_db) , get_admin = Depends(oauth2.get_current_user)):
    
    hashed_pwd = utils.hash(admin.password)
    admin.password = hashed_pwd
    new_admin = Admin(**admin.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return new_admin



@router.put("/{id}", status_code=status.HTTP_205_RESET_CONTENT)
def update_admin(id:int,updated_user:schemas.AdminLogin, db:Session = Depends(database.get_db), get_admin = Depends(oauth2.get_current_user)):
    admin_query = db.query(Admin).filter(Admin.id == id)
     
    print(get_admin.role)
    if admin_query.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOD,detail= f"Cannot Update a user that does not exist")
    
    admin_query.update(updated_user.dict(),synchronize_session=False)
    db.commit()

    return admin_query.first()




