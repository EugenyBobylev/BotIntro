from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
import calendar
import datetime


def create_calendar(year=None, month=None):
    now = datetime.date.today()
    if year is None:
        year = now.year
    if month is None:
        month = now.month

    keyboard = InlineKeyboardMarkup()
    # top
    keyboard.row(
        InlineKeyboardButton(f'{calendar.month_name[month]} {year}', callback_data='IGNORE-0-0-0')
    )
    keyboard.row(
        InlineKeyboardButton('Пн', callback_data='MONDAY-0-0-0'),
        InlineKeyboardButton('Вт', callback_data='TUESDAY-0-0-0'),
        InlineKeyboardButton('Ср', callback_data='WEDNESDAY-0-0-0'),
        InlineKeyboardButton('Чт', callback_data='THURSDAY-0-0-0'),
        InlineKeyboardButton('Пт', callback_data='FRIDAY-0-0-0'),
        InlineKeyboardButton('Сб', callback_data='SATURDAY-0-0-0'),
        InlineKeyboardButton('Вс', callback_data='SUNDAY-0-0-0')
    )
    # middle
    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        keyboard.row(
            InlineKeyboardButton('-' if week[0] == 0 else str(week[0]), callback_data=f'DAY-{year}-{month}-{week[0]}'),
            InlineKeyboardButton('-' if week[1] == 0 else str(week[1]), callback_data=f'DAY-{year}-{month}-{week[1]}'),
            InlineKeyboardButton('-' if week[2] == 0 else str(week[2]), callback_data=f'DAY-{year}-{month}-{week[2]}'),
            InlineKeyboardButton('-' if week[3] == 0 else str(week[3]), callback_data=f'DAY-{year}-{month}-{week[3]}'),
            InlineKeyboardButton('-' if week[4] == 0 else str(week[4]), callback_data=f'DAY-{year}-{month}-{week[4]}'),
            InlineKeyboardButton('-' if week[5] == 0 else str(week[5]), callback_data=f'DAY-{year}-{month}-{week[5]}'),
            InlineKeyboardButton('-' if week[6] == 0 else str(week[6]), callback_data=f'DAY-{year}-{month}-{week[6]}')
        )
    # bottom
    keyboard.row(
        InlineKeyboardButton('< Пред.', callback_data=f'PREV_MONTH-{year}-{month}-0'),
        InlineKeyboardButton('След. >', callback_data=f'NEXT_MONTH-{year}-{month}-0')
    )
    return keyboard


def calendar_callback(bot, query):
    ret_data = (False, None)
    data: str = query.data
    (action, syear, smonth, sday) = data.split('-')
    year = int(syear)
    month = int(smonth)
    day = int(sday)
    if action == 'DAY':
        date = datetime.date(year, month, day)
        ret_data = True, date
    elif action == 'PREV_MONTH':
        if month == 1:
            year = year - 1
            month = 12
        else:
            month = month - 1
        bot.edit_message_text(
            text='Выберите дату',
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(year, month)
        )
    elif action == 'NEXT_MONTH':
        if month == 12:
            year = year + 1
            month = 1
        else:
            month = month + 1
        bot.edit_message_text(
            text='Выберите дату',
            chat_id=query.message.chat.id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(year, month)
        )
    return ret_data


def date_from_str(strdate: str):
    date = datetime.date.today()
    if strdate.isdigit():
        days = datetime.timedelta(days=int(strdate))
        date = date + days
    elif strdate[0] == '-' and strdate[1:].isdigit():
        days = datetime.timedelta(days=int(strdate))
        date = date + days
    else:
        date = (datetime.datetime.strptime(strdate, '%d.%m.%Y')).date()
    return date
