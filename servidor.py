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
    print(f'O cliente com o ip {ip_cliente[0]} foi conectado')
    clientes.append((conexao, ip_cliente))
    return conexao, ip_cliente


def encerrar_conexao(conexao_tcp):
    print("Encerrando a conexão e saindo do programa")
    conexao_tcp.close()


def listening(conexao_tcp, ip_cliente):
    print("Começando o BATchat. Esperando a mensagem...")

    while True:
        receber_mensagem = json.loads(conexao_tcp.recv(Buffer).decode('utf-8'))

        if receber_mensagem != '':
            print(f'\nCliente {ip_cliente[0]}: {receber_mensagem}')
            if receber_mensagem == 'exit':
                print("O servidor encerrou a conexão. Quer desconectar também? Digite exit também.")

        enviando_mensagem = input('Você: ')

        if enviando_mensagem != "":
            for cliente in clientes:
                cliente[0].send(bytes(json.dumps(enviando_mensagem), "utf8"))
            if enviando_mensagem == "exit":
                break
    encerrar_conexao(conexao_tcp)


def handle_client(conexao_corrente, cliente):
    listening(conexao_corrente, cliente)


if __name__ == '__main__':
    servidor = concetar_ao_servidor()

    while True:
        conexao_corrente, cliente = confirmacao_do_cliente(servidor)
        thread = threading.Thread(target=handle_client, args=(conexao_corrente, cliente))
        thread.start()

    sys.exit()
