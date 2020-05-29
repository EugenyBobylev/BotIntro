import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.bot.bot_stack import BotStack

bot = telebot.TeleBot('1019358164:AAFGDWu1zn-nJyDKlKEFzFcuWBgYP-f30-Y')
stack = BotStack()


@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.send_message(message.chat.id, 'Начинаем работу /start')
    push(msg)
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Добавить задачу', callback_data='add_new_task'))
    keyboard.add(InlineKeyboardButton('Мои задачи', callback_data='show_tasks'))
    bot.send_message(message.chat.id, 'Выберите дальнейшее действие', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(query):
    data = query.data
    if data in get_tasks_dict:
        func = get_tasks_dict[data]
        func(query.message)


@bot.message_handler(content_types=['text'])
def send_text(message):
    clear_messages(message.chat.id)
    message.text = message.text.lower()
    if message.text == 'text':
        bot.send_message(message.chat.id, 'Привет')
    elif message.text == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text == 'как дела старина':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
    else:
        bot.delete_message(message.chat.id, message.message_id)


def clear_messages(chat_id):
    while stack.count(chat_id) > 0:
        msg_id = pop(chat_id)
        bot.delete_message(chat_id, msg_id)


@bot.message_handler(func=lambda message: True)
def get_home(message):
    bot.reply_to(message, 'выполняется get_home')


@bot.message_handler(content_types=['sticker'])
def add_new_task(message):
    bot.reply_to(message, 'выполняется add_new_task')


@bot.message_handler(func=lambda message: True)
def show_tasks(message):
    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton('Все не завершенные', callback_data='get_all_tasks')),
    keyboard.add(InlineKeyboardButton('Все на сегодня', callback_data='get_today_tasks')),
    keyboard.add(InlineKeyboardButton('Все на завтра', callback_data='get_tomorrow_tasks'))
    keyboard.add(InlineKeyboardButton('Вернуться', callback_data='get_home'))

    bot.send_message(message.chat.id, 'Выберите', reply_markup=keyboard)
    bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id)



def push(message):
    stack.push(message.chat.id, message.message_id)


@bot.message_handler(func=lambda message: True)
def get_all_tasks(message):
    bot.reply_to(message, 'выполняется get_all_tasks')


@bot.message_handler(func=lambda message: True)
def get_today_tasks(message):
    bot.reply_to(message, 'выполняется get_today_tasks')


@bot.message_handler(func=lambda message: True)
def get_tomorrow_tasks(message):
    bot.reply_to(message, 'выполняется get_tomorrow_tasks')


def pop(chat_id):
    message_id = stack.pop(chat_id)
    return message_id


if __name__ == '__main__':
    get_tasks_dict = {
        'get_home': get_home,
        'add_new_task': add_new_task,
        'show_tasks': show_tasks,
        'get_all_tasks': get_all_tasks,
        'get_today_tasks': get_today_tasks,
        'get_tomorrow_tasks': get_tomorrow_tasks
    }
    bot.polling()
