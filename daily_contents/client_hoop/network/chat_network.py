import asyncio
import websockets
import json

class ChatNetworkClient:
    def __init__(self, server_url, client_name):
        self.server_url = server_url
        self.client_name = client_name
        self.websocket = None
        self.messages = []  # 받은 메시지를 저장할 리스트
        self.connected = False  # 웹소켓 연결 상태

    async def connect(self):
        """ WebSocket 서버에 연결 """
        self.websocket = await websockets.connect(f"{self.server_url}/ws/{self.client_name}")
        asyncio.create_task(self.receive_messages())

    async def send_message(self, message):
        """ 서버에 JSON 형식으로 메시지 전송 """
        if self.websocket:
            try:
                json_message = json.dumps({"client_name": self.client_name, "message": message})
                await self.websocket.send(json_message)  # ✅ JSON 형식으로 전송
                print(f"✅ 메시지 전송: {json_message}")
            except Exception as e:
                print(f"❌ 메시지 전송 실패: {e}")

    async def receive_messages(self):
        """ 서버에서 메시지 수신 """
        try:
            while True:
                response = await self.websocket.recv()
                data = json.loads(response)  # ✅ JSON 변환 시도
                self.messages.append(f"{data['client_name']}: {data['message']}")  # 메시지 저장
                print(f"📩 메시지 수신: {data}")
        except Exception as e:
            print(f"Error receiving message: {e}")

    async def disconnect(self):
        """ 서버 연결 종료 """
        if self.websocket:
            await self.websocket.close()
