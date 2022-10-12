from loader import dp, scheduler
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import ADMINS
from keyboards.default.bot_button import *
from utils.db_api.DB_functions import *

from states.bot_states import States_Zagotovka

async def send_message_to_admin(dp: Dispatcher):
    await dp.bot.send_message(ADMINS[0],'hi')

def start_shedule(massive_remindes):
    try:
        scheduler.add_job(massive_remindes[...], 'cron', massive_remindes[...], hour=massive_remindes[...], minute=massive_remindes[...], id=massive_remindes[...])
    except:
        pass


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    
    
    try:
        FuncM.POST(message.chat.id,message.chat.username)
    except:
        pass
    await message.answer(f"Привет, {message.from_user.full_name}!\nНапишите мне Ваше ФИО, это понадобится нам в дальнейшем для удобства)")
    await States_Zagotovka.aim.set()
    # await message.answer(f"Меню юзера:",reply_markup=add_button(user_bat))
    print(message.chat.id)


@dp.message_handler(state=States_Zagotovka.aim, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, ):
    # FuncM.update_aim(message.chat.id,message.text)
    await message.answer(f"Меню пользователя:",reply_markup=add_button(user_bat))
    await States_Zagotovka.user_menu.set()