import pygame
import asyncio
from components.ui_components import InputBox

class ChatUI:
    def __init__(self, x, y, width, height, font, chat_network, client_name, loop):
        self.rect = pygame.Rect(x, y, width, height)  # 채팅창 위치 및 크기
        self.font = font
        self.chat_network = chat_network
        self.client_name = client_name  # 클라이언트 이름 저장
        self.input_box = None  # 초기에는 None (연결 후 생성)
        self.connected = False  # 웹소켓 연결 여부
        self.loop = loop  # asyncio 이벤트 루프 저장

    def handle_event(self, event):
        """채팅 입력창 이벤트 처리"""
        if self.input_box and self.connected:
            result = self.input_box.handle_event(event)
            if result is not None:  # 엔터 입력 시 메시지 전송
                if self.chat_network and result.strip():
                    message = f"{self.client_name}: {result}"
                    
                    # ✅ 메시지를 비동기적으로 전송 (future.result() 제거)
                    asyncio.run_coroutine_threadsafe(self.chat_network.send_message(message), self.loop)
                    
                    print(f"✅ 메시지 전송 요청됨: {message}")

                    # ✅ 메시지 전송 후 입력창 비우기
                    self.input_box.text = ""

    def draw(self, screen):
        """채팅 UI 그리기"""
        pygame.draw.rect(screen, (230, 230, 230), self.rect)  # 채팅 배경

        # 받은 메시지 출력 (최대 10개)
        if self.chat_network and self.chat_network.messages:
            y_offset = 10
            for msg in self.chat_network.messages[-10:]:
                text_surface = self.font.render(msg, True, (0, 0, 0))
                screen.blit(text_surface, (self.rect.x + 10, self.rect.y + y_offset))
                y_offset += 25  # 메시지 간격

        # ✅ 웹소켓 연결이 확인되면 입력창을 표시
        if self.connected and self.input_box:
            self.input_box.draw(screen)

    def set_connected(self):
        """웹소켓 연결이 완료되면 호출 (입력창 활성화)"""
        if not self.input_box:
            input_x = self.rect.x + 5  # 입력창이 chat UI 내부에서 정렬되도록 조정
            input_y = self.rect.y + self.rect.height - 45  # 입력창이 chat_height 내에서 하단에 배치
            input_width = self.rect.width - 10  # 입력창이 chat UI 너비를 거의 차지하도록 설정
            input_height = 35  # 적절한 높이 설정
            
            self.input_box = InputBox(input_x, input_y, input_width, input_height, self.font, placeholder="Type a message...")

        self.connected = True
        print("연결완료")
