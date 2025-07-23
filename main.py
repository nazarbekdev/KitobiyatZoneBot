from aiogram import Dispatcher
from handlers import start, results, rating, invite, prizes, admin
from database.db import setup_database


def setup_routers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(results.router)
    dp.include_router(rating.router)
    dp.include_router(invite.router)
    dp.include_router(prizes.router)
    dp.include_router(admin.router)


def main_setup():
    setup_database()
