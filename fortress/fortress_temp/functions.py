import numpy as np
import math
from classes import Player

def coord(v_s, theta_s, v_w, theta_w, k, init_x, init_y):
    '''
    v_s : 발사 속도 (파워)
    theta_s : 발사 각도
    v_w : 풍속
    theta_w : 풍향
    k : 저항값
    '''
    g = 9.8
    a_s = math.radians(theta_s)
    a_w = math.radians(theta_w)
    
    t_end = round(2 * (v_s * math.sin(a_s) - v_w * math.sin(a_w)) / g, 2)
    
    x = []
    y = []
    t_list = list(np.arange(0, t_end, 0.1))
    t_list.append(t_end)
    
    for i in range(len(t_list)):
        t = t_list[i]
        x_coord = round((v_s * math.cos(a_s) * t + v_w * math.cos(a_w) * t) * (1-k), 2) + init_x
        y_coord = -round((v_s * math.sin(a_s) * t - (1/2)*g*(t**2) - v_w * math.sin(a_w) * t), 2) + init_y
        x.append(x_coord)
        y.append(y_coord)
    
    return x, y

def environ(turn):
    '''
    턴 수에 따라 계절 산출, 계절에 따른 풍속, 풍향, 저항, 데미지 배율 설정
    '''
    if 1 <= turn < 4:
        season = 'spring'
    elif 4 <= turn < 7:
        season = 'summer'
    elif 7 < turn < 10:
        season = 'autumn'
    else:
        season = 'winter'
    
    if season == 'spring':
        wind_velocity = list(range(10))
        wind_angle = list(range(0, 190, 10))
        resistance = 0
        damage_scale = 1
    elif season == 'summer':
        wind_velocity = list(range(20))
        wind_angle = list(range(0, 190, 10))
        resistance = 0.2
        damage_scale = 0.7
    elif season == 'autumn':
        wind_velocity = list(range(10))
        wind_angle = list(range(0, 190, 10))
        resistance = 0
        damage_scale = 2
    elif season == 'winter':
        wind_velocity = list(range(20))
        wind_angle = list(range(0, 190, 10))
        resistance = 0.1
        damage_scale = 1.2
    
    v_w = wind_velocity[np.random.randint(0, len(wind_velocity)-1)]
    theta_w = wind_angle[np.random.randint(0, len(wind_angle)-1)]
    
    return v_w, theta_w, resistance, damage_scale

# if idx -> -1
def calculation(impact, player):
    # player = Player(wheel, side)
    if impact-player.volume <= player.position[0] <= impact+player.volume:
        player.hit()
