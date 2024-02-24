from fastapi import status, APIRouter
from fastapi.exceptions import HTTPException
from database import Session, engine
from schemas import UserSchema, UserCreate
from models import User
from werkzeug.security import generate_password_hash


session = Session(bind=engine)

signup_router = APIRouter()


@signup_router.post('/signup', response_model=UserSchema,status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    """
    Check if email, username already in database
    If already exists --> return HTTPException 400 Bad Request
    If not --> create new user
    MUST refresh session to get models.User.id
    """
    #with Session() as session:
    db_email = session.query(User).filter(User.email==user.email).first()

    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Email already registered")
    
    db_username = session.query(User).filter(User.username==user.username).first()

    if db_username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Username already registered")
    
    new_user = User(
        username = user.username,
        email = user.email,
        password = generate_password_hash(user.password),
        is_staff = user.is_staff,
        is_active = True

    )

    print('new user', new_user)
    
    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    finally:
        session.close()
        
    
    print('new user 2', new_user)

    return new_user
