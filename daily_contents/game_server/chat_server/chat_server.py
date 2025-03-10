import asyncio
import json
import redis.asyncio as redis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

# Redis 연결 설정
REDIS_HOST = "localhost"
REDIS_PORT = 6379
CHANNEL_NAME = "chat_channel"  # Redis에서 사용할 채널 이름

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

# 현재 연결된 WebSocket 클라이언트 리스트
active_connections = {}

async def redis_subscriber(websocket: WebSocket):
    """ Redis Pub/Sub 구독 (서버에서 클라이언트로 메시지 전달) """
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(CHANNEL_NAME)

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"])  # 받은 메시지 전송
    except Exception as e:
        print(f"[❌ Redis Subscription Error]: {e}")
    finally:
        await pubsub.unsubscribe(CHANNEL_NAME)

@app.websocket("/ws/{client_name}")
async def websocket_endpoint(websocket: WebSocket, client_name: str):
    """ WebSocket 연결 관리 """
    await websocket.accept()
    active_connections[client_name] = websocket

    print(f"🔵 {client_name} connected!")

    # ✅ JSON 형식으로 클라이언트에게 "CONNECTED" 메시지 전송
    connected_message = json.dumps({"system": "CONNECTED", "client_name": client_name})
    await websocket.send_text(connected_message)

    # Redis Pub/Sub 메시지 리스너 실행
    asyncio.create_task(redis_subscriber(websocket))

    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 수신된 메시지: {data}")  # ✅ 디버깅용 로그 추가

            # ✅ JSON 형식인지 확인 후 처리
            try:
                parsed_data = json.loads(data)
                client_name = parsed_data.get("client_name", "Unknown")
                message_text = parsed_data.get("message", "")

                if message_text.strip():  # 빈 메시지는 무시
                    message = json.dumps({"client_name": client_name, "message": message_text})
                    await redis_client.publish(CHANNEL_NAME, message)  # ✅ Redis에 메시지 발행
                    print(f"✅ Redis에 저장됨: {message}")
            except json.JSONDecodeError:
                print(f"❌ JSON 디코드 오류: {data}")

    except WebSocketDisconnect:
        print(f"🔴 {client_name} disconnected")
        del active_connections[client_name]  # 클라이언트 제거
    except Exception as e:
        print(f"[❌ WebSocket Error]: {e}")

@app.get("/")
async def home():
    return HTMLResponse("<h1>FastAPI WebSocket Chat Server</h1>")

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
        await asyncio.sleep(1)  # ✅ 연결 후 메시지 수신을 안정적으로 하기 위해 약간의 지연 추가
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
                try:
                    data = json.loads(response)  # JSON 형식으로 변환
                except json.JSONDecodeError:
                    print(f"❌ JSON 디코드 실패: {response}")
                    continue  # JSON이 아닌 경우 무시

                # ✅ 시스템 메시지 처리 (연결 확인)
                if "system" in data and data["system"] == "CONNECTED":
                    print(f"✅ WebSocket 연결됨: {data['client_name']}")
                    self.connected = True  # 연결 상태 업데이트
                    continue  # 연결 확인 메시지는 저장하지 않음

                # "client_name: message" 형식으로 저장
                formatted_message = f"{data['client_name']}: {data['message']}"
                self.messages.append(formatted_message)
        except Exception as e:
            print(f"Error receiving message: {e}")

    async def disconnect(self):
        """ 서버 연결 종료 """
        if self.websocket:
            await self.websocket.close()