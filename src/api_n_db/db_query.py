import psycopg2
#import json
import datetime

class Bd_messenger():
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

    def send_messsage(self, id_sender: int, id_chat: int, text: str) -> bool:
        '''Отправка сообщения от пользователя в чат'''
        date = datetime.datetime.now().timestamp()
        text = text.strip()

        try:
            self.cur.execute(
                """INSERT INTO message (id_sender, id_chat, text, date) VALUES (%s, %s, %s, %s)""",
                (id_sender, id_chat, text, date)
            )
            self.conn.commit()
            return True
        
        except Exception as e:
            print(str(e))

    def update(self, id_user: int) -> list[dict, bool]:
        '''Получает все сообщения находящиеся в чатах где состоит данный пользователь'''
        id_chats, error = self.get_chats(id_user)

        if error:
            return {'error': id_chats}, False
        
        if id_chats is None:
            return {}, True
        
        string = ', '.join(['%s'] * len(id_chats))
        query = f"""SELECT * FROM message WHERE id_chat IN ({string})"""
        
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
            return {'error': str(e)}, False
        
        
        
        try:
            self.cur.execute(f"""SELECT users.id_chats FROM users WHERE users.id=%s""", (id_user,))
            id_chats = self.cur.fetchall()

            if id_chats:
                stroka = ','.join(['%s'] * len(id_chats[0][0]))
                query = f'SELECT id_mess FROM chat WHERE id_Chat IN ({stroka})'
                self.cur.execute(query, id_chats[0][0])
                answer = self.cur.fetchall()
                id_messages = []

                for i in answer:
                    for j in i:
                        for k in j:
                            id_messages.append(k)

                stroka = ','.join(['%s'] * len(id_messages))
                query = f"""SELECT * FROM messages WHERE messages.id_message IN ({stroka})"""
                self.cur.execute(query, id_messages)
                mess = self.cur.fetchall()

                messages_data = [
                    {
                        'id_mess': msg[0],
                        'id_sender': msg[1],
                        'id_chat': msg[2],
                        'text': msg[3],
                        'date': msg[4]
                    }
                    for msg in mess
                ]

                return messages_data, True
        
        except Exception as e:
            return {'error': str(e)}, False

    def get_chats(self, id_user: int) -> tuple[list, bool]:
        '''Получение списка чатов конекретного пользователя'''
        try:
            self.cur.execute(
                """SELECT id_chats FROM user WHERE id_user = %s""",
                (id_user,)
            )
            data = self.cur.fetchall()

            if data:
                return data[0][0], True
            
            return None, True
        
        except Exception as e:
            return str(e), False

if __name__ == "__main__":
    bd = Bd_messenger()
    bd.get_chats(1)
    stroka = bd.update(1)
    print(stroka)
