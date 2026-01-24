import pygame

pygame.init()
info = pygame.display.Info()

# --- 1. TELA REAL ---
if info.current_w < info.current_h:
    REAL_WIDTH = info.current_h
    REAL_HEIGHT = info.current_w
else:
    REAL_WIDTH = info.current_w
    REAL_HEIGHT = info.current_h

# --- 2. TELA VIRTUAL ---
WIDTH = 640
HEIGHT = 360

TITLE = "Air Combat 2026"
FPS = 30
SCALE = 1.0 
SCROLL_SPEED = 2 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)
CYAN = (0, 255, 255)

# Removi B-2 e B-52 para não dar erro de imagem (quadrado vermelho)
AIRCRAFT_DATA = {
    'Gripen F-39E': {'hp': 100, 'speed': 5, 'prefix': 'gripen', 'scale_factor': 0.9},
    'F-16 Viper':   {'hp': 80,  'speed': 6, 'prefix': 'f16',    'scale_factor': 0.9},
    'Su-35 Flanker':{'hp': 110, 'speed': 4.5,'prefix': 'su35',  'scale_factor': 1.0},
    'F-35 Lightning':{'hp': 90, 'speed': 5, 'prefix': 'f35',    'scale_factor': 0.9},
    'F-22 Raptor':  {'hp': 100, 'speed': 5.5,'prefix': 'f22',   'scale_factor': 1.0},
    'Rafale':       {'hp': 95,  'speed': 5.2,'prefix': 'rafale', 'scale_factor': 0.9}
}
