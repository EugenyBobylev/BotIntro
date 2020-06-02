import datetime
from app.bot.model import TodoTask


def test_create():
    task = TodoTask()
    assert task is not None


def test_create_from_dict():
    descr = 'Моя задача'
    date = datetime.date(year=2020, month=6, day=12)
    data = {"задача": descr, "срок": date}
    task = TodoTask.create(data)

    assert isinstance(task, TodoTask)