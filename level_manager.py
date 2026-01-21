import pygame
import random
from settings import *
from sprites import Enemy

class LevelManager:
    def __init__(self, game):
        self.game = game
        self.timer = 0
        self.wave_interval = 120 # frames
        
    def update(self):
        self.timer += 1
        if self.timer >= self.wave_interval:
            self.timer = 0
            self.spawn_wave()

    def spawn_wave(self):
        wave_type = random.choice(['V_FORMATION', 'LINE', 'TANK_SQUAD'])
        
        if wave_type == 'V_FORMATION':
            center_x = random.randint(100, WIDTH-100)
            for i in range(3):
                # 3 Jatos em V
                x_offset = (i * 60) * SCALE
                y_offset = (abs(1-i) * 50) * SCALE
                e = Enemy(center_x + (i-1)*60*SCALE, -50 - y_offset, "JET")
                self.game.enemies.add(e)
                self.game.all_sprites.add(e)
                
        elif wave_type == 'LINE':
            y_start = -50
            for i in range(4):
                e = Enemy(random.randint(50, WIDTH-50), y_start - (i*100), "HELICOPTER")
                self.game.enemies.add(e)
                self.game.all_sprites.add(e)
                
        elif wave_type == 'TANK_SQUAD':
            x_pos = random.randint(50, WIDTH-50)
            e = Enemy(x_pos, -50, "TANK")
            self.game.enemies.add(e)
            self.game.all_sprites.add(e)
