# cliente:
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
    'ERRO-700': 'Você não está logado.',
    'ERRO-702': 'Argumentos inválidos.',
    'ERRO-703': 'Nome de usuário já existe.',
    'PASS-213': 'Usuário registrado com sucesso.',
    'ERRO-704': 'Credenciais inválidas.',
    'PASS-214': 'Login realizado com sucesso.',
    'CHAT-215': 'Mensagem enviada com sucesso',
    'CHAT-216': 'Usuário alvo não está online.',
    'PASS-217': 'Desconectado com sucesso.',
    'ERRO-999': 'Comando inválido.'
}

username = ''
while True:
    command = input('Digite um comando: ')
    client_socket.send(command.encode())
    response = client_socket.recv(1024).decode()
    print(f'{response}: {message_translation.get(response, response)}')
    if command.startswith('ENTRAR') and 'PASS-214' in response:
        username = command.split(' ')[1]
        threading.Thread(target=receive_message).start()
        send_thread = threading.Thread(target=send_message)
        send_thread.start()
        send_thread.join()
