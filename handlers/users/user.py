import os
import random
import re
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from states.bot_states import States_Zagotovka
from keyboards.default.bot_button import *
from keyboards.inline.inline_botton import *
from datetime import time, timedelta
from loader import dp, scheduler
from utils.db_api.DB_functions import FuncM, My_Order
from utils.jsonparser.parser import *

import time
from datetime import datetime


@dp.message_handler(state=States_Zagotovka.user_menu, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text == user_bat[0]:
        await States_Zagotovka.week_state.set()
        await message.answer(f"Выберите ресторан для доставки", reply_markup=add_button(get_rests()))
        await States_Zagotovka.reminder_state.set()

    elif message.text == user_bat[1]:
        await States_Zagotovka.add_friend.set()
        await message.answer('Выберете действие', reply_markup=add_button(friend_button))

    elif message.text == user_bat[2]:
        # await States_Zagotovka.aim.set()
        await message.answer('Тут будет история заказов')
        await message.answer(f"Меню пользователя:", reply_markup=add_button(user_bat))
    # else:
    #     await message.answer(f"Что-то пошло не так...")


@dp.message_handler(state=States_Zagotovka.reminder_state, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text in run_zakaz:
        await message.answer('menu', reply_markup=add_button(My_Order.main(message.chat.id)+back_but))
        await States_Zagotovka.sostavlenie_predvaritelnogo.set()
    else:
        await message.answer('Сообщение с предложением откушать отправлено по Вашим друзьям)')
        friends = FuncM.get_friends_smart(message.chat.id)
        msg = ''
        if friends == ['']:
                await message.answer('Ваш список друзей пуст')
                await message.answer(f"Меню пользователя:", reply_markup=add_button(user_bat))
                await States_Zagotovka.user_menu.set()
        else:
            for i in range(len(friends)):
                print(FuncM.get_username_by_id1(int(friends[i])))
                msg = msg + f'{FuncM.get_username_by_id1(friends[i])} : ❌'+'\n'
            My_Order.POST_REST(message.chat.id, message.text)
            await message.answer(f'Готовность друзей:\n{msg}')
            for i in friends:
                await dp.bot.send_message(int(i), f"Хотите заказать еду из '{message.text}'\nИнициатор : {message.from_user.full_name}",reply_markup=add_button(priglos))
                state1 = dp.current_state(chat=int(i), user=int(i))
                await state1.set_state(States_Zagotovka.yes_no)
            
            await message.answer(f"Как только все друзья будут готовы, мы Вас опопвестим...", reply_markup=add_button(run_zakaz))
        

@dp.message_handler(state=States_Zagotovka.yes_no, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text == priglos[0]:
        await message.answer('Можете сделать заказ:',reply_markup=add_button(My_Order.main(message.chat.id)))
        await States_Zagotovka.sostavlenie_predvaritelnogo.set()
    if message.text == priglos[1]:
        My_Order.delString(message.chat.id)
        await message.answer('Если Вас не устраивает ресторан, можете организовать заказ из другого рестрана.')
        await message.answer(f"Меню пользователя:", reply_markup=add_button(user_bat))
        await States_Zagotovka.user_menu.set()

# @dp.message_handler(state=States_Zagotovka.zakaz, content_types=types.ContentTypes.ANY)
# async def bot_echo_all(message: types.Message, state: FSMContext):
#     if message.text == burger[0]:
#         await message.answer('Заказ принят но полностью я это реализую когда созвонюсь с Серегой...')
#         await message.answer(f"Меню пользователя:", reply_markup=add_button(user_bat))
#         await States_Zagotovka.user_menu.set()


@dp.message_handler(state=States_Zagotovka.sostavlenie_predvaritelnogo, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    try: 
        if message.text in My_Order.getListProducts(message.chat.id):
            My_Order.POST_PATH(message.chat.id, message.text)
            if My_Order.main(message.chat.id)[3] == '':
                with open(f'/mnt/c/hakaton/zona1/utils/images/1.jpg', 'rb') as photo:
                    await message.answer_photo(photo)
                    photo.close()
            else:
                with open(f'/mnt/c/hakaton/zona1/utils/{My_Order.main(message.chat.id)[3]}', 'rb') as photo:
                    await message.answer_photo(photo)
                    photo.close()
            # print(f'/utils/{My_Order.main(message.chat.id)[3]}')
            # await message.answer_photo(f'/utils/{My_Order.main(message.chat.id)[3]}')
            await message.answer(f'{message.text}\n{My_Order.main(message.chat.id)[0]}\n{My_Order.main(message.chat.id)[1]}\n{My_Order.main(message.chat.id)[2]}',reply_markup=add_button(forward_but+back_but))

        elif message.text == back_but[0]:
            My_Order.DEL_PATH(message.chat.id, message.text)
            await message.answer('menu', reply_markup=add_button(My_Order.main(message.chat.id)+back_but))
        elif message.text == forward_but[0]:
            My_Order.POST_PRELIMINARY(message.chat.id)
            My_Order.DEL_PATH_REST(message.chat.id)
            msg=''
            for i in My_Order.GET_PR(message.chat.id):
                # i = i.split('|')
                msg += '\n'+f'`{i}`'
            await message.answer(f'Подтвердите заказ:{msg}\n\nЦена заказа: {My_Order.getPrice(message.chat.id)}', reply_markup=add_button(podtverdit_ili_net),parse_mode='MarkDown')
            await States_Zagotovka.podtverdit_ili_net.set()
    except:
        if message.text == back_but[0]:
            My_Order.DEL_PATH_REST(message.chat.id)
            try:
                My_Order.POST_PATH(message.chat.id, message.text)
                await message.answer('menu', reply_markup=add_button(My_Order.main(message.chat.id)+back_but))
            except:
                
                await message.answer('Желаете отказаться от заказа?', reply_markup=add_button(yes_no))
                await States_Zagotovka.blya.set()
        # elif message.text == forward_but[0]:

        else:
            My_Order.POST_PATH(message.chat.id, message.text)
            await message.answer('menu', reply_markup=add_button(My_Order.main(message.chat.id)+back_but))

@dp.message_handler(state=States_Zagotovka.podtverdit_ili_net, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text == podtverdit_ili_net[0]:
        My_Order.POST_FINAL(message.chat.id)
        await message.answer('Спасибо за Ваш заказ, очень скоро Вам придет сумма перевода и номер счета вашего коллеги. Вы и сами знаете что с этим делать')
        await message.answer(f"Меню пользователя:", reply_markup=add_button(user_bat))
        await States_Zagotovka.user_menu.set()
    elif message.text == podtverdit_ili_net[1]:
        My_Order.DEL_PATH_REST(message.chat.id)
        await message.answer('menu', reply_markup=add_button(My_Order.main(message.chat.id)+back_but))
        await States_Zagotovka.sostavlenie_predvaritelnogo.set()
    elif message.text == podtverdit_ili_net[2]:
        await message.answer('Пришлите нам продукт который желаете удалить\n(Можете скопировать название нажав на продукт)')
        await States_Zagotovka.del_prod.set()

@dp.message_handler(state=States_Zagotovka.del_prod, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    try:
        My_Order.DEL_PRODUCT(message.chat.id, message.text)
        await message.answer('Продукт успешно удален')
        msg=''
        for i in My_Order.GET_PR(message.chat.id):
            msg += '\n'+f'`{i[:-1]}`'
        await message.answer(f'Подтвердите заказ:{msg}\n\nЦена заказа: {My_Order.getPrice(message.chat.id)}', reply_markup=add_button(podtverdit_ili_net),parse_mode='MarkDown')
        await States_Zagotovka.podtverdit_ili_net.set()
    except:
        await message.answer('Некорректно указан продукт')
        msg=''
        for i in My_Order.GET_PR(message.chat.id):
            msg += '\n'+f'`{i[:-1]}`'
        await message.answer(f'Подтвердите заказ:{msg}\n\nЦена заказа: {My_Order.getPrice(message.chat.id)}', reply_markup=add_button(podtverdit_ili_net),parse_mode='MarkDown')
        await States_Zagotovka.podtverdit_ili_net.set()


@dp.message_handler(state=States_Zagotovka.blya, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text == yes_no[0]:
        My_Order.delString(message.chat.id)
        await message.answer(f"Меню пользователя:", reply_markup=add_button(user_bat))
        await States_Zagotovka.user_menu.set()
    elif message.text == yes_no[1]:
        My_Order.DEL_PATH_REST(message.chat.id)
        await message.answer('menu', reply_markup=add_button(My_Order.main(message.chat.id)+back_but))
        await States_Zagotovka.sostavlenie_predvaritelnogo.set()

@dp.message_handler(state=States_Zagotovka.add_friend, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    if message.text == friend_button[0]:
        await message.answer('Напишите нам username пользователя ( Например : Example123 )')
        await States_Zagotovka.add_friend1.set()
    elif message.text == friend_button[1]:
        await message.answer('Напишите нам username пользователя ( Например : Example123 )')
        friends = FuncM.get_friends(message.chat.id)
        msg = ''
        print(friends)
        if friends == ['']:
            await message.answer('Ваш список друзей пуст')
            await message.answer(f"Меню пользователя:", reply_markup=add_button(user_bat))
            await States_Zagotovka.user_menu.set()
        else:
            for i in range(len(friends)):
                print(FuncM.get_username_by_id1(int(friends[i])))
                msg = msg + f'`{FuncM.get_username_by_id1(friends[i])}`'+'\n'
            await message.answer(f'Список Ваших друзей:\n{msg}', parse_mode='MarkDown')
            await States_Zagotovka.delite_friend.set()
    elif message.text == friend_button[2]:
        friends = FuncM.get_friends(message.chat.id)
        msg = ''
        if friends == ['']:
            await message.answer('Ваш список друзей пуст')
            await message.answer(f"Меню пользователя:", reply_markup=add_button(user_bat))
            await States_Zagotovka.user_menu.set()
        else:
            for i in range(len(friends)):
                print(FuncM.get_username_by_id1(int(friends[i])))
                msg = msg + f'`{FuncM.get_username_by_id1(friends[i])}`'+'\n'
            await message.answer(f'Список Ваших друзей:\n{msg}', parse_mode='MarkDown')
            await message.answer(f"Меню пользователя:", reply_markup=add_button(user_bat))
            await States_Zagotovka.user_menu.set()


@dp.message_handler(state=States_Zagotovka.add_friend1, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    # await dp.bot.send_message(FuncM.get_username_by_id(message.text), f'Вам пишла заявка в друзья от {message.chat.username}',reply_markup=add_button(priglos))
    # state1 = dp.current_state(chat=FuncM.get_username_by_id(message.text), user=FuncM.get_username_by_id(message.text))
    # await state1.set_state(States_Zagotovka.podtverzdenie_friend)
    try:
        FuncM.Friends(message.chat.id, message.text)
        await message.answer('Друг добавлен')
    except:
        await message.answer('Данного пользователя не пользовался ботом, о нем нет данных')
    await message.answer(f"Меню пользователя:", reply_markup=add_button(user_bat))
    await States_Zagotovka.user_menu.set()


@dp.message_handler(state=States_Zagotovka.add_friend, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    # if message.text in USERNAME_LIST():
    #     ADD_FRIEND(message.chat.id)
    #     await message.answer(f'Пользователь {message.chat.id} добавлен в список друзей')
    # else:
    #     await message.answer(f'В моей базе не найдено пользователей с данным именем')
    await message.answer(f"Меню пользователя:", reply_markup=add_button(user_bat))
    await States_Zagotovka.user_menu.set()


@dp.message_handler(state=States_Zagotovka.delite_friend, content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    FuncM.delete_friends(message.chat.id, message.text)
    await message.answer('Друг удален')
    await message.answer(f"Меню пользователя:", reply_markup=add_button(user_bat))
    await States_Zagotovka.user_menu.set()
