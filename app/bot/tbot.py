import telebot
from app.bot.bot_stack import BotStack

bot = telebot.TeleBot('1019358164:AAFGDWu1zn-nJyDKlKEFzFcuWBgYP-f30-Y')
stack = BotStack()


@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.send_message(message.chat.id, 'Начинаем работу /start')
    push(msg)


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

def push(message):
    stack.push(message.chat.id, message.message_id)


def pop(chat_id):
    message_id = stack.pop(chat_id)
    return message_id


if __name__ == '__main__':
    bot.polling()
