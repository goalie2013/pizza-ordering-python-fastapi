from fastapi import APIRouter
from routers.auth.signup import signup_router
from routers.auth.login import login_router

# 'tags' parameter helps organize API in /docs (Swagger UI)
auth_router = APIRouter(
    prefix='/auth',
    tags=['auth', 'dd']
)

auth_router.include_router(signup_router)
auth_router.include_router(login_router)


@auth_router.get("/")
async def hello():
    return {"message": "Hello World!"}

