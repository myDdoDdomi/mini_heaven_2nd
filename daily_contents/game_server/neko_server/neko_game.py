import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

# ✅ 게임 상태 관리
active_players = {}  # 현재 접속한 클라이언트 목록
ready_players = set()  # 준비 완료된 플레이어 목록
finished_players = []  # 게임을 끝낸 플레이어들의 점수 목록
game_active = False  # ✅ 게임이 진행 중인지 여부 (False: 새 접속 가능, True: 접속 차단)

@app.websocket("/ws/{player_name}")
async def websocket_endpoint(websocket: WebSocket, player_name: str):
    """WebSocket을 통한 플레이어 연결 관리"""
    global game_active

    if game_active:
        # 🔴 게임이 진행 중이면 새로운 접속 차단
        await websocket.close()
        print(f"🚫 {player_name}의 접속이 차단됨 (게임 진행 중)")
        return

    print(f"🎮 새로운 플레이어 접속: {player_name}")
    await websocket.accept()
    active_players[player_name] = websocket

    # ✅ 연결된 클라이언트에게 "CONNECT" 이벤트 전송
    await websocket.send_text(json.dumps({"event": "CONNECT", "player_name": player_name}))
    
    # ✅ 모든 클라이언트에게 현재 접속 중인 플레이어 목록 전송
    await broadcast({"event": "PLAYER_LIST", "players": list(active_players.keys())})

    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 {player_name}로부터 받은 데이터: {data}")

            try:
                parsed_data = json.loads(data)
                event_type = parsed_data.get("event")

                # ✅ 클라이언트가 "READY" 상태를 보냈을 경우
                if event_type == "READY":
                    ready_players.add(player_name)
                    print(f"✅ {player_name} 준비 완료!")

                    # 🔥 모든 플레이어가 준비 완료 상태이면 게임 시작
                    if len(ready_players) == len(active_players):
                        game_active = True  # ✅ 게임이 시작되면 새로운 접속 차단
                        print("🎮 게임 시작!")
                        await broadcast({"event": "GAME_START"})

                # ✅ 클라이언트가 "FINISH" 이벤트를 보냈을 경우 (게임 종료)
                elif event_type == "FINISH":
                    score = parsed_data.get("score", 0)
                    finished_players.append({"player_name": player_name, "score": score})
                    print(f"🎯 {player_name} 게임 종료! 점수: {score}")

                    # 🔥 점수 내림차순 정렬
                    sorted_scores = sorted(finished_players, key=lambda x: x["score"], reverse=True)

                    # ✅ 게임을 완료한 유저들에게만 점수 업데이트 메시지 전송
                    await send_to_finished_players({"event": "SCORE_UPDATE", "scores": sorted_scores})

                    # ✅ 게임 종료 체크
                    await check_game_end()

            except json.JSONDecodeError:
                print(f"❌ JSON 디코드 오류: {data}")

    except WebSocketDisconnect:
        # ✅ 플레이어가 연결을 끊었을 때 처리
        await disconnect_player(player_name)

async def disconnect_player(player_name: str):
    """🔥 플레이어가 나갔을 때 처리"""
    if player_name in active_players:
        del active_players[player_name]
    
    ready_players.discard(player_name)
    finished_players[:] = [p for p in finished_players if p["player_name"] != player_name]

    print(f"🔴 {player_name} 접속 종료")
    await broadcast({"event": "PLAYER_LIST", "players": list(active_players.keys())})

    # ✅ 게임 종료 체크 (모든 플레이어가 게임을 끝냈다면 초기화)
    await check_game_end()

async def check_game_end():
    """🔥 모든 유저가 게임을 끝냈는지 확인하고, 게임을 리셋할지 결정"""
    global game_active

    # ✅ 모든 플레이어가 게임을 끝냈다면 (접속한 모든 플레이어가 FINISH 상태여야 함)
    if len(finished_players) == len(active_players):
        print("🏆 모든 플레이어가 게임을 종료했습니다! 점수 초기화 후 새로운 게임 가능")
        
        # ✅ 점수 초기화 및 게임 상태 리셋
        finished_players.clear()
        ready_players.clear()
        game_active = False  # ✅ 새로운 플레이어 접속 허용

        # ✅ 모든 클라이언트에게 점수 초기화 메시지 전송
        await broadcast({"event": "GAME_RESET"})

async def send_to_finished_players(message: dict):
    """🔥 게임을 완료한 유저들에게만 메시지 전송"""
    data = json.dumps(message)
    for player_data in finished_players:
        player_name = player_data["player_name"]
        if player_name in active_players:
            try:
                await active_players[player_name].send_text(data)
            except Exception as e:
                print(f"❌ {player_name}에게 메시지 전송 실패: {e}")

async def broadcast(message: dict):
    """🔥 모든 플레이어에게 메시지 전송"""
    data = json.dumps(message)
    for player, ws in active_players.items():
        try:
            await ws.send_text(data)
        except Exception as e:
            print(f"❌ {player}에게 메시지 전송 실패: {e}")

@app.get("/")
async def home():
    return HTMLResponse("<h1>FastAPI WebSocket Game Server</h1>")
