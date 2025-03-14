import pygame
import asyncio
import threading
from resources.components.ui_components import InputBox
import textwrap  # 🔥 긴 텍스트를 자동으로 줄바꿈하는 라이브러리 추가

class ChatUI:
    def __init__(self, x, y, width, height, font, chat_network, client_name):
        self.rect = pygame.Rect(x, y, width, height)  # 채팅창 위치 및 크기
        self.font = font
        self.chat_network = chat_network
        self.client_name = client_name  # 클라이언트 이름 저장
        self.input_box = None  # 초기에는 None (연결 후 생성)
        self.connected = False  # 웹소켓 연결 여부
        
        # ✅ 별도의 asyncio 루프를 실행하는 스레드 생성
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.run_event_loop, daemon=True)
        self.thread.start()

        self.line_height = font.get_height() + 5  # 줄 높이 설정
        self.chat_padding = 10  # 채팅 텍스트와 창 사이 간격
        self.max_text_width = width - 20  # 최대 텍스트 너비 (좌우 여백 고려)

    def wrap_text(self, text):
        """🔥 긴 텍스트를 채팅창 너비에 맞춰 여러 줄로 나누는 함수"""
        words = text.split(" ")  # 띄어쓰기를 기준으로 단어를 나눔
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            test_width, _ = self.font.size(test_line)

            if test_width <= self.max_text_width:  # 한 줄에 넣을 수 있으면 추가
                current_line = test_line
            else:  # 초과하면 줄 바꿈
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)  # 마지막 줄 추가

        return lines

    def run_event_loop(self):
        """백그라운드에서 asyncio 이벤트 루프 실행"""
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def handle_event(self, event):
        """채팅 입력창 이벤트 처리"""
        if self.input_box and self.connected:
            result = self.input_box.handle_event(event)
            if result is not None:  # 엔터 입력 시 메시지 전송
                # print(f"🎯 입력된 메시지: {result}")  # ✅ 메시지가 정상적으로 감지되는지 확인

                if not self.chat_network:
                    # print(f"❌ 채팅 네트워크가 None입니다. 메시지 전송 불가")
                    return  # ✅ 채팅 네트워크가 없으면 실행 중단

                if not self.chat_network.connected:
                    # print("❌ 서버와 연결되지 않음. 연결을 먼저 시도해야 합니다.")
                    return  # ✅ 서버와 연결되지 않았다면 메시지 전송 X

                # ✅ 비동기 메시지 전송
                message = f"{result}"
                future = asyncio.run_coroutine_threadsafe(self.chat_network.send_message(message), self.loop)

                try:
                    future.result()  # 실행 결과 확인 (예외 발생 시 확인 가능)
                    # print(f"✅ 메시지 전송 요청됨: {message}")
                except Exception as e:
                    ...# print(f"❌ 메시지 전송 실패: {e}")

                # ✅ 메시지 전송 후 입력창 비우기
                self.input_box.text = ""


    def draw(self, screen):
        """채팅 UI 그리기"""
        pygame.draw.rect(screen, (230, 230, 230), self.rect)  # 채팅 배경

        # 받은 메시지 출력 (최대 10개)
        if self.chat_network and self.chat_network.messages:
            y_offset = self.chat_padding  # 첫 번째 메시지의 Y 위치 조정

            for msg in self.chat_network.messages[-10:]:
                wrapped_lines = self.wrap_text(msg)  # ✅ 줄바꿈 적용

                for line in wrapped_lines:
                    text_surface = self.font.render(line, True, (0, 0, 0))
                    screen.blit(text_surface, (self.rect.x + self.chat_padding, self.rect.y + y_offset))
                    y_offset += self.line_height  # 줄 간격 조정

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
        # print("연결완료")
