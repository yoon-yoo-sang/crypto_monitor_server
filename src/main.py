import uvicorn
from fastapi import FastAPI

from src.controllers import user_controller, coin_controller

app = FastAPI()

app.include_router(user_controller.router, prefix="/api/v1")
app.include_router(coin_controller.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
