import schemas
from models import User
from database import Session
from werkzeug.security import check_password_hash, generate_password_hash

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}




def fake_hash_password(password: str):
    return "fakehashed" + password


def _get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return schemas.UserInDB(**user_dict)

def fake_decode_token(token):
    user = _get_user(fake_users_db, token)
    return user

##### REAL HELPER METHODS BELOW

def get_user(username: str):
    print('get_user()')
    with Session() as session:
        db_username = session.query(User).filter(User.username==username).first()
        if db_username is None:
            return False
        print('db_username', db_username)
        return db_username


def verify_password(password: str, hashed_password: str) -> bool:
    return check_password_hash(hashed_password, password)