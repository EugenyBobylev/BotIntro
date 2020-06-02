import datetime

class TodoTask():
    def __init__(self):
        self.descr: str = 'новая задача'
        self.stop: datetime.date = datetime.date.today()

    @staticmethod
    def create(param):
        task = TodoTask()
        task.descr = param['задача']
        task.stop = param['срок']

        return task
