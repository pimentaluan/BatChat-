# Módulo Servidor
from http.server import BaseHTTPRequestHandler, HTTPServer
from cryptography.fernet import Fernet

chave = Fernet.generate_key()  # Gera uma chave de criptografia
criptografia = Fernet(chave)

class Servidor(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        mensagem = "Olá, Cliente!"
        mensagem_criptografada = criptografia.encrypt(mensagem.encode())  # Criptografa a mensagem
        self.wfile.write(mensagem_criptografada)
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        if post_data.decode() == 'stop':
            print("Comando 'stop' recebido, finalizando a conexão...")
            self.server.shutdown()

def iniciar_servidor():
    host = '192.168.0.3'  # Substitua 'seu_endereco_ip' pelo endereço IP público da sua máquina
    port = 8000
    servidor = HTTPServer((host, port), Servidor)
    print('Servidor iniciado...')
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    servidor.server_close()

if __name__ == '__main__':
    iniciar_servidor()
