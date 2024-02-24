from fastapi import FastAPI
from routers.auth.auth_routes import auth_router
from routers.order_routes import order_router
from routers import user_routes

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(user_routes.router)
