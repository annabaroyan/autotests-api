import socket
import sys


class TCPClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        """Подключение к серверу"""
        try:
            # Создаем TCP сокет
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Подключаемся к серверу
            self.client_socket.connect((self.host, self.port))
            print(f"Подключено к серверу {self.host}:{self.port}")

            return True

        except ConnectionRefusedError:
            print("Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
            return False
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False

    def send_message(self, message):
        """Отправка сообщения серверу"""
        try:
            # Отправляем сообщение
            self.client_socket.send(message.encode('utf-8'))

            # Получаем ответ от сервера
            response = self.client_socket.recv(4096).decode('utf-8')

            # Выводим ответ сервера
            print("Ответ от сервера:")
            print(response)

        except Exception as e:
            print(f"Ошибка при отправке/получении данных: {e}")

    def close(self):
        """Закрытие соединения"""
        if self.client_socket:
            self.client_socket.close()
            print("Соединение закрыто")


def main():
    # Создаем клиента
    client = TCPClient()

    # Подключаемся к серверу
    if not client.connect():
        sys.exit(1)

    try:
        # Отправляем сообщение (по условию задания)
        message = "Привет, сервер!"
        print(f"Отправляем сообщение: {message}")
        client.send_message(message)

    except KeyboardInterrupt:
        print("\nКлиент остановлен")
    finally:
        # Закрываем соединение
        client.close()


if __name__ == "__main__":
    main()