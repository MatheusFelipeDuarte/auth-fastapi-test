from fastapi import Depends
from sqlalchemy.orm import Session as Session_type
from fastapi.security import OAuth2PasswordBearer
from app.auth_user import UserUseCases
from app.db.connection import Session

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/user/login')



def get_db_session():
    try:
        session = Session()
        yield session
    finally:
        session.close()

def token_verifier(db_session: Session_type = Depends(get_db_session), token = Depends(oauth_scheme)):
    uc = UserUseCases(db_session=db_session)
    uc.verify_access_token(access_token=token)