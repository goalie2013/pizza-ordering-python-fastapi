from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
import schemas
from mock import fake_users_db, fake_decode_token, fake_hash_password


# 'tags' parameter helps organize API in /docs (Swagger UI)
router = APIRouter(
    prefix='/user',
    tags=['user']
)

"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# receive a token as a str from sub-dependency oauth2_scheme
# str -> schemas.User
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    print('user: ', user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect username or password")
    user = schemas.UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Incorrect username or password")
    
    return {"access_token": user.username, "token_type": "bearer"}

# Inject current user
@router.get("/me")
async def read_users_me(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    print('current_user: ', current_user)
    return current_user



@user_router.get("/")
async def hello(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
"""