from fastapi import FastAPI
from db_query import Bd_messenger

def register_endpoints(app: FastAPI):
    bd = Bd_messenger()

    @app.get("/")
    def home() -> list[dict, bool]:
        try:
            return {"message": "Api от MinMess"}, False
        
        except Exception as e:
            return {}, True

    @app.get("/send_mes/{id_sender}/{id_chat}/{text}")
    async def send_message(id_sender: int, id_chat: int, text: str) -> list[dict, bool]:
        try:
            bd.send_messsage([id_sender, id_chat, text])
            return {"status": "Отправлено", "id_sender": {id_sender}, "text": {text}}, False

        except Exception as e:
            return {"status": "Не дошло"}, True

    @app.get("/update/{id_user}")
    async def update(id_user: int) -> list[dict, bool]:
        try:
            result = bd.update(id_user)
            return result, False
        
        except Exception as e:
            return [], True

    @app.get("/get_chats/{id_user}")
    async def get_chats(id_user: int) -> list[dict, bool]:
        try:
            return {"id_chats": bd.get_chats(id_user)}, False
        
        except Exception as e:
            return {"id_chats": None}, True