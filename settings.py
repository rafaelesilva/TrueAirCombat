import pygame

# Inicializa para detectar tela
pygame.init()
info = pygame.display.Info()

# --- FORÇAR MODO PAISAGEM (LANDSCAPE) ---
# Se a largura for menor que a altura, invertemos os valores.
# Assim, o jogo sempre "pensa" que está deitado.
if info.current_w < info.current_h:
    WIDTH = info.current_h
    HEIGHT = info.current_w
else:
    WIDTH = info.current_w
    HEIGHT = info.current_h

# --- Título e Performance ---
TITLE = "Air Combat 2026"
FPS = 60

# --- CÁLCULO DE ESCALA (ZOOM) ---
# No modo paisagem, usamos a ALTURA como referência para não ficar muito zoom.
# Base de referência: 480px de altura (celulares antigos)
TARGET_BASE_HEIGHT = 480
SCALE = HEIGHT / TARGET_BASE_HEIGHT

# Limita o zoom máximo para não ficar gigante em tablets
if SCALE > 2.0: SCALE = 2.0

SCROLL_SPEED = int(3 * SCALE)
if SCROLL_SPEED < 1: SCROLL_SPEED = 1

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
YELLOW = (255, 215, 0)

# --- DATABASE DAS AERONAVES ---
AIRCRAFT_DATA = {
    'Gripen F-39E': {'hp': 100, 'speed': 6, 'prefix': 'gripen', 'scale_factor': 1.0},
    'F-16 Viper':   {'hp': 80,  'speed': 7, 'prefix': 'f16',    'scale_factor': 1.0},
    'Su-35 Flanker':{'hp': 110, 'speed': 5.5,'prefix': 'su35',  'scale_factor': 1.1},
    'F-35 Lightning':{'hp': 90, 'speed': 6, 'prefix': 'f35',    'scale_factor': 1.0},
    'F-22 Raptor':  {'hp': 100, 'speed': 6.5,'prefix': 'f22',   'scale_factor': 1.1},
    'Rafale':       {'hp': 95,  'speed': 6.2,'prefix': 'rafale', 'scale_factor': 1.0},
    'B-2 Spirit':   {'hp': 150, 'speed': 4,  'prefix': 'b2',     'scale_factor': 1.3},
    'B-52 Stratofortress':{'hp': 200, 'speed': 3, 'prefix': 'b52', 'scale_factor': 1.4}
}
