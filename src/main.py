from requests import get
from config import *

def ping():
    response = get(
        url     = f"{FULL_DOMAIN}/",
        timeout = 60
    )

    if response.status_code == 200: # OK
        data = response.json()
        return data
    else:
        return {'status': False}

def send_message(id_sender: int, id_chat: int, text: str):
    url = f"{FULL_DOMAIN}/send_message/{id_sender}/{id_chat}/{text}"
    response = get(
        url     = url,
        timeout = 60
    )

    if response.status_code == 200: # OK
        data = response.json()
        result = f"Сообщение успешно отправлено ({data['date']})"
    else:
        result = f"Ошибка в процессе отправки ({response.status_code})"

    return result

if __name__ == "__main__":
    status = ping()
    print(status['status'])