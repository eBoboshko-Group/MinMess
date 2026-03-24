import psycopg2
from datetime import datetime

class DbMessenger():
    def __init__(self):
        self.conn = psycopg2.connect(
            host     = "46.8.225.46",
            database = "minmess",
            port     = "5432",
            user     = "postgres",
            password = "Buhjvfybz123!"
        )
        self.cur = self.conn.cursor()

    def send_messsage(self, id_sender: int, id_chat: int, text: str) -> tuple[float, str | None, None]:
        '''
        Записывает сообщение в базу данных. Время отправки функция формирует самостоятельно (datetime.now().timestamp())  
        Возвращает время отправки (date) и обработанный текст (text). В случае ошибки - None и None.
        '''
        date = datetime.now().timestamp()
        text = text.strip()

        try:
            self.cur.execute(
                query = """INSERT INTO messages (id_sender, id_chat, text, date) VALUES (%s, %s, %s, %s)""",
                vars  = (id_sender, id_chat, text, date)
            )
            self.conn.commit()
            return date, text

        except Exception as e:
            print(f"error: src/db_query.py: send_message(): {e}")
            return None, None

    def update(self, id_user: int) -> list[dict] | dict:
        '''
        Получает все сообщения из всех чатов где состоит данный пользователь.  
        Возвращает список со словарями к каждому сообщению или пустой список, если сообщений нет. В случае ошибки - словарь с ключем 'error', хранящим сообщение ошибки.
        '''
        id_chats = self.get_chats(id_user)

        if id_chats is None:
            return {"error": "Ошибка получения чатов (на уровне БД)"}

        if not id_chats:
            return []

        placeholders = ', '.join(['%s'] * len(id_chats))
        query = f"""SELECT id_mess, id_sender, id_chat, text, date FROM messages WHERE id_chat IN ({placeholders})"""

        try:
            self.cur.execute(query, id_chats)
            messages = self.cur.fetchall()

            return [
                {
                    'id_mess': m[0],
                    'id_sender': m[1],
                    'id_chat': m[2],
                    'text': m[3],
                    'date': m[4].isoformat() if isinstance(m[4], datetime) else m[4] # Что за вайбкод?
                }
                for m in messages
            ]

        except Exception as e:
            print(f"error: src/db_query.py: update(): {e}")
            return {"error": str(e)}

    def get_chats(self, id_user: int) -> list | None:
        '''Возвращает список чатов данного пользователя или пустой список, если чатов нет или None в случае ошибки.'''
        try:
            self.cur.execute(
                query = """SELECT id_chats FROM users WHERE id_user = %s""",
                vars  = (id_user,)
            )
            data = self.cur.fetchone()

            if data and data[0]:
                return data[0]
            
            return []

        except Exception as e:
            print(f"error: src/db_query.py: get_chats(): {e}")
            return None

    def edit_message(self, id_mess: int, new_text: str) -> tuple[float, str | None, None]:
        '''Возвращает список чатов данного пользователя или пустой список, если чатов нет или None в случае ошибки.'''
        date_edit = datetime.now().timestamp()
        new_text = new_text.strip()

        try:
            self.cur.execute(
                query = """UPDATE messages SET text = %s AND date_edit = %s WHERE id_mess = %s""",
                vars  = (new_text, date_edit, id_mess)
            )
            self.conn.commit()
            return date_edit, new_text

        except Exception as e:
            print(f"error: src/db_query.py: edit_message(): {e}")
            return None, None