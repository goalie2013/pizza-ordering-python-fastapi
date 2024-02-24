from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str
    is_staff: bool = False
    is_active: bool = False

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int

    class Config:
        from_attributes=True
        json_schema_extra={
            "example":{
                "id": 1,
                "username": "john doe",
                "email": "jdoe@gmail.com",
                "is_staff": False,
                "is_active": True
            }
        }

class UserInDBSchema(UserSchema):
    hashed_password: str

"""
class SignUpModel(BaseModel):
    id: int
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        from_attributes=True
        json_schema_extra={
            "example":{
                "username": "john doe",
                "email": "jdoe@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }
"""

class OrderBase(BaseModel):
    quantity: int
    order_status: str = "PENDING"
    pizza_size: str = "small"
    toppings: str

class Order(OrderBase):
    id: int
    user_id: int
    #user: Mapped["User"] = relationship('User', back_populates='orders')

    class Config:
        from_attributes=True
        json_schema_extra={
            "example": {
                "quantity": 2,
                "order_status": "PENDING",
                "pizza_size": "medium",
                "toppings": "sausage",
            }
        }


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: str | None = None