import socket
import sys
import json
import threading
from playsound import playsound
import pyttsx3

Server_Port = 50000
Buffer = 1024


def conexao():
    valor = input("Insira o endereço IP para começar a comunicação: ")
    confirmacao = input(f"O destino é {valor}. Certo(s/n)? ")
    if confirmacao in "Ss":
        return iniciar_conexao(valor)
    if confirmacao in "Nn":
        print("Saindo do programa...")
        sys.exit()


def testar_endereco_ip(endereco_ip):
    if len(endereco_ip.split('.')) == 4:
        return True
    print("Encerrando o programa... Confira se o endereço ip está certo")
    sys.exit()


def iniciar_conexao(endereco_ip):
    print("Tentando conectar com o servidor...")
    testar_endereco_ip(endereco_ip)
    conexao_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        destino = (endereco_ip, Server_Port)
        conexao_tcp.connect(destino)
    except ConnectionError as erro:
        print("A conexão foi negada. Tente novamente")

    username = input("\nInsira seu nome de usuário: ")  # Solicita o nome de usuário ao cliente
    conexao_tcp.send(bytes(json.dumps(username), "utf-8"))  # Envia o nome de usuário ao servidor

    return conexao_tcp


def receber_mensagens(conexao_tcp):
    while True:
        receber_mensagem = json.loads(conexao_tcp.recv(Buffer).decode("utf-8"))
        if receber_mensagem != '':
            print(f"Servidor: {receber_mensagem}")
            if receber_mensagem == "exit":
                print('O servidor encerrou a conexão. Quer desconectar também? Digite exit também.')


def conversa(conexao_tcp):
    print("Vamos começar o chat!\n Quando quiser parar, digite exit")

    # Inicia uma nova thread para receber mensagens
    thread = threading.Thread(target=receber_mensagens, args=(conexao_tcp,))
    thread.start()

    while True:
        mensagem = input("\nVocê: ")

        if mensagem != '':
            try:
                conexao_tcp.send(bytes(json.dumps(mensagem), "utf-8"))
            except ConnectionResetError:
                print("A conexão foi encerrada pelo servidor.")

            if mensagem == "exit":
                break


if __name__ == '__main__':

    print("Bem vindo ao BATCHAT! 🦇")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if voice.gender == 'male':
            engine.setProperty('voice', voice.id)
            break
    text = "Bem vindo ao Batichati"
    engine.say(text)
    engine.runAndWait()
    #playsound("Batman Opening and Closing Theme 1966 - 1968 With Snippets (mp3cut.net).mp3")

    conexao = conexao()
    conversa(conexao)

    try:
        conexao.close()
    except ConnectionError as erro:
        print("A conexão TCP foi encerrada")
