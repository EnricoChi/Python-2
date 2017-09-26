from socket import *
import time
import json

# Создаём сокет и слушаем
s = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
s.bind(('127.0.0.1', 8888))                # Присваивает порт 8888
s.listen(5)                       # Слушаем входящие

# Приводим ответ от сервера к формату JSON + JIM
def format_response(response, alert):
    answer = {
        "response" : response ,
        "time" : time.time(),
        "alert" : alert
    }
    on_output = json.dumps(answer)
    return on_output

# Формируем ответ для клиента
def output_to_client(data):
    if data['action'] == 'presence':
        response = '200'
        answer = format_response(response, 'Запрос на подключение принят --- ' + time.ctime(data['time']))
    elif data['action'] == 'msg':
        response = '200'
        answer = format_response(response, 'Сообщение "' + data['message'] + '" получено сервером --- ' + time.ctime(data['time']))
    elif data['action'] == 'quit':
        answer = 'quit'
    else:
        response = '100'
        answer = format_response(response, 'Не известный тип запроса --- ' + time.ctime(data['time']))
    return answer

# Отправляем ответ клиенту
def send_to_client(answer, client):
    client.send(answer.encode('utf-8'))
    pass


while True:
    result = s.accept()                     # Принять запрос на соединение
    client, addr = result
    client_data = client.recv(1024)         # Принимаем клиентские данные
    data = json.loads(client_data)          # Распарсиваем JSON
    answer = output_to_client(data)         # Формируем текст ответа клиенту
    send_to_client(answer, client)          # Отправляем ответ - answer => клиенту - client
    while True:
        message = json.loads(client.recv(1024))
        if message != 'quit':
            output = output_to_client(message)
            send_to_client(output, client)
        else:
            client.close()