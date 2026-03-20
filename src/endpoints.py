from fastapi import FastAPI
from db_query import DbMessenger

def register_endpoints(app: FastAPI):
    db = DbMessenger()

    @app.get('/')
    def root() -> str:
        return "API MinMess"
    
    @app.get('/send_message/{id_sender}/{id_chat}/{text}')
    def send_message(id_sender: int, id_chat: int, text: str) -> int:
        result = db.send_messsage(id_sender, id_chat, text)
        
        if result is True:
            return 1 # Дошло

        return 0 # Не дошло
    
    @app.get('/update/{id_user}')
    def update(id_user: int):
        result, error = db.update(id_user)
        return result
    
    @app.get('/get_chats/{id_user}')
    def get_chats(id_user: int):
        result, error = db.get_chats(id_user)
        return result
