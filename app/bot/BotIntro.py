import app.bot.config
import telebot


bot = telebot.TeleBot(app.bot.config.token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')


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
    func = get_tasks_dict[data]
    func(query.message)


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

    bot.polling()
