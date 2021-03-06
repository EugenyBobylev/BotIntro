import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot import chatstate
from app.bot.TCalendar import create_calendar, calendar_callback, date_from_str
from app.bot.bot_stack import BotStack
from app.bot.model import TodoTask

bot = telebot.TeleBot('1019358164:AAFGDWu1zn-nJyDKlKEFzFcuWBgYP-f30-Y')
stack = BotStack()
data = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    show_home_menu(message.chat.id)


@bot.message_handler(commands=['calendar'])
def show_calendar(message):
    keyboard = create_calendar()
    msg = bot.send_message(message.chat.id, 'Выберите дату', reply_markup=keyboard)
    push(msg)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(query):
    qdata = query.data
    if qdata in get_tasks_dict:
        func = get_tasks_dict[qdata]
        func(query.message)
    elif chatstate.get_chat_state(query.message.chat.id) == 'add_task_date':
        (ok, date) = calendar_callback(bot, query)
        if ok:
            #bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id)
            pop(query.message.chat.id)
            pop(query.message.chat.id)
            data["срок"] = date
            msg = bot.send_message(query.message.chat.id, f'Срок = {data["срок"]}')
            push(msg)
            confirm_task(msg.chat.id)


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


def get_home(message):
    cnt = stack.all_count()
    clear_messages(message.chat.id)
    show_home_menu(message.chat.id)


# ********************** Новая задача **********************************************************************************
def add_new_task(message):
    data = {}
    clear_messages(message.chat.id)
    add_task_descr(message)


def add_task_descr(message):
    pop(message.chat.id)
    chatstate.set_chat_state(message.chat.id, 'add_task_descr')
    msg = bot.send_message(message.chat.id, 'Введите описание задачи:')
    push(msg)


@bot.message_handler(func=lambda message: chatstate.get_chat_state(message.chat.id) == 'add_task_descr')
def set_task_descr(message):
    data["задача"] = message.text
    push(message)  # ответ пользователя в стек
    clear_messages(message.chat.id)
    msg = bot.send_message(message.chat.id, f'Задача = "{data["задача"]}"')
    push(msg)
    add_task_date(msg)


def add_task_date(message):
    chatstate.set_chat_state(message.chat.id, 'add_task_date')
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Календарь', callback_data='show_calendar'))
    msg = bot.send_message(message.chat.id, 'Введите срок выполнения задачи', reply_markup=keyboard)
    push(msg)


@bot.message_handler(func=lambda message: chatstate.get_chat_state(message.chat.id) == 'add_task_date')
def set_task_date(message):
    data["срок"] = date_from_str(message.text)
    push(message)
    pop(message.chat.id)
    pop(message.chat.id)
    msg = bot.send_message(message.chat.id, f'Срок = {data["срок"]}')
    push(msg)
    confirm_task(msg.chat.id)


def confirm_task(chat_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton('Изменить', callback_data='add_task_descr'),
        InlineKeyboardButton('Сохранить', callback_data='save_task'),
        InlineKeyboardButton('Отмена', callback_data='get_home')
    )
    msg = bot.send_message(chat_id, f'Выберите действие', reply_markup=keyboard)
    push(msg)


def save_task(message):
    task = TodoTask.create(data)
    print(task)
    clear_messages(message.chat.id)
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton('В начало', callback_data='get_home'),
        InlineKeyboardButton('Добавить задачу', callback_data='add_new_task')
    )
    msg = bot.send_message(message.chat.id, "Задача сохранена", reply_markup=keyboard)
    push(msg)


# *******************************my tasks **************************************************
def show_tasks(message):
    clear_messages(message.chat.id)
    show_tasks_menu(message.chat.id)


def get_all_tasks(message):
    msg = bot.reply_to(message, 'выполняется get_all_tasks')
    push(msg)


def get_today_tasks(message):
    msg = bot.reply_to(message, 'выполняется get_today_tasks')
    push(msg)


def get_tomorrow_tasks(message):
    msg = bot.reply_to(message, 'выполняется get_tomorrow_tasks')
    push(msg)


# **************** menu ********************************************************
def show_home_menu(chat_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Добавить задачу', callback_data='add_new_task'))
    keyboard.add(InlineKeyboardButton('Мои задачи', callback_data='show_tasks'))
    msg = bot.send_message(chat_id, 'Выберите дальнейшее действие', reply_markup=keyboard)
    push(msg)


def show_tasks_menu(chat_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Все не завершенные', callback_data='get_all_tasks'))
    keyboard.add(InlineKeyboardButton('Все на сегодня', callback_data='get_today_tasks'))
    keyboard.add(InlineKeyboardButton('Все на завтра', callback_data='get_tomorrow_tasks'))
    keyboard.add(InlineKeyboardButton('Вернуться', callback_data='get_home'))
    msg = bot.send_message(chat_id, 'Выберите', reply_markup=keyboard)
    push(msg)


# ************************** stack methods ***************************************************
def clear_messages(chat_id):
    while stack.count(chat_id) > 0:
        pop(chat_id)
        # bot.delete_message(chat_id, msg_id)


def push(message):
    stack.push(message.chat.id, message.message_id)


def pop(chat_id):
    msg_id = stack.pop(chat_id)
    if msg_id is not None:
        bot.delete_message(chat_id, msg_id)


if __name__ == '__main__':
    get_tasks_dict = {
        'get_home': get_home,
        'add_new_task': add_new_task,
        'add_task_descr': add_task_descr,
        'add_task_date': add_task_date,
        'save_task': save_task,
        'show_calendar': show_calendar,
        'show_tasks': show_tasks,
        'get_all_tasks': get_all_tasks,
        'get_today_tasks': get_today_tasks,
        'get_tomorrow_tasks': get_tomorrow_tasks
    }

    bot.polling()
