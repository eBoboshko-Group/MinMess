from fastapi import FastAPI
from src.db_query import DbMessenger

def register_endpoints(app: FastAPI):
    db = DbMessenger()
    
    @app.get('/')
    def ping() -> dict:
        return {'status': True}
    
    @app.get('/send_messsage/{id_sender}/{id_chat}/{text}')
    def send_messsage(id_sender: int, id_chat: int, text: str) -> tuple[float, str]:
        date, text = db.send_messsage(id_sender, id_chat, text)

        if text is None:
            return None

        return {'date': date, 'text': text}
    
    @app.get('/get_chats/{id_user}')
    def get_chats(id_user: int) -> list:
        id_chats = db.get_chats(id_user)

        if id_chats is None or not id_chats:
            return None
        
        return {'id_chats': id_chats}
    
    @app.get('/update/{id_user}')
    def update(id_user: int) -> dict:
        messages_data = db.update(id_user)

        if messages_data is None or not messages_data:
            return None
        
        return messages_data