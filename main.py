from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from mysite.database.db import engine, Base
from mysite.api import (
    rooms_http,
    members_http,
    messages_http,
    messages_edit_http,
    attachments_http,
    read_http,
    ws_messages
)
from fastapi.staticfiles import StaticFiles
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title='Academy Chat',
    description='Чат для учителя и студентов',
    version='1.0.0',
    lifespan=lifespan
)

os.makedirs('media', exist_ok=True)
app.mount('/media', StaticFiles(directory='media'), name='media')

app.include_router(rooms_http.router)
app.include_router(members_http.router)
app.include_router(messages_http.router)
app.include_router(messages_edit_http.router)
app.include_router(attachments_http.router)
app.include_router(read_http.router)
app.include_router(ws_messages.router)


@app.get('/')
async def root():
    return {'message': 'Academy Chat работает!'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)