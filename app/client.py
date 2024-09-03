import asyncio
from app.websocket_manager import WebSocketManager

class TidioClient:
    def __init__(self, token):
        self.token = token
        self.websocket_manager = WebSocketManager(self.token)

    async def send_message(self, message):
        await self.websocket_manager.sender(message)

    async def receive_messages(self):
        async for message in self.websocket_manager.receiver():
            print(f"Received: {message}")

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.websocket_manager.connection())
        try:
            while True:
                message = input("Enter message to send: ")
                if message.lower() == "exit":
                    break
                print(f"message::: {message}")
                loop.run_until_complete(self.send_message(message))
                loop.run_until_complete(self.receive_messages())
        except KeyboardInterrupt:
            print("Interrupted by user")
        finally:
            loop.run_until_complete(self.websocket_manager.disconnection())
