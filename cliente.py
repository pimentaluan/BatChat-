# Módulo Cliente
import http.client

def iniciar_cliente():
    host = '192.168.0.3'  # Substitua 'seu_endereco_ip' pelo endereço IP público do servidor
    port = 8000
    conexao = http.client.HTTPConnection(host, port)

    while True:
        comando = input("Digite um comando (ou 'sair' para terminar): ")
        if comando.lower() == 'sair':
            break

        conexao.request("GET", "/" + comando)
        resposta = conexao.getresponse()
        mensagem = resposta.read()
        print('Recebido do servidor:', mensagem)

    conexao.close()

if __name__ == '__main__':
    iniciar_cliente()
