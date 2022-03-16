from fastapi import APIRouter, Depends, status, HTTPException, Response

from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import utils as utils
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

from .. import database, schema, model, Oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid Credentials 'email'")

    if not pwd_context.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid credential"
        )

    access_token = Oauth2.create_access_token(data= {"user_id": user.id})

    return {"access_token": access_token, "token_type":"bearer"}

