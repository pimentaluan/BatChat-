# Módulo Cliente
class Client:
    def __init__(self, host = 'localhost', port = 5000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send_message(self, username, message):
        message = json.dumps({"username": username, "message": message})
        self.socket.send(message.encode())

    def receive_message(self):
        message = self.socket.recv(1024)
        message = json.loads(message.decode())
        return f"{message['username']}: {message['message']}"