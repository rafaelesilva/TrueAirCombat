import pygame

pygame.init()
info = pygame.display.Info()

if info.current_w < info.current_h:
    REAL_WIDTH = info.current_h
    REAL_HEIGHT = info.current_w
else:
    REAL_WIDTH = info.current_w
    REAL_HEIGHT = info.current_h

WIDTH = 640
HEIGHT = 360
MAP_WIDTH = 2048 
MAP_HEIGHT = 2048

TITLE = "Air Combat Strike"
FPS = 30
SCALE = 1.0 
SCROLL_SPEED = 2 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GREY = (100, 100, 100)
SMOKE = (200, 200, 200)
RADAR_BG = (0, 20, 0, 150) 
RADAR_BORDER = (0, 255, 0)

# --- CONFIGURAÇÃO DE ALVOS TERRESTRES ---
# Removida a entrada 'BRIDGE'
TARGET_DATA = {
    'RADAR':  {'hp': 100, 'score': 200, 'color': (150, 150, 150), 'size': (40, 40), 'shape': 'CIRCLE'},
    'BUNKER': {'hp': 300, 'score': 500, 'color': (100, 100, 80),  'size': (60, 50), 'shape': 'RECT'},
    'FACTORY':{'hp': 400, 'score': 600, 'color': (120, 100, 100), 'size': (80, 70), 'shape': 'RECT'}
}

AIRCRAFT_DATA = {
    'Gripen F-39E': {'hp': 100, 'speed': 6, 'prefix': 'gripen', 'scale': 0.9, 'loadout': ['VULCAN', 'METEOR', 'MK-82']},
    'F-16 Viper':   {'hp': 80,  'speed': 7, 'prefix': 'f16',    'scale': 0.9, 'loadout': ['VULCAN', 'AIM-120', 'MK-82']},
    'Su-35 Flanker':{'hp': 110, 'speed': 5.5,'prefix': 'su35',  'scale': 1.0, 'loadout': ['VULCAN', 'R-77', 'MK-82']},
    'F-35 Lightning':{'hp': 90, 'speed': 6, 'prefix': 'f35',    'scale': 0.9, 'loadout': ['VULCAN', 'AIM-120', 'GBU-12']},
    'F-22 Raptor':  {'hp': 100, 'speed': 6.5,'prefix': 'f22',   'scale': 1.0, 'loadout': ['VULCAN', 'AIM-9X', 'GBU-39']},
    'Rafale':       {'hp': 95,  'speed': 6.2,'prefix': 'rafale', 'scale': 0.9, 'loadout': ['VULCAN', 'MICA', 'MK-82']},
    'B-2 Spirit':   {'hp': 200, 'speed': 4.0, 'prefix': 'b2',    'scale': 1.2, 'loadout': ['AGM-158', 'MOAB']}, 
    'B-52 Strato':  {'hp': 250, 'speed': 3.0, 'prefix': 'b52',   'scale': 1.3, 'loadout': ['AGM-86', 'MK-84']}
}

MISSILE_STATS = {
    'VULCAN':  {'type': 'GUN',     'vel': 25, 'color': (255, 200, 50),  'size': (4, 2),  'fins': 'NONE',   'dmg': 5},
    'METEOR':  {'type': 'MISSILE', 'vel': 22, 'color': (180, 180, 180), 'size': (14, 4), 'fins': 'INTAKE', 'dmg': 25},
    'AIM-120': {'type': 'MISSILE', 'vel': 20, 'color': (230, 230, 230), 'size': (12, 3), 'fins': 'NORMAL', 'dmg': 20},
    'R-77':    {'type': 'MISSILE', 'vel': 19, 'color': (200, 200, 200), 'size': (13, 4), 'fins': 'GRID',   'dmg': 25},
    'AIM-9X':  {'type': 'MISSILE', 'vel': 24, 'color': (50, 50, 50),    'size': (10, 3), 'fins': 'FRONT',  'dmg': 15},
    'MICA':    {'type': 'MISSILE', 'vel': 21, 'color': (220, 220, 255), 'size': (11, 3), 'fins': 'NORMAL', 'dmg': 20},
    'AGM-158': {'type': 'MISSILE', 'vel': 15, 'color': (80, 80, 80),    'size': (18, 6), 'fins': 'STEALTH','dmg': 80},
    'AGM-86':  {'type': 'MISSILE', 'vel': 14, 'color': (200, 200, 200), 'size': (20, 5), 'fins': 'WINGS',  'dmg': 90},
    'MK-82':   {'type': 'BOMB',    'vel': 12, 'color': (50, 60, 50),    'size': (10, 5), 'fins': 'BOMB',   'dmg': 60},
    'GBU-12':  {'type': 'BOMB',    'vel': 12, 'color': (60, 70, 60),    'size': (12, 5), 'fins': 'BOMB',   'dmg': 70},
    'GBU-39':  {'type': 'BOMB',    'vel': 13, 'color': (100, 100, 100), 'size': (8, 4),  'fins': 'WINGS',  'dmg': 50},
    'MK-84':   {'type': 'BOMB',    'vel': 10, 'color': (40, 50, 40),    'size': (16, 8), 'fins': 'BOMB',   'dmg': 120},
    'MOAB':    {'type': 'BOMB',    'vel': 8,  'color': (200, 100, 50),  'size': (25, 12),'fins': 'MOAB',   'dmg': 400} 
}
