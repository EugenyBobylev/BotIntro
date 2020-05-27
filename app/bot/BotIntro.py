import app.bot.config
import calendar
import datetime
import telebot

from app.bot.TCalendar import create_calendar

bot = telebot.TeleBot(app.bot.config.token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


@bot.message_handler(commands=['calendar1'])
def get_calendar1(message):
    bot.send_message(message.chat.id, 'Выберите', reply_markup=create_calendar())


def create_callback_data(action, year, month, day):
    """ Create the callback data associated to each button"""
    return ";".join([action, str(year), str(month), str(day)])


@bot.message_handler(commands='calendar')
def get_calendar(message):
    now = datetime.date.today()
    year = now.year
    month = now.month
    caption1 = f'{calendar.month_name[month]} {year}'

    keyboard = telebot.types.InlineKeyboardMarkup()
    # top
    keyboard.row(
        telebot.types.InlineKeyboardButton(caption1, callback_data='calendar_ignore')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Пн', callback_data='calendar_ignore_mo'),
        telebot.types.InlineKeyboardButton('Вт', callback_data='calendar_ignore_tu'),
        telebot.types.InlineKeyboardButton('Ср', callback_data='calendar_ignore_we'),
        telebot.types.InlineKeyboardButton('Чт', callback_data='calendar_ignore_th'),
        telebot.types.InlineKeyboardButton('Пт', callback_data='calendar_ignore_fr'),
        telebot.types.InlineKeyboardButton('Сб', callback_data='calendar_ignore_sa'),
        telebot.types.InlineKeyboardButton('Вс', callback_data='calendar_ignore_su')
    )
    # middle
    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        keyboard.row(
            telebot.types.InlineKeyboardButton('-' if week[0] == 0 else str(week[0]), callback_data=f'DAY-{year}-{month}-{week[0]}'),
            telebot.types.InlineKeyboardButton('-' if week[1] == 0 else str(week[1]), callback_data=f'DAY-{year}-{month}-{week[1]}'),
            telebot.types.InlineKeyboardButton('-' if week[2] == 0 else str(week[2]), callback_data=f'DAY-{year}-{month}-{week[2]}'),
            telebot.types.InlineKeyboardButton('-' if week[3] == 0 else str(week[3]), callback_data=f'DAY-{year}-{month}-{week[3]}'),
            telebot.types.InlineKeyboardButton('-' if week[4] == 0 else str(week[4]), callback_data=f'DAY-{year}-{month}-{week[4]}'),
            telebot.types.InlineKeyboardButton('-' if week[5] == 0 else str(week[5]), callback_data=f'DAY-{year}-{month}-{week[5]}'),
            telebot.types.InlineKeyboardButton('-' if week[6] == 0 else str(week[6]), callback_data=f'DAY-{year}-{month}-{week[6]}')
        )
    # bottom
    keyboard.row(
        telebot.types.InlineKeyboardButton('< Пред.', callback_data='PREV_MONTH'),
        telebot.types.InlineKeyboardButton('След. >', callback_data='NEXT_MONTH')
    )

    bot.send_message(message.chat.id, caption1, reply_markup=keyboard)


@bot.message_handler(commands=['gettasks'])
def get_tasks(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Все не завершенные', callback_data='get_all_tasks'),
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('Все на сегодня', callback_data='get_today_tasks'),
        telebot.types.InlineKeyboardButton('Все на завтра', callback_data='get_tomorrow_tasks')
    )
    bot.send_message(message.chat.id, 'Выберите', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(query):
    data = query.data
    if data in get_tasks_dict:
        func = get_tasks_dict[data]
        func(query.message)
    else:
        calendar_callback(query)


@bot.callback_query_handler(func=lambda call: True)
def calendar_callback(query):
    data: str = query.data
    if data.startswith('DAY'):
        date1 = to_date(data)
        bot.send_message(query.message.chat.id, f'Выбрана дата = {date1}')


def to_date(data: str):
    (action, year, month, day) = data.split('-')
    return datetime.date(int(year), int(month), int(day))


@bot.message_handler(commands=['url'])
def btn_test(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    url_button = telebot.types.InlineKeyboardButton(text="Перейти на Яндекс", url="https://ya.ru")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, 'Нажми кнопку получишь результат', reply_markup=keyboard)


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
        'get_all_tasks': get_all_tasks,
        'get_today_tasks': get_today_tasks,
        'get_tomorrow_tasks': get_tomorrow_tasks
    }

    date = datetime.date(2020, 5, 15)
    print(date.strftime('%d.%m.%Y'))
    bot.polling()
