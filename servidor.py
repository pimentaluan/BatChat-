# Módulo Servidor
import socket
import threading
import json

class Server:
    def __init__(self, host = 'localhost', port = 5000):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.clients = []
        self.lock = threading.Lock()

    def broadcast(self, message, source):
        with self.lock:
            for client in self.clients:
                if client != source:
                    client.send(message)

    def handle(self, client):
        while True:
            try:
                message = client.recv(1024)
                message = json.loads(message.decode())
                print(f"{message['username']}: {message['message']}")
                self.broadcast(message, client)
            except:
                with self.lock:
                    self.clients.remove(client)
                client.close()
                break

    def run(self):
        while True:
            client, address = self.server.accept()
            with self.lock:
                self.clients.append(client)
            print(f"Conexão estabelecida com {str(address)}")
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()