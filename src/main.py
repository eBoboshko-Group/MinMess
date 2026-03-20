from requests import get

def send_message(id_sender: int, id_chat: int, text: str) -> str:
    url: str = f"http://46.8.225.46:8001/send_mes/{id_sender}/{id_chat}/{text}"
    response = get(url)

    if response.status_code == 200:
        data = response.json()

        text = (
            f"Сообщение для {id_chat} {data['status']}"
        )
    
    else:
        text = f"Возникла ошибка при отправке сообщения\nКод ошибки: {response.status_code}"

    return text

if __name__ == "__main__":
    text = send_message(1, 2, "TIMURIBRAGIMOV")
    print(text)