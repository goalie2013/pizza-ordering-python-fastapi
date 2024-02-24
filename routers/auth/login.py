from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from schemas import TokenSchema, TokenDataSchema, UserInDBSchema, UserSchema
from mock import fake_users_db, fake_decode_token, fake_hash_password, get_user, verify_password
from jose import JWTError, jwt
from dotenv import load_dotenv, dotenv_values

#TODO: use fake db for quick testing (like architecture book)

login_router = APIRouter()

load_dotenv()
config = dotenv_values(".env")

# tokenUrl is the URL in our API
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def authenticate_user(username: str, password: str):
    """
    Check if form username is in database. \n
    If yes, then check form password against hashed password (from db) \n
    If succeeds, return models.User
    """
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        print("PASSWORDS DO NOT MATCH")
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config["SECRET_KEY"], algorithm=config["ALGORITHM"])
    return encoded_jwt


@login_router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)]) -> TokenSchema:
    print('login()')
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(config["ACCESS_TOKEN_EXPIRE_MINUTES"]))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return TokenSchema(access_token=access_token, token_type="bearer")



#TODO: return UserSchema with no password or hashed password as 'user' 
#(bc will be returned as response to client-side)
# str -> schemas.User
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """ 
    Receive a JWT token as a str from OAuth2 and decode it
    """
    print('get_current_user()')
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, config["SECRET_KEY"], algorithms=[config["ALGORITHM"]])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataSchema(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user


# Inject current user
@login_router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: Annotated[UserSchema, Depends(get_current_user)]):
    print('current_user: ', current_user)
    return current_user
