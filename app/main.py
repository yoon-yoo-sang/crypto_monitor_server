from fastapi import FastAPI

from app.controllers import user_controller, coin_controller

app = FastAPI()

app.include_router(user_controller.router, prefix="/api/v1")
app.include_router(coin_controller.router, prefix="/api/v1")
