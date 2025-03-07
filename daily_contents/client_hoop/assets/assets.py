import pygame
import os

# 이미지 & 사운드 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "img")
BGM_DIR = os.path.join(BASE_DIR, "bgm")

# 이미지 로드 함수
def load_image(filename):
    return pygame.image.load(os.path.join(IMG_DIR, filename))

# 사운드 로드 함수
def load_sound(filename):
    return pygame.mixer.Sound(os.path.join(BGM_DIR, filename))

# 📌 모든 이미지 리소스 로드 (딕셔너리로 저장)
IMAGES = {
    "bg_main": load_image("neko_main_bg.png"),
    "bg_explain": load_image("neko_explain_bg.png"),
    "bg_game": load_image("neko_bg.png"),
    "bg_loading": load_image("neko_loading_bg.png"),
    "cursor": load_image("neko_cursor.png"),
    "start_btn": load_image("start.png"),
    "start_btn_hover": load_image("start_click.png"),
    "explain_btn": load_image("explain.png"),
    "explain_btn_hover": load_image("explain_click.png"),
    "back_btn": load_image("back.png"),
    "back_btn_hover": load_image("back_click.png"),
    "neko1": load_image("neko1.png"),
    "neko2": load_image("neko2.png"),
    "neko3": load_image("neko3.png"),
    "neko4": load_image("neko4.png"),
    "neko5": load_image("neko5.png"),
    "neko6": load_image("neko6.png"),
    "neko_niku": load_image("neko_niku.png"),
    "chat_bg" : load_image("chat_bg.png"),
}

# 📌 모든 사운드 리소스 로드
SOUNDS = {
    "bgm_main": load_sound("hot-air-balloon-flight-148232.mp3"),
    "bgm_game1": load_sound("8-bit-cartoon-comedy-by-prettysleepy-art-12290.mp3"),
    "bgm_game2": load_sound("kim-lightyear-you-and-i-161104.mp3"),
    "bgm_game3": load_sound("area12-131883.mp3"),
    "countdown": load_sound("effect/countdown_bgm.mp3"),
    "effect1": load_sound("effect/buble_1.mp3"),
    "effect2": load_sound("effect/buble_2.mp3"),
    "effect3": load_sound("effect/buble_3.mp3"),
}
