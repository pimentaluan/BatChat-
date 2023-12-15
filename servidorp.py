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

    conexao.send(bytes("Digite 'registro' para criar uma nova conta ou 'login' para entrar: ", "utf-8"))
    opcao = conexao.recv(Buffer).decode('utf-8').lower()

    if opcao == 'registro':
        registrar_usuario(conexao, username)
    elif opcao == 'login':
        if username in usuarios:
            login_usuario(conexao, username)
        else:
            conexao.send(bytes("Usuário não registrado.", "utf-8"))
            return conexao, ip_cliente, username

    return conexao, ip_cliente, username

def usuario_registrado(username):
    return username in usuarios

def registrar_usuario(conexao, username):
    conexao.send(bytes("Digite sua senha para registro: ", "utf-8"))
    senha = conexao.recv(Buffer).decode('utf-8')

    if usuario_registrado(username):
        conexao.send(bytes("Usuário já registrado. Conexão encerrada.", "utf-8"))
        conexao.close()
    else:
        usuarios[username] = senha
        clientes.append((conexao, username))
        print(f'O usuário {username} foi registrado com sucesso.')
        conexao.send(bytes("Registro bem-sucedido. Agora você pode iniciar uma conversa.", "utf-8"))

def login_usuario(conexao, username):
    conexao.send(bytes("Digite sua senha para login: ", "utf-8"))
    senha = conexao.recv(Buffer).decode('utf-8')

    if usuario_registrado(username) and usuarios[username] == senha:
        clientes.append((conexao, username))
        print(f'O usuário {username} fez login com sucesso.')
        conexao.send(bytes(f"Olá, {username} bem vindo ao BatChat", "utf-8"))
        listening(conexao, username)
    else:
        conexao.send(bytes("Usuário ou senha incorretos. Conexão encerrada.", "utf-8"))
        conexao.close()

def encerrar_conexao(conexao_tcp, username):
    print(f"Encerrando a conexão para {username} e saindo do programa")
    conexao_tcp.close()

def listening(conexao, username):
    while True:
        try:
            receber_mensagem = conexao.recv(Buffer).decode('utf-8')
            if receber_mensagem != '':
                print(receber_mensagem)
                if receber_mensagem.lower() == 'exit':
                    print("O usuário encerrou a conexão.")
                    break
                for cliente in clientes:
                    if cliente[0] != conexao:
                        cliente[0].send(bytes(json.dumps(f"{username}: {receber_mensagem}"), "utf-8"))
        except json.JSONDecodeError:
            continue

    encerrar_conexao(conexao, username)

def handle_client(conexao_corrente, username):
    listening(conexao_corrente, username)

if __name__ == '__main__':
    servidor = conectar_ao_servidor()

    while True:
        conexao_corrente, ip_cliente, username = confirmacao_do_cliente(servidor)
        thread = threading.Thread(target=handle_client, args=(conexao_corrente, username))
        thread.start()

