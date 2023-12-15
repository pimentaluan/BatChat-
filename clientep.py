import socket
import sys
import threading
import json

Porta_servidor = 50000
Buffer = 1024

def conectar_ao_servidor():
    while True:
        ip_servidor = input("Digite o IP do servidor para conectar: ")
        conexao_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor_socket = (ip_servidor, Porta_servidor)
        try:
            conexao_tcp.connect(servidor_socket)
            print("Você está conectado.")
            return conexao_tcp
        except (socket.gaierror, ConnectionRefusedError):
            print("Esse IP não corresponde com o do servidor. Tente novamente.")

def enviar_mensagem(conexao_tcp):
    while True:
        mensagem = input("Digite sua mensagem (ou 'exit' para sair): ")
        conexao_tcp.send(bytes(json.dumps(mensagem), "utf-8"))
        if mensagem.lower() == 'exit':
            break

def receber_mensagem(conexao_tcp):
    while True:
        try:
            mensagem = conexao_tcp.recv(Buffer).decode('utf-8')
            if mensagem == '':
                break
            print(mensagem)
            if mensagem.lower() == 'exit':
                break
        except ConnectionAbortedError:
            break

def main():
    conexao = conectar_ao_servidor()
    while True:
        escolha = input("Digite 'REGISTRAR' para criar uma nova conta ou 'ENTRAR' para entrar: ").lower()
        if escolha in ['registrar', 'entrar']:
            conexao.send(bytes(escolha, "utf-8"))
            break
        else:
            print("Escolha inválida. Tente novamente.")

    if escolha == 'registrar':
        nome = input('Digite o nome do usuário para registro')
        senha = input("Digite sua senha para registro: ")
        conexao.send(bytes(senha, "utf-8"))

    elif escolha == 'entrar':
        username = input("Digite seu nome de usuário: ")
        senha = input('Digite sua senha: ')
        conexao.send(bytes(username, "utf-8"))
        conexao.send(bytes(senha, "utf-8"))

    # Recebe a opção de registro ou login imediatamente após a conexão
    opcao = conexao.recv(Buffer).decode('utf-8').lower()

    if "registro" in opcao or "login" in opcao:
        senha = input("Digite sua senha: ")
        conexao.send(bytes(senha, "utf-8"))

    print("Você está conectado.")

    enviar_thread = threading.Thread(target=enviar_mensagem, args=(conexao,))
    receber_thread = threading.Thread(target=receber_mensagem, args=(conexao,))

    enviar_thread.start()
    receber_thread.start()

    enviar_thread.join()
    receber_thread.join()

if __name__ == '__main__':
    main()
