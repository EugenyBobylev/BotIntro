import datetime


class TodoTask():
    def __init__(self):
        self.descr: str = 'новая задача'
        self.stop: datetime.date = datetime.date.today()

    def __repr__(self):
        return f'Задача: "{self.descr}"\nСрок: {self.stop}'

    @staticmethod
    def create(param):
        task = TodoTask()
        task.descr = param['задача']
        task.stop = param['срок']

        return task
