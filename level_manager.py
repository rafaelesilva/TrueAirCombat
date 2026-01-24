import pygame
import random
from settings import *
from sprites import Enemy

class LevelManager:
    def __init__(self, game):
        self.game = game
        self.timer = 0
        self.state = 'WAITING' # WAITING ou SPAWNING
        
        # Tempo entre ondas (aumente para "espalhar" mais)
        self.wait_time = 180 # 180 frames = 3 segundos de silêncio
        self.spawn_interval = 0
        
        self.available_planes = list(AIRCRAFT_DATA.keys())
        
    def update(self):
        self.timer += 1
        
        if self.state == 'WAITING':
            # Se passou o tempo de espera, começa uma nova onda
            if self.timer >= self.wait_time:
                self.timer = 0
                self.start_new_wave()
                
        elif self.state == 'SPAWNING':
            # Se já criou os inimigos, volta a esperar
            if self.timer > 60: # Dá um tempinho e reseta
                self.state = 'WAITING'
                self.timer = 0
                # Define um tempo aleatório para a próxima pausa (2 a 5 segundos)
                self.wait_time = random.randint(120, 300)

    def start_new_wave(self):
        self.state = 'SPAWNING'
        
        # Sorteia: Vai vir um sozinho ou um grupo?
        # 60% de chance de vir sozinho (mais calmo), 40% de grupo
        wave_type = random.choice(['LONE_WOLF', 'LONE_WOLF', 'LONE_WOLF', 'SQUADRON', 'V_FORMATION'])
        enemy_model = random.choice(self.available_planes)
        
        if wave_type == 'LONE_WOLF':
            # UM DE CADA VEZ
            x_pos = random.randint(50, WIDTH-50)
            e = Enemy(x_pos, -60, enemy_model)
            self.game.enemies.add(e)
            self.game.all_sprites.add(e)
            
        elif wave_type == 'SQUADRON':
            # VÁRIOS JUNTOS (Linha ou aleatório)
            for i in range(3):
                offset = random.randint(-100, 100)
                e = Enemy(random.randint(50, WIDTH-50), -60 - (i*80), enemy_model)
                self.game.enemies.add(e)
                self.game.all_sprites.add(e)
                
        elif wave_type == 'V_FORMATION':
            # TRIO ORGANIZADO
            center_x = random.randint(100, WIDTH-100)
            for i in range(3):
                x_off = (i-1) * 60 * SCALE
                y_off = abs(i-1) * 40 * SCALE
                e = Enemy(center_x + x_off, -60 - y_off, enemy_model)
                self.game.enemies.add(e)
                self.game.all_sprites.add(e)
