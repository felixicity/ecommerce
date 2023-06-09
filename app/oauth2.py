from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas,models,database
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from sqlalchemy.orm import Session



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


# We need to provide a secret key , algorithm, expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES  = settings.access_token_expire_minutes


def create_access_token(data : dict):
        to_encode = data.copy()

        expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY ,ALGORITHM)
        
        return encoded_jwt


def verify_access_token(token:str ,credentials_exception):

        try:
            payload = jwt.decode(token,SECRET_KEY,ALGORITHM)

            id: str = payload.get("user_id")

            if not id: 
                    raise credentials_exception
            
            token_data = schemas.TokenData(id = id)
        except JWTError:
            raise credentials_exception
        
        return token_data


def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail="could not validate credentials",headers={"WWW-Authenticate": "Bearer"}) 
        
        token_data= verify_access_token(token,credentials_exception)
        user = db.query(models.User).filter(models.User.id == token_data.id).first()

        return user




def verify_access_token_admin(token:str ,credentials_exception):

        try:
            payload = jwt.decode(token,SECRET_KEY,ALGORITHM)

            id: str = payload.get("user_id")
            role:str = payload.get("role")
            password:str = payload.get("password")

            if not id or not role or not password: 
                raise credentials_exception
            
            token_data = schemas.AdminTokenData(id = id,role=role,password=password)
        except JWTError:
            raise credentials_exception
        
        return token_data


def get_current_admin(token:str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail="could not validate credentials",headers={"WWW-Authenticate": "Bearer"}) 
        
        token_data = verify_access_token_admin(token,credentials_exception)
        admin = db.query(models.Admin).filter(models.Admin.role == token_data.role)

        return admin



def verify_admin_user_access_token_admin(token:str ,credentials_exception):

        try:
            payload = jwt.decode(token,SECRET_KEY,ALGORITHM)

            id: str = payload.get("user_id")
            password:str = payload.get("password")

            if not id or not password: 
                raise credentials_exception
            
            token_data = schemas.AdminUserTokenData(id = id,password=password)
        except JWTError:
            raise credentials_exception
        
        return token_data
        



def get_current_user_admin(token:str = Depends(oauth2_scheme), db:Session = Depends(database.get_db)):
        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail="could not validate credentials",headers={"WWW-Authenticate": "Bearer"}) 
        
        token_data = verify_admin_user_access_token_admin(token,credentials_exception)
        admin = db.query(models.User).filter(models.User.id == token_data.id)

        return admin


