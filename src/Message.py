from abc import ABC, abstractmethod



class Message(ABC):

    def __init__(self):
        self.fromm : TgClient = None
        self.to : tg_id = None
        self.text : str = None

    @abstractmethod
    def send(self):
        pass



class MessageSchedule(Message):
    def __init__(self, text):
        self.text = text
        super().__init__()

    def send(self):
        pass


class MessageOnce(Message):
    def __init__(self):
        self.text = None
        super().__init__()


    def send(self):
        pass

    def createText(self):
        pass