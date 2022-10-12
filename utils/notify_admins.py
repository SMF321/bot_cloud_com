import asyncio
from datetime import datetime
import logging

from aiogram import Dispatcher, Bot

from data.config import ADMINS

from loader import scheduler

from utils.db_api.DB_functions import *

async def send_message_to_admin(dp: Dispatcher):
    await dp.bot.send_message(ADMINS[0],'hi')

async def send_msg_by_remember(dp: Dispatcher):
    await dp.bot.send_message(898544428, 'напоминание')



async def send_remember(dp: Dispatcher):
    for i in range(len(FuncM.Get_info(898544428)[1])):
        scheduler.add_job(asyncio.create_task(send_msg_by_remember(dp)),\
        'cron', day_of_week=FuncM.Get_info(898544428)[1][i],\
        hour=int(FuncM.Get_info(898544428)[0][i].split(':')[0]),\
        minute=int(FuncM.Get_info(898544428)[0][i].split(':')[1]),\
        id=FuncM.Get_info(898544428)[2][i])

async def start_remember(dp):
    while True:
        await send_remember(dp)
        await asyncio.sleep(15)
    

async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "/start")

        except Exception as err:
            logging.exception(err)
    
    # asyncio.create_task(start_remember(dp))
    