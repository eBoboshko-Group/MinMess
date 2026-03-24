import psycopg2
import datetime

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

    def send_messsage(self, id_sender: int, id_chat: int, text: str):
        date = datetime.datetime.now()
        text = text.strip()

        try:
            self.cur.execute(
                query = """INSERT INTO message (id_sender, id_chat, text, date) VALUES (%s, %s, %s, %s)""",
                vars  = (id_sender, id_chat, text, date)
            )
            self.conn.commit()
            return date, text
            
        except Exception as e:
            print(f"Error send: {e}")
            return None, None

    def update(self, id_user: int):
        id_chats = self.get_chats(id_user)

        if id_chats is None:
            return {"error": "Ошибка получения чатов (на уровне БД)"}
        
        if not id_chats:
            return []

        placeholders = ', '.join(['%s'] * len(id_chats))
        query = f"""SELECT id_mess, id_sender, id_chat, text, date FROM message WHERE id_chat IN ({placeholders})"""
        
        try:
            self.cur.execute(query, id_chats)
            messages = self.cur.fetchall()

            return [
                {
                    'id_mess': m[0],
                    'id_sender': m[1],
                    'id_chat': m[2],
                    'text': m[3],
                    'date': m[4].isoformat() if isinstance(m[4], datetime.datetime) else m[4]
                }
                for m in messages
            ]
        except Exception as e:
            print(f"Error update: {e}")
            return {"error": str(e)}

    def get_chats(self, id_user: int):
        try:
            self.cur.execute(
                query = """SELECT id_chats FROM "user" WHERE id_user = %s""",
                vars  = (id_user,)
            )
            data = self.cur.fetchone()

            if data and data[0]:
                return data[0]
            
            return []
        
        except Exception as e:
            print(f"Error get_chats: {e}")
            return None

    def delete_message(self, id_mess: int):
        try:
            self.cur.execute(
                query = """DELETE FROM message WHERE id_mess = %s""",
                vars  = (id_mess,)
            )
            data = self.cur.fetchone()

            if data and data[0]:
                return data[0]
            
            return []
        
        except Exception as e:
            print(f"Error get_chats: {e}")
            return None