import sys
import socket

# Dicionário de tradução de mensagens
message_translation = {
    'PASS-213': 'Usuário registrado com sucesso.',
    'PASS-214': 'Login realizado com sucesso.',
    'ERRO-700': 'Você não está logado.',
    'ERRO-702': 'Argumentos inválidos.',
    'ERRO-703': 'Usuário já existe.',
    'ERRO-704': 'Credenciais inválidas.',
    'ERRO-999': 'Comando desconhecido.',
    'CHAT-215': 'Chat iniciado com sucesso.',
    'CHAT-216': 'O usuário não está conectado.',
    'CHAT-217': 'O chat já foi iniciado.',
    'CHAT-218': 'Um usuário não está logado.'
}

# Obtém os argumentos da linha de comando ou usa valores padrão
if len(sys.argv) >= 3:
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
# Se o usuário não definir HOST e porta, utiliza os metodos padrões abaixo:
else:
    HOST = '127.0.0.1'  # Valor padrão para o endereço IP
    PORT = 12345  # Valor padrão para a porta

# Criação do socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta-se ao servidor
client_socket.connect((HOST, PORT))

# Variáveis para armazenar o nome do usuário com quem estamos conversando
username = None
other_username = None

while True:
    # Solicita ao usuário para digitar um comando
    command = input('Digite um comando: ')

    # Envia o comando para o servidor
    client_socket.sendall(command.encode())

    # Recebe a resposta do servidor
    data = client_socket.recv(1024)

    # Processa a resposta recebida
    received_message = data.decode().strip()
    # Retorna a tradução da resposta enviada pelo servidor
    translated_message = message_translation.get(received_message, 'Resposta do servidor: ' + received_message)
    print(translated_message)

    # Verifica se o usuário está logado
    if received_message.startswith('PASS-214'):
        # O usuário está logado
        username = received_message.split()[1]

    # Verifica se o comando é CHAT
    if command.startswith('CHAT'):
        # Obtém o nome do usuário com quem deseja conversar
        other_username = command.split()[1]

        # Envia o comando CHAT para o servidor
        command = f'CHAT {other_username}'
        client_socket.sendall(command.encode())

        # Recebe a resposta do servidor
        data = client_socket.recv(1024)

        # Processa a resposta recebida
        received_message = data.decode().strip()

        # Se a resposta for CHAT-215, o chat foi iniciado com sucesso
        if received_message == 'CHAT-215':
            # Mostra uma mensagem de confirmação
            print('Chat com {} foi iniciado!'.format(other_username))

        # Se a resposta for diferente de CHAT-215, o chat não foi iniciado
        else:
            print(received_message)

    # Verifica se o comando é EXIT
    if command.lower() == 'bye':
        # Encerra a conexão com o servidor
        client_socket.close()
        break
