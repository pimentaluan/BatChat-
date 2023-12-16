import socket
import threading

HOST = '0.0.0.0'  # Endereço IP do servidor
PORT = 12345  # Porta de escuta do servidor

users = {}  # Dicionário para armazenar usuários
user_sockets = {}  # Dicionário para mapear usuários a seus respectivos sockets
user_chats = {}  # Dicionário para controlar chats

def handle_client(client_socket, client_address):
    global users, user_sockets, user_chats

    while True:
        data = client_socket.recv(1024)
        if not data:
            print('CLIENT DISCONNECTED:', client_address)
            break

        received_message = data.decode().strip()
        print('RECEIVED MESSAGE:', received_message)
        response_message = process_message(received_message, client_socket)
        client_socket.sendall(response_message.encode())

def process_message(message, client_socket):
    global users, user_sockets, user_chats

    message = message.upper()

    if message.startswith('REG'):
        split_message = message.split(' ')
        if len(split_message) < 3:
            return 'ERRO-702\n'

        username = split_message[1]
        password = split_message[2]

        if username in users:
            return 'ERRO-703\n'  # Usuário já existe

        users[username] = password
        user_sockets[username] = client_socket
        return 'PASS-213\n'  # Usuário registrado com sucesso

    elif message.startswith('LOG'):
        split_message = message.split(' ')
        if len(split_message) < 3:
            return 'ERRO-702\n'

        username = split_message[1]
        password = split_message[2]

        if username not in users:
            return 'ERRO-704\n'  # Usuário não encontrado

        if users[username] != password:
            return 'ERRO-705\n'  # Senha incorreta

        return 'PASS-214 {}\n'.format(username)  # Usuário logado com sucesso

    elif message == 'LIST':
        users_list = '\n'.join(users.keys()) + '\n'
        return users_list

    elif message.startswith('CHAT'):
        split_message = message.split(' ')
        if len(split_message) < 2:
            return 'ERRO-702\n'  # Comando incompleto

        user_to_chat = split_message[1]
        if user_to_chat not in users:
            return 'ERRO-706\n'  # Usuário não encontrado

        # Se já estiver em um chat, não inicia outro
        if user_to_chat in user_chats or username in user_chats.values():
            return 'ERRO-707\n'  # Já está em um chat

        user_chats[username] = user_to_chat
        user_chats[user_to_chat] = username

        user_sockets[user_to_chat].sendall(f'CHAT-START {username}\n'.encode())
        return 'PASS-215\n'  # Iniciar chat com o usuário específico

    elif message.startswith('SEND'):
        split_message = message.split(' ', 2)
        if len(split_message) < 3:
            return 'ERRO-702\n'  # Comando incompleto

        sender = split_message[1]
        message_content = split_message[2]

        if sender not in users:
            return 'ERRO-706\n'  # Usuário não encontrado

        receiver = user_chats.get(sender)
        if not receiver:
            return 'ERRO-708\n'  # Chat não iniciado

        user_sockets[receiver].sendall(f'RECEIVE {sender}: {message_content}\n'.encode())

        return 'PASS-216\n'  # Mensagem enviada com sucesso

    return 'ERRO-500\n'

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    print('SERVER STARTED')

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print('CLIENT CONNECTED:', client_address)

            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    finally:
        server_socket.close()

if __name__ == '__main__':
    main()
