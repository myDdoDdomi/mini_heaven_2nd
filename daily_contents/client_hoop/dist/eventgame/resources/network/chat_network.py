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
        try:
            self.websocket = await websockets.connect(f"{self.server_url}/ws/{self.client_name}")
            # print(f"✅ WebSocket 연결됨: {self.client_name}")  # ✅ 연결 로그 추가
            self.connected = True  # ✅ 연결 상태 업데이트
            await asyncio.sleep(1)  # ✅ 안정적인 연결을 위해 지연 추가
            asyncio.create_task(self.receive_messages())
        except Exception as e:
            ...# print(f"❌ WebSocket 연결 실패: {e}")

    async def send_message(self, message):
        """ 서버에 JSON 형식으로 메시지 전송 """
        if self.websocket:
            try:
                json_message = json.dumps({"client_name": self.client_name, "message": message})
                # print(f"📤 전송되는 메시지: {json_message}")  # ✅ 실제 전송되는 데이터 확인
                await self.websocket.send(json_message)  # ✅ JSON 형식으로 전송
                # print(f"✅ 메시지 전송 완료: {json_message}")
            except Exception as e:
                ...# print(f"❌ 메시지 전송 실패: {e}")

    async def receive_messages(self):
        """ 서버에서 메시지 수신 """
        try:
            while True:
                response = await self.websocket.recv()
                data = json.loads(response)  # ✅ JSON 변환 시도
                
                # ✅ 시스템 메시지 처리
                if "system" in data and data["system"] == "CONNECTED":
                    # print(f"✅ 서버 연결 확인 메시지 수신: {data}")  # ✅ 연결 메시지 확인 로그 추가
                    self.connected = True  # ✅ 연결 상태 업데이트
                    continue  # 일반 메시지로 저장하지 않음

                # ✅ 일반 채팅 메시지 처리
                if "client_name" in data and "message" in data:
                    formatted_message = f"{data['client_name']}: {data['message']}"
                    self.messages.append(formatted_message)  # ✅ 채팅 메시지 저장
                    # print(f"📩 메시지 수신: {formatted_message}")

        except Exception as e:
            ...# print(f"Error receiving message: {e}")

    async def disconnect(self):
        """ 서버 연결 종료 """
        if self.websocket:
            await self.websocket.close()
