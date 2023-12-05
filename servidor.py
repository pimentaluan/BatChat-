import socket
import sys
import threading
import json
from playsound import playsound

Ip_servidor = ''
Porta_servidor = 50000
Buffer = 1024

clientes = []


def concetar_ao_servidor():
    conexao_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexao_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor_socket = (Ip_servidor, Porta_servidor)
    conexao_tcp.bind(servidor_socket)
    conexao_tcp.listen(1)

    return conexao_tcp


def confirmacao_do_cliente(conexao_tcp):
    conexao, ip_cliente = conexao_tcp.accept()
    username = conexao.recv(Buffer).decode('utf-8')  # Recebe o nome de usuário do cliente
    print(f'O cliente com o nome de usuário {username} e ip {ip_cliente[0]} foi conectado')
    clientes.append((conexao, ip_cliente, username))  # Armazena o nome de usuário junto com a conexão e o IP
    return conexao, ip_cliente, username  # Retorna o nome de usuário


def encerrar_conexao(conexao_tcp):
    print("Encerrando a conexão e saindo do programa")
    conexao_tcp.close()


def listening(conexao_tcp, ip_cliente, username):
    print("Começando o BATchat. Esperando a mensagem...")
    while True:
        receber_mensagem = json.loads(conexao_tcp.recv(Buffer).decode('utf-8'))
        if receber_mensagem != '':
            print(f'\n{username}: {receber_mensagem}')  # Imprime a mensagem com o nome de usuário
            if receber_mensagem == 'exit':
                print("O servidor encerrou a conexão. Quer desconectar também? Digite exit também.")
            # Envia a mensagem para todos os clientes, exceto o remetente
            for cliente in clientes:
                if cliente[1] != ip_cliente:  # Verifica se o cliente atual não é o remetente
                    cliente[0].send(bytes(json.dumps(f"{username}: {receber_mensagem}"), "utf8"))

        # Cometado as linhas abaixo para remover a opção do servidor enviar mensagens
        # enviando_mensagem = input('Você: ')
        # if enviando_mensagem != "":
        #     # Envia a mensagem para todos os clientes
        #     for cliente in clientes:
        #         cliente[0].send(bytes(json.dumps(enviando_mensagem), "utf8"))
        #     if enviando_mensagem == "exit":
        #         break
    encerrar_conexao(conexao_tcp)


def handle_client(conexao_corrente, cliente, username):
    listening(conexao_corrente, cliente, username)


if __name__ == '__main__':
    servidor = concetar_ao_servidor()

    while True:
        conexao_corrente, cliente, username = confirmacao_do_cliente(servidor)
        thread = threading.Thread(target=handle_client, args=(conexao_corrente, cliente, username))
        thread.start()
    sys.exit()
