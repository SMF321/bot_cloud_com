from turtle import back
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_bat = ['Массовая расcылка информации','Добавить/удалить задачу','Просмотреть отзывы','Добавить вопросы интеллектуальной рефлексии']
user_bat = ['Организовать доставку','Добавить в друзья/Удалить из друзей/Просмотр друзей','История заказов']
week = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота','Воскресенье']
reminder_menu = ['Рестораны будут подтягиваться из json','Рестораны будут подтягиваться из json','Рестораны будут подтягиваться из json']
friend_button = ['Добавить в друзья','Удалить из друзей','Мои друзья']
yes_no = ['Да','Нет']
priglos = ['Принять','Отклонить']
test_vopros = ["<class 'bool'>","<class 'tuple'>","<class 'str'>"]
mood_bat = ['positive','negative','neutral']
back_but = ['Назад']
forward_but = ['Добавить в заказ']
burger = ['Бургер','Бургер','Бургер']
run_zakaz = ['Приступить к заказу']
podtverdit_ili_net = ['Подтверждаю', 'Сделать заказ еще','Удалить продукт из заказа']

def add_button(mass):
    buttons = ReplyKeyboardMarkup(True,True,True)
    for i in range(len(mass)):
        keyboad = KeyboardButton(mass[i])
        buttons.add(keyboad)
    return buttons