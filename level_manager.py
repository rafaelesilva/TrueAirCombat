import pygame
import random
from settings import *
from sprites import Enemy

class LevelManager:
    def __init__(self, game):
        self.game = game
        self.timer = 0
        self.wave_interval = 120 # frames
        # Lista com todos os nomes de aviões disponíveis
        self.available_planes = list(AIRCRAFT_DATA.keys())
        
    def update(self):
        self.timer += 1
        if self.timer >= self.wave_interval:
            self.timer = 0
            self.spawn_wave()

    def spawn_wave(self):
        # Escolhe um padrão de ataque
        wave_type = random.choice(['V_FORMATION', 'LINE', 'SOLO_ACE'])
        
        # Escolhe UM modelo de avião para ser o inimigo desta onda
        enemy_model = random.choice(self.available_planes)
        
        if wave_type == 'V_FORMATION':
            center_x = random.randint(100, WIDTH-100)
            for i in range(3):
                # 3 Aviões em formação V
                x_offset = (i * 60) * SCALE
                y_offset = (abs(1-i) * 50) * SCALE
                
                e = Enemy(center_x + (i-1)*60*SCALE, -50 - y_offset, enemy_model)
                self.game.enemies.add(e)
                self.game.all_sprites.add(e)
                
        elif wave_type == 'LINE':
            y_start = -50
            # 4 Aviões descendo em fila, cada um pode ser de um modelo diferente ou todos iguais
            # Aqui vamos variar para ficar divertido:
            for i in range(4):
                model = random.choice(self.available_planes)
                e = Enemy(random.randint(50, WIDTH-50), y_start - (i*100), model)
                self.game.enemies.add(e)
                self.game.all_sprites.add(e)
                
        elif wave_type == 'SOLO_ACE':
            # Um único inimigo, talvez mais forte (você pode ajustar HP depois)
            x_pos = random.randint(50, WIDTH-50)
            e = Enemy(x_pos, -50, enemy_model)
            # Damos um pouco mais de HP para o "Líder"
            e.hp *= 1.5
            self.game.enemies.add(e)
            self.game.all_sprites.add(e)
