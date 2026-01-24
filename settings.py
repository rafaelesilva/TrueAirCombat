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

# --- AERONAVES E ARMAMENTOS ---
# Nota: Para caças, mantivemos mísseis pois são melhores para Dogfight (Combate Aéreo).
# Para Bombardeiros, colocamos as Bombas Pesadas.
AIRCRAFT_DATA = {
    'Gripen F-39E': {'hp': 100, 'speed': 6, 'prefix': 'gripen', 'scale': 0.9, 'missile': 'METEOR'},
    'F-16 Viper':   {'hp': 80,  'speed': 7, 'prefix': 'f16',    'scale': 0.9, 'missile': 'AIM-120'},
    'Su-35 Flanker':{'hp': 110, 'speed': 5.5,'prefix': 'su35',  'scale': 1.0, 'missile': 'R-77'},
    'F-35 Lightning':{'hp': 90, 'speed': 6, 'prefix': 'f35',    'scale': 0.9, 'missile': 'MK-84'}, # F-35 tmb bombardea
    'F-22 Raptor':  {'hp': 100, 'speed': 6.5,'prefix': 'f22',   'scale': 1.0, 'missile': 'AIM-9X'},
    'Rafale':       {'hp': 95,  'speed': 6.2,'prefix': 'rafale', 'scale': 0.9, 'missile': 'MICA'},
    
    # BOMBARDEIROS REAIS = BOMBAS REAIS
    'B-2 Spirit':   {'hp': 200, 'speed': 4.0, 'prefix': 'b2',    'scale': 1.2, 'missile': 'MOAB'}, # GBU-43 Massive
    'B-52 Strato':  {'hp': 250, 'speed': 3.0, 'prefix': 'b52',   'scale': 1.3, 'missile': 'MK-84'}  # Carpet Bombing
}

# --- CONFIGURAÇÃO VISUAL DAS ARMAS ---
# type: 'MISSILE' (tem motor/fumaça) ou 'BOMB' (cai/sem fumaça)
MISSILE_STATS = {
    # MÍSSEIS AR-AR (Rápidos, rastro de fumaça, dano médio)
    'METEOR':  {'type': 'MISSILE', 'vel': 22, 'color': (180, 180, 180), 'size': (14, 4), 'fins': 'INTAKE', 'dmg': 20},
    'AIM-120': {'type': 'MISSILE', 'vel': 20, 'color': (230, 230, 230), 'size': (12, 3), 'fins': 'NORMAL', 'dmg': 20},
    'R-77':    {'type': 'MISSILE', 'vel': 19, 'color': (200, 200, 200), 'size': (13, 4), 'fins': 'GRID',   'dmg': 25},
    'AIM-9X':  {'type': 'MISSILE', 'vel': 24, 'color': (50, 50, 50),    'size': (10, 3), 'fins': 'FRONT',  'dmg': 15},
    'MICA':    {'type': 'MISSILE', 'vel': 21, 'color': (220, 220, 255), 'size': (11, 3), 'fins': 'NORMAL', 'dmg': 20},
    'VULCAN':  {'type': 'GUN',     'vel': 25, 'color': (255, 200, 50),  'size': (4, 2),  'fins': 'NONE',   'dmg': 5},
    
    # BOMBAS (Lentas, caem, explodem MUITO forte)
    'MK-84':   {'type': 'BOMB',    'vel': 12, 'color': (40, 50, 40),    'size': (16, 8), 'fins': 'BOMB',   'dmg': 100}, # Bomba Verde Oliva
    'MOAB':    {'type': 'BOMB',    'vel': 10, 'color': (200, 100, 50),  'size': (25, 12),'fins': 'MOAB',   'dmg': 300}  # Bomba Gigante Laranja
}
