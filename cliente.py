import socket
import sys

def enviar_mensagem(conexao_tcp):
    while True:
        mensagem = input("Digite sua mensagem (ou 'exit' para sair): ")
        conexao_tcp.send(bytes(mensagem, "utf-8"))
        if mensagem.lower() == 'exit':
            break

def receber_mensagem(conexao_tcp):
    Buffer = 1024
    while True:
        try:
            mensagem = conexao_tcp.recv(Buffer).decode('utf-8')
            if mensagem == '':
                break
            print(mensagem)
            if mensagem.lower() == 'exit':
                break
        except ConnectionResetError:
            break

message_translation = {
    'PASS-213': 'Usuário registrado com sucesso.',
    'PASS-214': 'Login realizado com sucesso.',
    'ERRO-702': 'Argumentos inválidos.',
    'ERRO-703': 'Usuário já existe.',
    'ERRO-704': 'Credenciais inválidas.',
    'ERRO-706': 'Usuário não encontrado.',
    'ERRO-999': 'Comando desconhecido.',
    'MSG-RECEBIDA': 'Mensagem recebida: '
}

if len(sys.argv) >= 3:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
else:
    HOST = '127.0.0.1'
    PORT = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

username = None

while True:
    command = input('Digite um comando: ')
    client_socket.sendall(command.encode())

    data = client_socket.recv(1024)
    received_message = data.decode().strip()

    translated_message = message_translation.get(received_message, 'Resposta do servidor: ' + received_message)
    print(translated_message)

    if received_message.startswith('PASS-214'):
        username = received_message.split()[1]

    if command.lower() == 'chat':
        # Lógica para iniciar o chat...
        while True:
            mensagem = input('Digite sua mensagem (ou "exit" para sair do chat): ')
            client_socket.sendall(f'ENVIAR {username} {mensagem}'.encode())

            if mensagem.lower() == 'exit':
                break
            
            data = client_socket.recv(1024)
            received_message = data.decode().strip()

            translated_message = message_translation.get(received_message, 'Resposta do servidor: ' + received_message)
            print(translated_message)

            # Condição separada para lidar com o comando 'enviar' fora do loop do chat
            if command.lower().startswith('enviar'):
                split_command = command.split(' ', 3)
                if len(split_command) < 4:
                    print('Comando incompleto.')
                    continue

                client_socket.sendall(command.encode())

                data = client_socket.recv(1024)
                received_message = data.decode().strip()

                translated_message = message_translation.get(received_message, 'Resposta do servidor: ' + received_message)
                print(translated_message)
                
            if command.lower() == 'listar':
                client_socket.sendall('LISTAR'.encode())
                data = client_socket.recv(1024)
                active_users = data.decode().strip()
                print('Usuários ativos:', active_users)