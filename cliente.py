# client.py
import socket
import sys
import threading

if len(sys.argv) > 2:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    HOST = '127.0.0.1'
    PORT = 50000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def send_message():
    while True:
        message = input()
        if message == 'exit':
            client_socket.send(message.encode())
            break
        client_socket.send(message.encode())


def receive_message():
    while True:
        message = client_socket.recv(1024)
        if not message:
            break
        print(message.decode())

message_translation = {
    'Nome de usuário já existe.': 'Nome de usuário já existe.',
    'Usuário registrado com sucesso.': 'Usuário registrado com sucesso.',
    'Nome de usuário ou senha incorretos.': 'Nome de usuário ou senha incorretos.',
    'Login bem-sucedido.': 'Login bem-sucedido.',
    'Usuário alvo não está online.': 'Usuário alvo não está online.',
    'Solicitação de chat enviada.': 'Solicitação de chat enviada.',
    'Desconectado com sucesso.': 'Desconectado com sucesso.',
    'Comando inválido.': 'Comando inválido.'
}

username = ''
while True:
    command = input('Digite um comando: ')
    client_socket.send(command.encode())
    response = client_socket.recv(1024).decode()
    print(message_translation.get(response, response))
    if command.startswith('ENTRAR') and 'Login bem-sucedido.' in response:
        username = command.split(' ')[1]
        threading.Thread(target=receive_message).start()
        send_thread = threading.Thread(target=send_message)
        send_thread.start()
        send_thread.join()
