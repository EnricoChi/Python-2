from socket import *
import time
import json
import logging
from functools import wraps

import log_config

LOG_LEVEL = logging.DEBUG
log_config.set_logger('client', LOG_LEVEL)
CLIENT_LOG = logging.getLogger('client')

class Log:

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            CLIENT_LOG.debug('{}'.format(func.__name__))
            return result
        return inner


log = Log()



# Сформировать presence-сообщение в JIM
@log
def presence_format(action, time):
    message = {
        'action': action,
        'time': time,
    }
    return message


# Разобрать сообщение сервера
@log
def response_parse(response):
    output = 'Response code: ' + response['response'] + "\n"
    output += '--- ' + response['alert'] + ' ---'
    return output


# Отправляет сообщение серверу
@log
def send_message(presence_message, s):
    jpresence = json.dumps(presence_message)
    bpresence = jpresence.encode('utf-8')
    s.send(bpresence)


# Получается сообщение от сервера
@log
def get_response(sock):
    bresponse = sock.recv(1024)
    jresponse = bresponse.decode('utf-8')
    response = json.loads(jresponse)
    return response


if __name__ == '__main__':
    s = socket(AF_INET, SOCK_STREAM)                                # Создал сокет TCP
    s.connect(('localhost', 7777))                                  # Соединился с сервером
    presence_message = presence_format('presence', time.time())     # Сформировать presence-сообщение
    send_message(presence_message, s)
    response = get_response(s)
    response = response_parse(response)
    print(response)
