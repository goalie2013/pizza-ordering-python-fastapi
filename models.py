from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship, Mapped

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship('Order', back_populates='user')  # back_populates Order.user

    def __repr__(self):
        return f"User id {self.id}: {self.username} {self.is_active} {self.is_staff}"

class Order(Base):

    ORDER_STATUSES = (
        ('PENDING', 'pending'),
        ('IN-TRANSIT', 'in-transit'),
        ('DELIVERED', 'delivered'),
    )

    PIZZA_SIZES = (
        ('SM', 'small'),
        ('M', 'medium'),
        ('LG', 'large'),
        ('XL', 'extra large'),
    )

    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    order_status = Column(ChoiceType(choices=ORDER_STATUSES), default='PENDING')
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES))
    toppings = Column(String(30))
    user_id = Column(Integer, ForeignKey('users.id'))
    user: Mapped["User"] = relationship('User', back_populates='orders') # back_populates User.orders

    def __repr__(self):
        return f"Order {self.id}"