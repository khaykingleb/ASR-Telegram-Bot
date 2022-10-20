"""Telegram bot."""

import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import Executor

from .. import cfg

loop = asyncio.get_event_loop()
bot = Bot(cfg.TG_BOT_TOKEN, loop=loop)
dp = Dispatcher(bot, storage=MemoryStorage())
executor = Executor(dp, skip_updates=True)
