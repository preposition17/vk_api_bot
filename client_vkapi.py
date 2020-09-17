import vk_api
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

import requests
import json
import socket
import time
import configparser

def conf_read(param):
    config = configparser.ConfigParser()
    config.read('config.ini')
    method = {'group_token': config['KEYS']['group_token'],
              'app_service_key': config['KEYS']['app_service_key']
            }
    return method[param]

def con2serv():
    try:
        sock = socket.socket()
        sock.connect(('localhost', 9090))
        print('Connected!')
        return sock
    except ConnectionRefusedError:
        print('Server not responding.')
        print('Reconnecting...')
        time.sleep(5)
        return con2serv()

def client_exit(request, vk, event):
    if request == "кс" or request == "cs":
        print('Client exit...')
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=f'Клиент отключен.'
        )
        exit()

def server_exit(request, vk, event):
    if request == 'ss' or request == 'сс':
        print('Server exit...')
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=f'Сервер отключен.'
        )
    
def program_exit(request, vk, event):    
    if request == "стоп" or request == "stop":
        print('Exit...')
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message=f'Выход.'
        )
        exit()


def main():
    print('Client starting...')
    sock = con2serv()

    session = requests.Session() 
    vk_session = vk_api.VkApi(token=conf_read('group_token'))
    vk = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if event.to_me:
                request = event.text.lower()
                server_exit(request, vk, event)

                try:
                    data_send = str.encode(request)
                    sock.send(data_send)
                    data = sock.recv(1024)
                    message = data.decode()
                    print(f'Message received: {message}')
                    
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=get_random_id(),
                        message=f'{message}'
                    )    
                
                except vk_api.exceptions.ApiError:
                    program_exit(request, vk, event)
                    print('Server not responding.')
                    sock = con2serv()
                
                client_exit(request, vk, event)
                
                

try:
    if __name__ == '__main__':
        main()
        pass
except KeyboardInterrupt:
    print('\nExit...')
    exit()