"""API router for Telegram."""

from aiogram import types
from fastapi import APIRouter

from .. import cfg
from ..bot.handlers import bot, dp

router = APIRouter()


@router.on_event("startup")
async def on_startup() -> None:  # NOQA
    await bot.set_webhook(cfg.TG_BOT_URL, drop_pending_updates=True)


@router.on_event("shutdown")
async def on_shutdown() -> None:  # NOQA
    await bot.delete_webhook(drop_pending_updates=True)


@router.post("/bot/{}".format(cfg.TG_BOT_TOKEN), include_in_schema=False)
async def tg_bot_webhook(update: dict):  # NOQA
    tg_update = types.Update(**update)
    await dp.process_update(tg_update)
