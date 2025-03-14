import pygame

# 📌 이미지 & 사운드 리소스 로드 (상대 경로 사용)
img_neko = [
    None,
    pygame.image.load("./resources/assets/img/neko1.png"),
    pygame.image.load("./resources/assets/img/neko2.png"),
    pygame.image.load("./resources/assets/img/neko3.png"),
    pygame.image.load("./resources/assets/img/neko4.png"),
    pygame.image.load("./resources/assets/img/neko5.png"),
    pygame.image.load("./resources/assets/img/neko6.png"),
    pygame.image.load("./resources/assets/img/neko_niku.png")
]

IMAGES = {
    "bg_main": pygame.image.load("./resources/assets/img/neko_main_bg.png"),
    "bg_explain": pygame.image.load("./resources/assets/img/neko_explain_bg.png"),
    "bg_game": pygame.image.load("./resources/assets/img/neko_bg.png"),
    "bg_loading": pygame.image.load("./resources/assets/img/neko_loading_bg.png"),
    "cursor": pygame.image.load("./resources/assets/img/neko_cursor.png"),
    "start_btn": pygame.image.load("./resources/assets/img/start.png"),
    "start_btn_hover": pygame.image.load("./resources/assets/img/start_click.png"),
    "explain_btn": pygame.image.load("./resources/assets/img/explain.png"),
    "explain_btn_hover": pygame.image.load("./resources/assets/img/explain_click.png"),
    "back_btn": pygame.image.load("./resources/assets/img/back.png"),
    "back_btn_hover": pygame.image.load("./resources/assets/img/back_click.png"),
    "neko1": pygame.image.load("./resources/assets/img/neko1.png"),
    "neko2": pygame.image.load("./resources/assets/img/neko2.png"),
    "neko3": pygame.image.load("./resources/assets/img/neko3.png"),
    "neko4": pygame.image.load("./resources/assets/img/neko4.png"),
    "neko5": pygame.image.load("./resources/assets/img/neko5.png"),
    "neko6": pygame.image.load("./resources/assets/img/neko6.png"),
    "neko_niku": pygame.image.load("./resources/assets/img/neko_niku.png"),
    "chat_bg": pygame.image.load("./resources/assets/img/chat_bg.png"),
    "neko_ranking": pygame.image.load("./resources/assets/img/neko_ranking_bg.png")
}

SOUNDS = {
    "bgm_main": pygame.mixer.Sound("./resources/assets/bgm/hot-air-balloon-flight-148232.mp3"),
    "bgm_game1": pygame.mixer.Sound("./resources/assets/bgm/8-bit-cartoon-comedy-by-prettysleepy-art-12290.mp3"),
    "bgm_game2": pygame.mixer.Sound("./resources/assets/bgm/kim-lightyear-you-and-i-161104.mp3"),
    "bgm_game3": pygame.mixer.Sound("./resources/assets/bgm/area12-131883.mp3"),
    "countdown": pygame.mixer.Sound("./resources/assets/bgm/effect/countdown_bgm.mp3"),
    "effect1": pygame.mixer.Sound("./resources/assets/bgm/effect/buble_1.mp3"),
    "effect2": pygame.mixer.Sound("./resources/assets/bgm/effect/buble_2.mp3"),
    "effect3": pygame.mixer.Sound("./resources/assets/bgm/effect/buble_3.mp3"),
}

yaong = [
    pygame.mixer.Sound("./resources/assets/bgm/server/yaong_1.mp3"),
    pygame.mixer.Sound("./resources/assets/bgm/server/yaong_2.mp3"),
    pygame.mixer.Sound("./resources/assets/bgm/server/yaong_3.mp3"),
    pygame.mixer.Sound("./resources/assets/bgm/server/yaong_4.mp3"),
    pygame.mixer.Sound("./resources/assets/bgm/server/yaong_5.mp3"),
    pygame.mixer.Sound("./resources/assets/bgm/server/yaong_6.mp3"),
    pygame.mixer.Sound("./resources/assets/bgm/server/yaong_7.mp3")
]
