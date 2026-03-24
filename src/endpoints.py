from fastapi import FastAPI
from db_query import DbMessenger

def register_endpoints(app: FastAPI):
    db = DbMessenger()
    
    @app.get('/')
    def ping() -> dict:
        return {'status': True}
    
    @app.get('/send_messsage/{id_sender}/{id_chat}/{text}')
    def send_messsage(id_sender: int, id_chat: int, text: str) -> tuple[float, str]:
        date, text = db.send_messsage(id_sender, id_chat, text)

        if (date and text) is None:
            return {"status": "error", "details": 'Ошибка на уровне БД. Проверьте логи'}

        return {'date': date, 'text': text}
    
    @app.get('/edit_message/{id_mess}/{new_text}')
    def edit_message(id_mess: int, new_text: str):
        date_edit, new_text = db.edit_message(id_mess, new_text)

        if (date_edit and new_text) is None:
            return {"status": "error", "details": 'Ошибка на уровне БД. Проверьте логи'}

        return {'date_edit': date_edit, 'new_text': new_text}
    
    @app.get('/get_chats/{id_user}')
    def get_chats(id_user: int) -> list:
        id_chats = db.get_chats(id_user)

        if id_chats is None or not id_chats:
            return None
        
        return {'id_chats': id_chats}
    
    @app.get('/update/{id_user}')
    def update(id_user: int):
        messages_data = db.update(id_user)
        
        # Если вернулся словарь с ошибкой
        if messages_data is dict and "error" in messages_data:
            return {"status": "error", "details": messages_data["error"]}
            
        return messages_data