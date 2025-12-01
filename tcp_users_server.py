import socket
import threading
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


class TCPServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.messages = []  # Список для хранения истории сообщений
        self.lock = threading.Lock()  # Блокировка для безопасного доступа к списку сообщений
        self.server_socket = None

    def start(self):
        """Запуск TCP сервера"""
        try:
            # Создаем TCP сокет
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Привязываем сокет к адресу и порту
            self.server_socket.bind((self.host, self.port))

            # Начинаем слушать подключения (до 10 в очереди)
            self.server_socket.listen(10)

            logging.info(f"Сервер запущен на {self.host}:{self.port}")
            logging.info("Ожидание подключений...")

            while True:
                # Принимаем новое подключение
                client_socket, client_address = self.server_socket.accept()

                # Логируем подключение
                logging.info(f"Пользователь с адресом: {client_address} подключился к серверу")

                # Создаем поток для обработки клиента
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_address)
                )
                client_thread.daemon = True
                client_thread.start()

        except KeyboardInterrupt:
            logging.info("Сервер остановлен")
        except Exception as e:
            logging.error(f"Ошибка: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()

    def handle_client(self, client_socket, client_address):
        """Обработка клиентского подключения"""
        try:
            while True:
                # Получаем данные от клиента
                data = client_socket.recv(1024)
                if not data:
                    break

                # Декодируем сообщение
                message = data.decode('utf-8').strip()

                # Логируем полученное сообщение
                logging.info(f"Пользователь с адресом: {client_address} отправил сообщение: {message}")

                # Безопасно добавляем сообщение в историю
                with self.lock:
                    self.messages.append(message)

                # Отправляем всю историю сообщений клиенту
                response = '\n'.join(self.messages)
                client_socket.send(response.encode('utf-8'))

        except ConnectionResetError:
            logging.info(f"Клиент {client_address} отключился")
        except Exception as e:
            logging.error(f"Ошибка при обработке клиента {client_address}: {e}")
        finally:
            client_socket.close()


def main():
    server = TCPServer()
    server.start()


if __name__ == "__main__":
    main()