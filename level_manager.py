import pygame
import random
from settings import *
from sprites import Enemy, GroundTarget

class LevelManager:
    def __init__(self, game):
        self.game = game
        self.timer = 0
        self.wait_time = 120
        self.available_planes = list(AIRCRAFT_DATA.keys())
        
        # --- SPAWN DE PRÉDIOS E RADARES ---
        # Como não temos um editor de mapa, vamos espalhar aleatoriamente
        self.spawn_ground_targets()

    def spawn_ground_targets(self):
        # 5 Radares
        for _ in range(5):
            x, y = random.randint(200, MAP_WIDTH-200), random.randint(200, MAP_HEIGHT-200)
            self.game.ground_targets.add(GroundTarget(x, y, 'RADAR'))
            
        # 8 Bunkers
        for _ in range(8):
            x, y = random.randint(200, MAP_WIDTH-200), random.randint(200, MAP_HEIGHT-200)
            self.game.ground_targets.add(GroundTarget(x, y, 'BUNKER'))
            
        # 4 Fábricas
        for _ in range(4):
            x, y = random.randint(200, MAP_WIDTH-200), random.randint(200, MAP_HEIGHT-200)
            self.game.ground_targets.add(GroundTarget(x, y, 'FACTORY'))
            
        # 2 Pontes (Simuladas)
        for _ in range(2):
            x, y = random.randint(200, MAP_WIDTH-200), random.randint(200, MAP_HEIGHT-200)
            self.game.ground_targets.add(GroundTarget(x, y, 'BRIDGE'))

    def update(self):
        self.timer += 1
        if self.timer >= self.wait_time:
            self.timer = 0
            self.spawn_enemy()
            self.wait_time = random.randint(120, 240)

    def spawn_enemy(self):
        enemy_model = random.choice(self.available_planes)
        while True:
            x = random.randint(100, MAP_WIDTH - 100)
            y = random.randint(100, MAP_HEIGHT - 100)
            dx = x - self.game.player.rect.centerx
            dy = y - self.game.player.rect.centery
            dist = (dx*dx + dy*dy)**0.5
            if dist > 600:
                break
        e = Enemy(x, y, enemy_model)
        self.game.enemies.add(e)
        self.game.all_sprites.add(e)
