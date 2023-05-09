from fastapi import APIRouter,Depends,status,HTTPException
from .. import schemas,database,utils,oauth2
from sqlalchemy.orm import Session
from typing import List,Optional
from ..models import Admin

router = APIRouter(prefix='/admin', tags=["Admin"])


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.AdminCreateResponse)
def create_chief_admin(admin:schemas.ChiefAdmin, db: Session = Depends(database.get_db)):
    hashed_pwd = utils.hash(admin.password)
    admin.password = hashed_pwd
    new_admin = Admin(**admin.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin




