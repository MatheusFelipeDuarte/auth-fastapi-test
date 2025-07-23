
from ast import expr_context
from datetime import datetime, timezone, timedelta
from hashlib import sha256
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import UserModel
from app.schemas import User
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from fastapi import status
from jose import jwt, JWTError
from decouple import config


crypt_context = CryptContext(["sha256_crypt"],sha256_crypt__default_rounds=77123)
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

class UserUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def user_register(self,user: User):

        user_model = UserModel(
            username= user.username,
            password =crypt_context.hash(user.password)
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User Already exists')
        
    def user_login(self,user:User, expires_in: int = 30):
        user_on_db = self.db_session.query(UserModel).filter_by(username=user.username).first() #posso usar o scalar aqui tbm
        # user_on_db = self.db_session.scalar(select(UserModel).where(UserModel.username == user.username))
        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid username or password'
            )

        if not crypt_context.verify(user.password,user_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid username or password'
            )
        exp = datetime.now(timezone.utc) + timedelta(minutes=expires_in)
        # O próprio JWT já entende o exp e analisa ele ao validar o access token. 
        payload = {
            'sub': user.username,
            "exp": exp,
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return {
            'access_token':access_token,
            'exp':exp.isoformat()
        }
    
    def verify_access_token(self,access_token):
        try:
            data = jwt.decode(access_token,SECRET_KEY,algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid access token")
        user_on_db = self.db_session.query(UserModel).filter_by(username=data['sub']).first() #posso usar o scalar aqui tbm
        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid username or password'
            )