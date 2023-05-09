from fastapi import APIRouter, Depends, status, HTTPException,Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import  database,schemas,models,utils,oauth2


router = APIRouter(prefix="/login",tags=['Authentication'])


@router.post('/user',response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends() , db : Session = Depends(database.get_db) ):
    
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
     
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    
    access_token = oauth2.create_access_token(data = {"user_id":user.id})

    return {"access_token":access_token,"token_type":"Bearer"}



@router.post('/admin',response_model=schemas.Token)
def admin_login(admin_credentials : OAuth2PasswordRequestForm = Depends() , db: Session = Depends( database.get_db)):

    admin = db.query(models.Admin).filter(models.Admin.email == admin_credentials.username).first()

    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Invalid Credentials")
    
    if not utils.verify(admin_credentials.password,admin.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id":admin.id,"role":admin.role,"password":admin.password})

    return {"access_token":access_token, "token_type":"Bearer"}


@router.post('/admin_user',response_model=schemas.Token)
def admin_user_login(admin_credentials : OAuth2PasswordRequestForm = Depends() , db: Session = Depends( database.get_db)):

    admin = db.query(models.User).filter(models.User.email == admin_credentials.username, models.User.isAdmin == True).first()

    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Invalid Credentials")
    
    if not utils.verify(admin_credentials.password,admin.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id":admin.id,"password":admin.password})

    return {"access_token":access_token,"token_type":"Bearer"}

