import asyncio
import json
import websockets

class GameNetworkClient:
    def __init__(self, server_url, client_name, update_ui_callback, game_ui):
        self.server_url = server_url
        self.client_name = client_name
        self.websocket = None
        self.connected = False
        self.players = []
        self.scores = []
        self.update_ui_callback = update_ui_callback  # ✅ UI 업데이트 함수 저장
        self.loop = asyncio.new_event_loop()
        self.game_ui = game_ui

        # ✅ asyncio 이벤트 루프 설정
        try:
            self.loop = asyncio.get_running_loop()
        except RuntimeError:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

    async def connect(self):
        """ 게임 서버에 WebSocket 연결 """
        try:
            self.websocket = await websockets.connect(f"{self.server_url}/ws/{self.client_name}")
            self.connected = True  # ✅ 연결 성공 시 True 설정
            # print(f"✅ 게임 서버 연결됨: {self.client_name}, connected: {self.connected}")
            asyncio.create_task(self.receive_messages())  
        except Exception as e:
            ...# print(f"❌ WebSocket 연결 실패: {e}")

    async def send_ready(self, ready_status: bool):
        """ READY 상태를 서버로 전송 """
        # print("🚀 send_ready 함수 실행됨!")

        if self.websocket is None:
            # print("❌ WebSocket이 None입니다! 서버에 READY 상태를 보낼 수 없습니다.")
            return

        try:
            message = json.dumps({"event": "READY", "client_name": self.client_name, "ready": ready_status})
            # print(f"📤 서버로 보낼 메시지: {message}")  # ✅ 전송할 JSON 데이터 확인
            await self.websocket.send(message)
            # print(f"✅ READY 상태 전송 완료: {message}")

        except Exception as e:
            ...# import traceback
            # print("❌ send_ready 실행 중 오류 발생:")
            # traceback.print_exc()  # 🔥 예외 전체 출력 (보다 자세한 오류 확인)

    async def send_finish(self, score):
        """게임 종료 후 점수 전송"""
        if self.websocket:
            message = json.dumps({"event": "FINISH", "client_name": self.client_name, "score": score})
            await self.websocket.send(message)
            # print(f"✅ 게임 종료 점수 전송 완료: {message}")

    async def receive_messages(self):
        """ 서버에서 메시지 수신 및 처리 """
        try:
            while True:
                response = await self.websocket.recv()
                data = json.loads(response)
                event_type = data.get("event")

                # ✅ 접속 중인 플레이어 리스트 업데이트
                if event_type == "PLAYER_LIST":
                    self.players = data.get("players", [])
                    # print(f"📜 현재 플레이어 목록: {self.players}")

                    # ✅ GameUI의 update_players() 호출
                    if self.update_ui_callback:
                        self.update_ui_callback(self.players)

                elif event_type == "GAME_START":
                    # print("🔥 게임 시작! 모든 플레이어 준비 완료!")
                    asyncio.run_coroutine_threadsafe(
                        self.game_ui.start_game(), self.game_ui.game_loop
                    )

                elif event_type == "SCORE_UPDATE":
                    """🔥 점수 업데이트 (랭킹 수신)"""
                    self.scores = data.get("scores", [])
                    # # print(f"🏆 최신 랭킹 업데이트: {self.scores}")

                    # ✅ 점수를 내림차순으로 정렬
                    self.scores.sort(key=lambda x: x["score"], reverse=True)

                    if hasattr(self.game_ui, "update_ranking"):
                        self.game_ui.update_ranking(self.scores)  # 🔥 그냥 직접 실행


        except Exception as e:
            ...# print(f"❌ 메시지 수신 오류: {e}")

    async def disconnect(self):
        """ WebSocket 연결 종료 """
        if self.websocket:
            await self.websocket.close()