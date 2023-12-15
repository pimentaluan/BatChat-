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
            print("Esse IP não corresponde ao do servidor. Tente novamente.")

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
        except ConnectionResetError:
            break

def main():
    try:
        conexao = conectar_ao_servidor()
        escolha = input("Digite 'REGISTRAR' para criar uma nova conta ou 'ENTRAR' para entrar: ").lower()
        conexao.send(bytes(escolha, "utf-8"))

        if escolha == 'registrar':
            nome = input('Digite o nome do usuário para registro: ')
            senha = input("Digite sua senha para registro: ")
            conexao.send(bytes(nome, "utf-8"))
            conexao.send(bytes(senha, "utf-8"))
            
            # Receber resposta do servidor após o registro
            resposta_registro = conexao.recv(Buffer).decode('utf-8')
            print(resposta_registro)

        elif escolha == 'entrar':
            username = input("Digite seu nome de usuário: ")
            senha = input('Digite sua senha: ')
            conexao.send(bytes(username, "utf-8"))
            conexao.send(bytes(senha, "utf-8"))
            resposta_login = conexao.recv(Buffer).decode('utf-8').lower()

            if "bem-vindo" in resposta_login:
                print(resposta_login)

                # Iniciar threads de envio e recebimento apenas após o login
                enviar_thread = threading.Thread(target=enviar_mensagem, args=(conexao,))
                receber_thread = threading.Thread(target=receber_mensagem, args=(conexao,))

                enviar_thread.start()
                receber_thread.start()

                enviar_thread.join()
                receber_thread.join()

            else:
                print("Você precisa criar uma conta.")
                return

    except KeyboardInterrupt:
        print("Cliente encerrado.")

if __name__ == '__main__':
    main()


