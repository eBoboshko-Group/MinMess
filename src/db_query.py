import psycopg2
import datetime

class DbMessenger():
    def __init__(self):
        '''Установка соединения с БД'''
        self.conn = psycopg2.connect(
            host     = "46.8.225.46",
            database = "minmess",
            port     = "5432",
            user     = "postgres",
            password = "Buhjvfybz123!"
        )
        self.cur = self.conn.cursor()

    def send_messsage(self, id_sender: int, id_chat: int, text: str) -> tuple[float, str]:
        '''Отправка сообщения от данного пользователя в данный чат'''
        date = datetime.datetime.now()
        text = text.strip()

        try:
            self.cur.execute(
                query = """INSERT INTO message (id_sender, id_chat, text, date) VALUES (%s, %s, %s, %s)""",
                vars  = (id_sender, id_chat, text, date)
            )
            self.conn.commit()
            return date, text
        
        except Exception:
            return 0.0, None

    def update(self, id_user: int) -> dict:
        '''Получает все сообщения находящиеся в чатах где состоит данный пользователь'''
        id_chats = self.get_chats(id_user)

        if id_chats is None:
            # Ошибка в get_chats()
            return {'status': "Ошибка"}
        
        if not id_chats:
            # Чатов нет
            return {'status': "Чатов нет"}
        
        placeholders = ', '.join(['%s'] * len(id_chats))
        query = f"""SELECT id_mess, id_sender, id_chat, text, date FROM message WHERE id_chat IN ({placeholders})"""
        
        try:
            self.cur.execute(query, id_chats)
            messages = self.cur.fetchall()

            messages_data = [
                {
                    'id_mess': message[0],
                    'id_sender': message[1],
                    'id_chat': message[2],
                    'text': message[3],
                    'date': message[4]
                }
                for message in messages
            ]
            return messages_data
        
        except Exception:
            return None

    def get_chats(self, id_user: int) -> list:
        '''Получение списка чатов данного пользователя'''
        try:
            self.cur.execute(
                query = """SELECT id_chats FROM "user" WHERE id_user = %s""",
                vars  = (id_user,)
            )
            data = self.cur.fetchone()

            if data and data[0]:
                return data[0]
            
            return []
        
        except Exception:
            return None