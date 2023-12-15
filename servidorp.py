import socket
import sys
import threading
import json

Ip_servidor = ''
Porta_servidor = 50000
Buffer = 1024

usuarios = {}
clientes = []

def conectar_ao_servidor():
    conexao_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conexao_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor_socket = (Ip_servidor, Porta_servidor)
    conexao_tcp.bind(servidor_socket)
    conexao_tcp.listen(1)

    return conexao_tcp

def confirmacao_do_cliente(conexao_tcp):
    conexao, ip_cliente = conexao_tcp.accept()
    username = conexao.recv(Buffer).decode('utf-8')

    # Pergunta se é um novo usuário ou um login
    conexao.send(bytes("Digite 'registro' para criar uma nova conta ou 'login' para entrar: ", "utf-8"))
    opcao = conexao.recv(Buffer).decode('utf-8').lower()

    if opcao == 'registro':
        registrar_usuario(conexao, username)
    elif opcao == 'login':
        if username in usuarios:
            login_usuario(conexao, username)
        else:
            conexao.send(bytes("Usuário não registrado. Conexão encerrada.", "utf-8"))
            conexao.close()
    else:
        conexao.send(bytes("Opção inválida. Conexão encerrada.", "utf-8"))
        conexao.close()

def registrar_usuario(conexao, username):
    conexao.send(bytes("Digite sua senha para registro: ", "utf-8"))
    senha = conexao.recv(Buffer).decode('utf-8')

    usuarios[username] = senha
    clientes.append((conexao, username))

    print(f'O usuário {username} foi registrado com sucesso.')
    conexao.send(bytes("Registro bem-sucedido. Agora você pode iniciar uma conversa.", "utf-8"))

def login_usuario(conexao, username):
    conexao.send(bytes("Digite sua senha para login: ", "utf-8"))
    senha = conexao.recv(Buffer).decode('utf-8')

    if usuarios[username] == senha:
        clientes.append((conexao, username))
        print(f'O usuário {username} fez login com sucesso.')
        conexao.send(bytes("Login bem-sucedido. Agora você pode iniciar uma conversa.", "utf-8"))
        return True
    else:
        conexao.send(bytes("Senha incorreta. Conexão encerrada.", "utf-8"))
        conexao.close()
        return False

def encerrar_conexao(conexao_tcp):
    print("Encerrando a conexão e saindo do programa")
    conexao_tcp.close()

def listening(conexao_tcp, username):
    print(f"Começando o BATchat para {username}. Esperando a mensagem...")
    while True:
        try:
            receber_mensagem = json.loads(conexao_tcp.recv(Buffer).decode('utf-8'))
            if receber_mensagem != '':
                print(f'\n{username}: {receber_mensagem}')
                if receber_mensagem.lower() == 'exit':
                    print(f"O usuário {username} encerrou a conexão.")
                    break
                for cliente in clientes:
                    if cliente[1] != username:
                        cliente[0].send(bytes(json.dumps(f"{username}: {receber_mensagem}"), "utf-8"))
        except json.JSONDecodeError:
            continue  # Trata o caso em que a mensagem não é JSON

    encerrar_conexao(conexao_tcp)

def handle_client(conexao_corrente, username):
    if listening(conexao_corrente, username):
        # Somente inicia a conversa se o login for bem-sucedido
        pass

if __name__ == '__main__':
    servidor = conectar_ao_servidor()

    while True:
        conexao_corrente, ip_cliente = confirmacao_do_cliente(servidor)
        thread = threading.Thread(target=handle_client, args=(conexao_corrente, username))
        thread.start()
