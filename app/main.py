import uvicorn as uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users, apartments

from app.models.database import database

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # когда приложение запускается устанавливаем соединение с БД
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    # когда приложение останавливается разрываем соединение с БД
    await database.disconnect()


app.include_router(users.router)
app.include_router(apartments.router)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
