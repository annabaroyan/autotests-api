import asyncio
import websockets


async def client():
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as websocket:
        # Отправляем сообщение серверу
        message = "Привет, сервер!"
        await websocket.send(message)
        print(f"Отправлено сообщение: {message}")

        # Получаем 5 ответных сообщений
        for _ in range(5):
            response = await websocket.recv()
            print(f"Получено от сервера: {response}")


if __name__ == "__main__":
    asyncio.run(client())