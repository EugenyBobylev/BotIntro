import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot import chatstate
from app.bot.TCalendar import create_calendar, calendar_callback, date_from_str
from app.bot.bot_stack import BotStack

bot = telebot.TeleBot('1019358164:AAFGDWu1zn-nJyDKlKEFzFcuWBgYP-f30-Y')
stack = BotStack()


@bot.message_handler(commands=['start'])
def start_message(message):
    show_home_menu(message.chat.id)


@bot.message_handler(commands=['calendar'])
def show_calendar(message):
    keyboard = create_calendar()
    bot.send_message(message.chat.id, 'Выберите дату', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(query):
    data = query.data
    if data in get_tasks_dict:
        func = get_tasks_dict[data]
        func(query.message)
    elif chatstate.get_chat_state(query.message.chat.id) == 'add_task_date':
        (ok, date) = calendar_callback(bot, query)
        if ok:
            bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id)
            bot.send_message(query.message.chat.id, f'Выбрана датa = {date}')


# @bot.message_handler(content_types=['text'])
def send_text(message):
    message.text = message.text.lower()
    if message.text == 'text':
        bot.send_message(message.chat.id, 'Привет')
    elif message.text == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    else:
        bot.delete_message(message.chat.id, message.message_id)


# @bot.message_handler(func=lambda message: True)
def get_home(message):
    show_home_menu(message.chat.id)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


# ********************** Новая задача **********************************************************************************
def add_new_task(message):
    # show_new_task_menu(message.chat.id)
    add_task_descr(message)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


def add_task_descr(message):
    chatstate.set_chat_state(message.chat.id, 'add_task_descr')
    bot.send_message(message.chat.id, 'Введите описание задачи:')


@bot.message_handler(func=lambda message: chatstate.get_chat_state(message.chat.id) == 'add_task_descr')
def set_task_descr(message):
    msg = bot.send_message(message.chat.id, f'Descr = "{message.text}"')
    add_task_date(msg)


def add_task_date(message):
    chatstate.set_chat_state(message.chat.id, 'add_task_date')
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Выбрать дату', callback_data='show_calendar'))
    bot.send_message(message.chat.id, 'Введите срок выполнения задачи', reply_markup=keyboard)


@bot.message_handler(func=lambda message: chatstate.get_chat_state(message.chat.id) == 'add_task_date')
def set_task_date(message):
    date = date_from_str(message.text)
    bot.send_message(message.chat.id, f'Выбрана датa = {date}')


# *********************************************************************************
# @bot.message_handler(func=lambda message: True)
def show_tasks(message):
    show_tasks_menu(message.chat.id)
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


# @bot.message_handler(func=lambda message: True)
def get_all_tasks(message):
    bot.reply_to(message, 'выполняется get_all_tasks')


# @bot.message_handler(func=lambda message: True)
def get_today_tasks(message):
    bot.reply_to(message, 'выполняется get_today_tasks')


# @bot.message_handler(func=lambda message: True)
def get_tomorrow_tasks(message):
    bot.reply_to(message, 'выполняется get_tomorrow_tasks')


# **************** menu ********************************************************
def show_home_menu(chat_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Добавить задачу', callback_data='add_new_task'))
    keyboard.add(InlineKeyboardButton('Мои задачи', callback_data='show_tasks'))
    bot.send_message(chat_id, 'Выберите дальнейшее действие', reply_markup=keyboard)


def show_tasks_menu(chat_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Все не завершенные', callback_data='get_all_tasks'))
    keyboard.add(InlineKeyboardButton('Все на сегодня', callback_data='get_today_tasks'))
    keyboard.add(InlineKeyboardButton('Все на завтра', callback_data='get_tomorrow_tasks'))
    keyboard.add(InlineKeyboardButton('Вернуться', callback_data='get_home'))
    bot.send_message(chat_id, 'Выберите', reply_markup=keyboard)


def show_new_task_menu(chat_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Добавьте описание', callback_data='add_task_descr'))
    keyboard.add(InlineKeyboardButton('Выберете дату', callback_data='add_task_date'))
    bot.send_message(chat_id, 'Новая задача', reply_markup=keyboard)


# *****************************************************************************
def clear_messages(chat_id):
    while stack.count(chat_id) > 0:
        msg_id = pop(chat_id)
        bot.delete_message(chat_id, msg_id)


def push(message):
    stack.push(message.chat.id, message.message_id)


def pop(chat_id):
    message_id = stack.pop(chat_id)
    return message_id


if __name__ == '__main__':
    get_tasks_dict = {
        'get_home': get_home,
        'add_new_task': add_new_task,
        'show_calendar': show_calendar,
        'show_tasks': show_tasks,
        'get_all_tasks': get_all_tasks,
        'get_today_tasks': get_today_tasks,
        'get_tomorrow_tasks': get_tomorrow_tasks,
        'add_task_descr': add_task_descr,
        'add_task_date': add_task_date
    }

    bot.polling()
