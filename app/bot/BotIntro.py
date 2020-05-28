import app.bot.config
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.bot.TCalendar import create_calendar, calendar_callback

bot = telebot.TeleBot(app.bot.config.token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Начинаем работу /start')
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Добавить задачу', callback_data='add_new_task'))
    keyboard.add(InlineKeyboardButton('Мои задачи', callback_data='show_tasks'))
    bot.send_message(message.chat.id, 'Выберите дальнейшее действие', reply_markup=keyboard)


@bot.message_handler(commands='calendar')
def get_calendar(message):
    keyboard = create_calendar()
    bot.send_message(message.chat.id, 'Выберите дату', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(query):
    data = query.data
    if data in get_tasks_dict:
        func = get_tasks_dict[data]
        func(query.message)
    else:
        (ok, date) = calendar_callback(bot, query)
        if ok:
            bot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id)
            bot.send_message(query.message.chat.id, f'Выбрана датa = {date}')


@bot.message_handler(content_types=['text'])
def send_text(message):
    message.text = message.text.lower()
    if message.text == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text == 'как дела старина':
        bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
    else:
        bot.send_message(message.chat.id, message.text)


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)


# --------------------------------------------------------
@bot.message_handler(content_types=['sticker'])
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


@bot.message_handler(func=lambda message: True)
def get_all_tasks(message):
    bot.reply_to(message, 'выполняется get_all_tasks')


@bot.message_handler(func=lambda message: True)
def get_today_tasks(message):
    bot.reply_to(message, 'выполняется get_today_tasks')


@bot.message_handler(func=lambda message: True)
def get_tomorrow_tasks(message):
    bot.reply_to(message, 'выполняется get_tomorrow_tasks')


if __name__ == "__main__":
    get_tasks_dict = {
        'get_home': get_home,
        'add_new_task': add_new_task,
        'show_tasks': show_tasks,
        'get_all_tasks': get_all_tasks,
        'get_today_tasks': get_today_tasks,
        'get_tomorrow_tasks': get_tomorrow_tasks
    }
    bot.polling()
