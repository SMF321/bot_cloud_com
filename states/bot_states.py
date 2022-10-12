import statistics
from aiogram.dispatcher.filters.state import State, StatesGroup


class States_Zagotovka (StatesGroup):
    admin_menu = State()
    text_rassilka = State()
    if_png_Jpg = State()
    png_jpg = State()
    add_quasion = State()
    add_quasion_if_png_Jpg = State()
    add_quasion_png_Jpg = State()
    answers = State()
    yes_no = State()
    add_mood = State()
    add_mood1 = State()
    zakaz = State()
    sostavlenie_predvaritelnogo = State()
    blya = State()
    podtverdit_ili_net = State()
    del_prod = State()


    ######################
    user_menu = State()
    aim = State()
    time_state = State()
    time_state1 = State()
    week_state = State()
    statistics = State()
    game = State()
    add_friend = State()
    add_friend1 = State()
    podtverzdenie_friend = State()
    check_knowledge = State()
    true_false_answer = State()
    feedback = State()
    reminder_state = State()
    delite_reminder = State()
    delite_friend = State()
    feedback_testing = State()
    feedback_testing1 = State()
    feedback_testing2 = State()
    feedback_testing3 = State()
    feedback_testing4 = State()
    feedback_testing5 = State()
    #####################
    priglos = State()
    zero = State()
    vopros_otvet = State()


    ######################
    vibor_testa = State()

    competition_wopros = State()
    competition_answer = State()
    competition_varianti_otveta = State()
    competition_ves = State()

    test_wopros = State()
    test_answer = State()
    test_varianti_otveta = State()
    test_ves = State()
    test_tema = State()
    #####################
    mood_msg = State()