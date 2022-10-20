"""Main application."""

from fastapi import FastAPI

from .routers import telegram

app = FastAPI(
    title="ASR API",
    description="ASR minimal working API server",
    version="1.0.0",
    contact={
        "name": "Gleb Khaykin",
        "email": "khaykingleb@gmail.com",
    },
)

app.include_router(telegram.router)
