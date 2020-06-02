import datetime
import re
import app.bot.TCalendar


def test_str_to_int():
    src = '-10'
    ok: bool = src[0] == '-' and src[1:].isdigit()
    assert ok


def test_str_to_date():
    src = '10.06.2020'
    src_date = datetime.date(year=2020, month=6, day=10)
    date = (datetime.datetime.strptime(src, '%d.%m.%Y')).date()
    assert src_date == date
