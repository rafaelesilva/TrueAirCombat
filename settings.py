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

# Cores
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

# --- AERONAVES E SEUS MÍSSEIS REAIS ---
AIRCRAFT_DATA = {
    'Gripen F-39E': {
        'hp': 100, 'speed': 6, 'prefix': 'gripen', 'scale': 0.9, 
        'missile': 'METEOR' # O melhor míssil além do alcance visual
    },
    'F-16 Viper': {
        'hp': 80,  'speed': 7, 'prefix': 'f16', 'scale': 0.9,
        'missile': 'AIM-120' # O clássico AMRAAM americano
    },
    'Su-35 Flanker': {
        'hp': 110, 'speed': 5.5,'prefix': 'su35', 'scale': 1.0,
        'missile': 'R-77' # O "Viper" russo com aletas de grade
    },
    'F-35 Lightning': {
        'hp': 90, 'speed': 6, 'prefix': 'f35', 'scale': 0.9,
        'missile': 'AIM-120'
    },
    'F-22 Raptor': {
        'hp': 100, 'speed': 6.5,'prefix': 'f22', 'scale': 1.0,
        'missile': 'AIM-9X' # Sidewinder super manobrável
    },
    'Rafale': {
        'hp': 95,  'speed': 6.2,'prefix': 'rafale', 'scale': 0.9,
        'missile': 'MICA' # Míssil francês versátil
    }
}

# --- CONFIGURAÇÃO VISUAL DOS MÍSSEIS ---
# velocity: velocidade do projetil
# color: cor do corpo principal
# size: (comprimento, largura)
MISSILE_STATS = {
    'METEOR':  {'vel': 22, 'color': (180, 180, 180), 'size': (14, 4), 'fins': 'INTAKE'}, # Cinza, com entradas de ar
    'AIM-120': {'vel': 20, 'color': (230, 230, 230), 'size': (12, 3), 'fins': 'NORMAL'}, # Branco
    'R-77':    {'vel': 19, 'color': (200, 200, 200), 'size': (13, 4), 'fins': 'GRID'},   # Aletas de grade
    'AIM-9X':  {'vel': 24, 'color': (50, 50, 50),    'size': (10, 3), 'fins': 'FRONT'},  # Preto/Escuro
    'MICA':    {'vel': 21, 'color': (220, 220, 255), 'size': (11, 3), 'fins': 'NORMAL'}, # Azulado
    'VULCAN':  {'vel': 25, 'color': (255, 200, 50),  'size': (4, 2),  'fins': 'NONE'}    # Tiro de canhão (amarelo)
}
