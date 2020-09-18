import socket

def msg_snd(request):
    print(f'Message received: {request}')
    if request == 'ss' or request == 'сс':
        print('Server exit...')
        exit()
        
    if request == "кс" or request == "cs":
        print('Client exit...')

    if request == "стоп" or request == "stop":
        print('Exit...')
        exit()

    else:
        return request
    

'''
Put your funcs here and no one gets hurt.
'''

def main():
    print('Server starting...')
    while True:
        sock = socket.socket()
        sock.bind(('', 9090))
        sock.listen(1)
        print (f'Listening...')
        conn, addr = sock.accept()
        print (f'Client connected: {addr}')

        while True:
            data = conn.recv(1024)
            message = data.decode()
            if not data:
                break
            conn.send(str.encode(msg_snd(message)))
        print (f'Client disconnected: {addr}') 
        conn.close()

try:
    if __name__ == '__main__':
        main()
        pass
except KeyboardInterrupt:
    print('\nExit...')
    exit()