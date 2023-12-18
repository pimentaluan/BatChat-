import socket
import threading

HOST = ''
PORT = 50000
active_users = {}

def handle_client(client_socket, address):
    username = ''
    while True:
        try:
            message = client_socket.recv(1024)
        except ConnectionResetError:
            print("Cliente desconectado inesperadamente")
            break
        if not message:
            break
        message = message.decode().strip()
        print(f"Mensagem recebida de {username}: {message}")  # Log and display the received message
        response, username = process_message(message, client_socket, address, username)
        if 'Login bem-sucedido.' in response:
            client_socket.send(response.encode())
            client_socket.send(f'Bem-vindo, {username}! Você está conectado.\n\n'
                               'Aqui estão os comandos disponíveis:\n'
                               '- LISTA: Lista todos os usuários registrados.\n\n'
                               '- CHAT <username> <mensagem>: Inicia um chat com o usuário especificado, enviando mensagem.\n'
                               '  Exemplo: CHAT maria Olá, como você está?\n\n'
                               '- SAIR: Encerra a conexão com o servidor.\n'.encode())
        else:
            client_socket.send(response.encode())

def process_message(message, client_socket, address, username):
    parts = message.split(' ')
    command = parts[0]
    if command == 'NOVO':
        _, username, password = message.split(' ')
        if username in active_users:
            return 'Nome de usuário já existe.', username
        active_users[username] = {'password': password, 'socket': client_socket}
        return 'Usuário registrado com sucesso.', username
    elif command == 'ENTRAR':
        _, username, password = message.split(' ')
        if username not in active_users or active_users[username]['password'] != password:
            return 'Nome de usuário ou senha incorretos.', ''
        return 'Login bem-sucedido.', username
    elif command == 'CHAT':
        _, target, *msg_parts = parts
        msg = ' '.join(msg_parts)
        if target in active_users:
            active_users[target]['socket'].send(f'{username}: {msg}'.encode())
            return 'Mensagem enviada.', username
        else:
            return 'Usuário alvo não está online.', username

    elif command == 'LISTA':
        return ', '.join(active_users.keys()), username
    
    elif command == 'SAIR':
        active_users.pop(username, None)
        client_socket.close()
        return 'Desconectado com sucesso.', ''
    return 'Comando inválido.', username

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print('Servidor iniciado.')
    while True:
        client_socket, address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, address)).start()
    server_socket.close()

if __name__ == '__main__':
    main()