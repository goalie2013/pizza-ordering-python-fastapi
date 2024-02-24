from fastapi import APIRouter
from models import User, Order
import schemas

# 'tags' parameter helps organize API in /docs (Swagger UI)
order_router = APIRouter(
    prefix='/orders',
    tags=['orders']
)

@order_router.get("/")
async def hello():
    return {"message": "Hello Order World!"}
