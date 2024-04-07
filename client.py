


# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
# sock.bind(('', 55000))  # связываем сокет с портом, где он будет ожидать сообщения
# sock.listen(10)  # указываем сколько может сокет принимать соединений
# print('Server is running, please, press ctrl+c to stop')
# while True:
#     conn, addr = sock.accept()  # начинаем принимать соединения
#     print('connected:', addr)  # выводим информацию о подключении
#     data = conn.recv(1024)  # принимаем данные от клиента, по 1024 байт
#     print(str(data))
#     conn.send(data.upper())  # в ответ клиенту отправляем сообщение в верхнем регистре
# conn.close()  # закрываем соединение



# import socket

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создаем сокет
# sock.connect(('localhost', 55000))  # подключемся к серверному сокету
# sock.send(bytes('Hello, world', encoding = 'UTF-8'))  # отправляем сообщение
# data = sock.recv(1024)  # читаем ответ от серверного сокета
# sock.close()  # закрываем соединение
# print(data)

import threading
import socket

class MyClient:
    def __init__(self, host, port, alias):
        self._host = host
        self._port = port
        self._alias = alias
        self.create_connect()

    def create_connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self._host, self._port))

    def client_receive(self):
        while True:
            try:
                message = self.client.recv(1024)
                if message.decode('utf-8') == "Ты кто?":
                    self.client.send(self._alias.encode('utf-8'))
                else:
                    if(not message.decode('utf-8').startswith(self._alias)):
                        print(message.decode('utf-8'))
            except:
                print('Error!')
                self.client.close()
                break
             
    def client_send(self):
        try:
            while True:
                message = f'{self._alias}: {input("")}'
                self.client.send(message.encode('utf-8'))
        except EOFError:
            pass

if __name__ == "__main__":
    try:
        #client = MyClient("213.226.126.185", 5666, "Илья")
        client = MyClient("localhost", 5666, "Илья")
        
        receive_thread = threading.Thread(target=client.client_receive)
        receive_thread.start()

        send_thread = threading.Thread(target=client.client_send)
        send_thread.start()
    except KeyboardInterrupt:
        receive_thread._stop()
        send_thread._stop()