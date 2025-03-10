import asyncio
import json
import redis.asyncio as redis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

# Redis 설정
REDIS_HOST = "localhost"
REDIS_PORT = 6379
CHANNEL_NAME = "chat_channel"

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
active_connections = {}  # 현재 연결된 클라이언트

async def redis_subscriber(websocket: WebSocket):
    """ Redis Pub/Sub 구독 (서버 → 클라이언트 메시지 전송) """
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(CHANNEL_NAME)

    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                await websocket.send_text(message["data"])  # JSON 메시지 전송
    except Exception as e:
        print(f"[❌ Redis Subscription Error]: {e}")
    finally:
        await pubsub.unsubscribe(CHANNEL_NAME)

@app.websocket("/ws/{client_name}")
async def websocket_endpoint(websocket: WebSocket, client_name: str):
    """ WebSocket 연결 관리 """
    print(f"📡 새로운 WebSocket 연결 요청: {client_name}")  # ✅ 로그 추가
    await websocket.accept()  # 연결 수락
    active_connections[client_name] = websocket
    print(f"🔵 {client_name} connected!")  # ✅ 연결 성공 시 출력되는 로그

    # ✅ JSON 형식으로 클라이언트에게 "CONNECTED" 메시지 전송
    connected_message = json.dumps({"system": "CONNECTED", "client_name": client_name})
    await websocket.send_text(connected_message)

    asyncio.create_task(redis_subscriber(websocket))  # ✅ Redis Pub/Sub 구독

    try:
        while True:
            data = await websocket.receive_text()  # ✅ 메시지 수신
            print(f"📩 수신된 메시지 원본: {data}")  # ✅ 원본 로그 추가

            try:
                parsed_data = json.loads(data)  # ✅ JSON 파싱
                sender = parsed_data.get("client_name", "Unknown")
                message_text = parsed_data.get("message", "")

                if message_text.strip():  # 빈 메시지는 무시
                    redis_message = json.dumps({"client_name": sender, "message": message_text})
                    await redis_client.publish(CHANNEL_NAME, redis_message)  # ✅ Redis에 메시지 발행
                    print(f"✅ Redis에 저장됨: {redis_message}")
                else:
                    print("⚠️ 빈 메시지가 수신됨, 무시합니다.")

            except json.JSONDecodeError:
                print(f"❌ JSON 디코드 오류: {data}")

    except WebSocketDisconnect:
        print(f"🔴 {client_name} disconnected")
        del active_connections[client_name]  # 클라이언트 제거
    except Exception as e:
        print(f"[❌ WebSocket Error]: {e}")


    except WebSocketDisconnect:
        print(f"🔴 {client_name} disconnected")
        del active_connections[client_name]
    except Exception as e:
        print(f"[❌ WebSocket Error]: {e}")

@app.get("/")
async def home():
    return HTMLResponse("<h1>FastAPI WebSocket Chat Server</h1>")
