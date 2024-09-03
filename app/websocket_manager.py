
import uuid

import websockets
import json
import time

class WebSocketManager:
    def __init__(self, token):
        self.token = token
        self.url = f"wss://socket.tidio.co/socket.io/?transport=websocket"
        # self.url = f"wss://socket.tidio.co/socket.io/?ppk={self.token}&device=desktop&EIO=3&transport=websocket"
        self.websocket = None

    async def connection(self):
        try:
            self.websocket = await websockets.connect(self.url)
            print("Connected to WebSocket")
        except Exception as e:
            print(f"Connection error: {e}")

    async def disconnection(self):
        if self.websocket:
            await self.websocket.close()
            print("WebSocket closed")

    async def sender(self, message):
        try:
            msg = self._create_message(message)
            await self.websocket.send(msg)
            print(f"Sending message: {msg}")
        except Exception as e:
            print(f"An error occurred while sending message: {e}")

    # def _create_message(self, message):
    #     current_timestamp = int(time.time())
    #     message_details = {
    #         "message": message,
    #         "time": current_timestamp,  # Use current timestamp
    #         "visitorId": "4974a1b424fa4a8bb024cb1708f33b00",
    #         "projectPublicKey": "bvwhj3a0llcvandqbwe0fahqg5lrwsxh",
    #         "device": "desktop"
    #     }
    #     msg = ["visitorIsTyping", message_details, None]
    #     return json.dumps(msg)

    def _create_message(self, message):
        generated_uuid = str(uuid.uuid4())
        message_data = ["visitorNewMessage",{"message" :message, "messageId": f"{generated_uuid}",
                                             "url":"http://localhost:8000/",
                                             "visitorId":"4974a1b424fa4a8bb024cb1708f33b00",
                                             "projectPublicKey":f"{self.token}","device":"desktop"}]

        return json.dumps(message_data)

    async def receiver(self):
        try:
            while True:
                response = await self.websocket.recv()
                print(f"Received: {response}")
                yield response
        except websockets.ConnectionClosed:
            print("WebSocket connection closed")
        except Exception as e:
            print(f"An error occurred while receiving message: {e}")

