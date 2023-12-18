# servidor:
import socket
import threading

HOST = ''
PORT = 50000
active_users = {}

def handle_client(client_socket, address):
    username = ''
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            message = message.decode().strip()
            print(f"Mensagem recebida de {username}: {message}")  
            response, username = process_message(message, client_socket, address, username)
            if response is not None:
                try:
                    client_socket.send(response.encode())
                except OSError as e:
                    print(f"Erro ao enviar resposta: {e}")
                    break
            if response == 'PASS-217':
                break  # Encerra o loop após o comando SAIR
    except OSError as e:
        print(f"Erro de socket: {e}")
    finally:
        print("Cliente desconectado")
        client_socket.close()

def process_message(message, client_socket, address, username):
    parts = message.split(' ')
    command = parts[0]
    if command == 'NOVO':
        if len(parts) != 3:
            return 'ERRO-702', ''
        _, username, password = parts
        if username in active_users:
            return 'ERRO-703', ''
        active_users[username] = {'password': password, 'socket': client_socket}
        return 'PASS-213', username
    elif command == 'ENTRAR':
        if len(parts) != 3:
            return 'ERRO-702', ''
        _, username, password = parts
        if username not in active_users or active_users[username]['password'] != password:
            return 'ERRO-704', ''
        return 'PASS-214', username
    elif command == 'CHAT':
        if len(parts) < 3:
            return 'ERRO-702', ''
        _, target, *msg_parts = parts
        msg = ' '.join(msg_parts)
        if target in active_users:
            active_users[target]['socket'].send(f'{username}: {msg}'.encode())
            return 'CHAT-215', username
        else:
            return 'CHAT-216', username
    elif command == 'LISTA':
        return ', '.join(active_users.keys()), username
    elif command == 'SAIR':
        active_users.pop(username)
        client_socket.close()
        print("Cliente desconectado")

    return 'ERRO-999', ''

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
