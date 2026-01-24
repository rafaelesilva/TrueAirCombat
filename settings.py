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

# Aumentei um pouco o mapa para ter espaço de patrulha
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
# Cor do Radar (Preto transparente)
RADAR_BG = (0, 20, 0, 150) 
RADAR_BORDER = (0, 255, 0)

AIRCRAFT_DATA = {
    'Gripen F-39E': {'hp': 100, 'speed': 6, 'prefix': 'gripen', 'scale_factor': 0.9},
    'F-16 Viper':   {'hp': 80,  'speed': 7, 'prefix': 'f16',    'scale_factor': 0.9},
    'Su-35 Flanker':{'hp': 110, 'speed': 5.5,'prefix': 'su35',  'scale_factor': 1.0},
    'F-35 Lightning':{'hp': 90, 'speed': 6, 'prefix': 'f35',    'scale_factor': 0.9},
    'F-22 Raptor':  {'hp': 100, 'speed': 6.5,'prefix': 'f22',   'scale_factor': 1.0},
    'Rafale':       {'hp': 95,  'speed': 6.2,'prefix': 'rafale', 'scale_factor': 0.9}
}
