import numpy as np
import math
from classes import Player
import pygame

def coord(player, v_w, theta_w, k):
    '''
    v_s : 발사 속도 (파워)
    theta_s : 발사 각도
    v_w : 풍속
    theta_w : 풍향
    k : 저항값
    '''
    g = 8
    v_s = player.gauge
    theta_s = player.angle
    
    a_s = math.radians(theta_s)
    a_w = math.radians(theta_w)
    r_sq = math.sqrt(40**2 + 16**2)
    
    cannon_cos = math.cos(round(40 / r_sq, 3))
    cannon_sin = math.sin(round(16 / r_sq, 3))
    
    shot_cos = cannon_cos * math.cos(a_s) - cannon_sin * math.sin(a_s)
    if player.side == 1:
        shot_sin = cannon_sin * math.cos(a_s) + cannon_cos * math.sin(a_s)
    elif player.side == 2:
        shot_sin = math.sin(a_s) * cannon_cos - cannon_sin * math.cos(a_s)
    

    
    
    init_x = player.position[0] + round(r_sq * shot_cos, 2)
    init_y = player.position[1] - round(r_sq * shot_sin, 2)
    h = r_sq * shot_sin
    
    t_end = round(((v_s * math.sin(a_s) - v_w * math.sin(a_w)) + math.sqrt((v_s * math.sin(a_s) - v_w * math.sin(a_w))**2 + 2*g*h)) / g, 2)   # 여기 왜 빠졌지?

    
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
    season = seasonal(turn)
    
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
        
def seasonal(turn):
    if 1 <= turn < 4:
        season = 'spring'
    elif 4 <= turn < 7:
        season = 'summer'
    elif 7 <= turn < 10:
        season = 'autumn'
    else:
        season = 'winter'
    return season
