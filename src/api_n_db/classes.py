#from dataclasses import dataclass
import datetime as dt

class Message():
    def __init__(self, id_sender: int, id_chat: int, text: str):
        self.id_sender = id_sender
        self.id_chat = id_chat
        self.text = text.strip()
        self.date = dt.datetime.now().timestamp()