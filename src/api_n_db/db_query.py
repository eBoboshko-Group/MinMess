import psycopg2
#import json
import datetime

class DbMessenger():
    def __init__(self):
        '''Установка соединения с БД'''
        self.conn = psycopg2.connect(
            host="46.8.225.46",
            database="minmess",
            port="5432",
            user="postgres",
            password="Buhjvfybz123!"
        )
        self.cur = self.conn.cursor()

    def send_messsage(self, id_sender: int, id_chat: int, text: str) -> bool | str:
        '''Отправка сообщения от данного пользователя в данный чат'''
        date = datetime.datetime.now()
        text = text.strip()

        try:
            self.cur.execute(
                """INSERT INTO message (id_sender, id_chat, text, date) VALUES (%s, %s, %s, %s)""",
                (id_sender, id_chat, text, date)
            )
            self.conn.commit()
            return True
        
        except Exception as e:
            return str(e)

    def update(self, id_user: int) -> tuple[list, bool]:
        '''Получает все сообщения находящиеся в чатах где состоит данный пользователь'''
        id_chats, error = self.get_chats(id_user)

        if not error:
            # Ошибка в get_chats()
            return [{'error': id_chats}], False
        
        if not id_chats:
            # Чатов нет
            return [], True
        
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
            return messages_data, True
        
        except Exception as e:
            return [{'error': str(e)}], False

    def get_chats(self, id_user: int) -> tuple[list, bool]:
        '''Получение списка чатов данного пользователя'''
        try:
            self.cur.execute(
                """SELECT id_chats FROM "user" WHERE id_user = %s""",
                (id_user,)
            )
            data = self.cur.fetchone()

            if data:
                return data[0], True
            
            return [], True
        
        except Exception as e:
            return str(e), False

if __name__ == "__main__":
    db = DbMessenger()
    db.get_chats(1)