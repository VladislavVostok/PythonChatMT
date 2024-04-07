import threading
import socket

class MyServer:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._clients = []
        self._aliases = []
        self.server_init()

    def server_init(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.bind((self._host, self._port))
        self._server.listen()


    def broadcast(self, message):
        for client in self._clients:
            client.send(message)

    # Функция перехватчик события, клиента
    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message)
            except:
                index = self._clients.index(client)
                self._clients[index].close()
                self._clients.remove(client)
                alias = self._aliases[index]
                self.broadcast(f'{alias} вышел из чата!'.encode('utf-8'))
                self._aliases.remove(alias)
                break

    # Главная функция по работе с клиентским приложением
    def receive(self):
        while True:
            print('Сервер работает и прослушивает соединение...')
            client, address = self._server.accept()
            print(f'Соединение с {str(address)} устанавливается!')
            client.send('Ты кто?'.encode('utf-8'))
            alias = client.recv(1024).decode('utf-8')
            self._aliases.append(alias)
            self._clients.append(client)
            print(f'Псевдонимом нового клиента: {alias}')
            self.broadcast(f'{alias} подключился к чату!'.encode('utf-8'))
            client.send('Теперь вы на связи!'.encode('utf-8'))
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()


if __name__ == "__main__":

    server = MyServer("127.0.0.1", 5666)
    server.receive()