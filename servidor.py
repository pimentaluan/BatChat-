import socket
import threading

HOST = ''  # Endereço IP do servidor
PORT = 12345  # Porta de escuta do servidor

active_users = {}  # Dicionário para armazenar usuários e suas informações

def handle_client(client_socket, client_address):
    global active_users
    username = None  # Define username at the beginning of the function

    while True:
        data = client_socket.recv(1024)

        if not data:
            print('CLIENT DISCONNECTED:', client_address)
            break

        received_message = data.decode().strip()
        print('RECEIVED MESSAGE:', received_message)

        response_message = process_message(received_message, client_socket, client_address, username)  # Pass username to process_message
        client_socket.sendall(response_message.encode())

def process_message(message, client_socket, client_address, username):
    global active_users

    message = message.upper()

    if message.startswith('NOVO'):
        split_message = message.split(' ')
        if len(split_message) < 3:
            return 'ERRO-702\n'

        new_username = split_message[1]
        password = split_message[2]

        if new_username in active_users:
            return 'ERRO-703\n'  # Usuário já existe

        active_users[new_username] = {'password': password, 'socket': client_socket, 'chats': []}
        return 'PASS-213\n'  # Usuário registrado com sucesso

    elif message.startswith('ENTRAR'):
        split_message = message.split(' ')

        if len(split_message) < 3:
            return 'ERRO-702\n'

        login_username = split_message[1]
        password = split_message[2]

        if login_username not in active_users:
            return 'ERRO-704\n'  # Usuário não encontrado

        if active_users[login_username]['password'] != password:
            return 'ERRO-705\n'  # Senha incorreta

        username = login_username  # Correção: Define o username ao entrar
        active_users[username]['socket'] = client_socket  # Associa o nome de usuário ao socket
        return f'PASS-214 {username}\n'  # Login realizado com sucesso e envia o username

    elif message.startswith('CHAT'):
        split_message = message.split(' ')
        if len(split_message) < 2:
            return 'ERRO-702\n'  # Comando incompleto

        user_to_chat = split_message[1]
        if user_to_chat not in active_users:
            return 'ERRO-706\n'  # Usuário não encontrado

        username = [k for k, v in active_users.items() if v['socket'] == client_socket][0]

        # Verifica se já está em um chat com o usuário que se quer iniciar outro chat
        if user_to_chat in active_users[username]['chats']:
            return 'ERRO-707\n'  # Já está em um chat

        active_users[username]['chats'].append(user_to_chat)
        active_users[user_to_chat]['chats'].append(username)

        receiver_socket = active_users[user_to_chat]['socket']
        receiver_socket.sendall(f'CHAT-INICIAR {username}\n'.encode())
        return 'PASS-215\n'  # Iniciar chat com o usuário específico


    elif message.startswith('ENVIAR'):
        split_message = message.split(' ', 2)
        if len(split_message) < 3:
            return 'ERRO-702\n'  # Comando incompleto

        sender = username  # Use o username passado por handle_client
        receiver = split_message[1]
        message_content = split_message[2]

        if receiver not in active_users:
            return 'ERRO-706\n'  # Usuário não encontrado

        if sender in active_users and receiver in active_users:
            if receiver in active_users[sender]['chats']:
                receiver_socket = active_users[receiver]['socket']
                receiver_socket.sendall(f'RECEBIDO {sender}: {message_content}\n'.encode())
                return 'PASS-216\n'  # Mensagem enviada com sucesso

        return 'ERRO-708\n'  # Chat não iniciado

    
    

    elif message.startswith('SAIR'):
        username = [k for k, v in active_users.items() if v['socket'] == client_socket][0]
        del active_users[username]
        client_socket.close()
        return 'PASS-217\n'  # Desconectado com sucesso

    return 'ERRO-500\n'  # Comando desconhecido

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