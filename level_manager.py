import pygame
import random
from settings import *
from sprites import Enemy

class LevelManager:
    def __init__(self, game):
        self.game = game
        self.timer = 0
        self.wait_time = 120 # Tempo entre spawns
        self.available_planes = list(AIRCRAFT_DATA.keys())
        
    def update(self):
        # Simples: cria um inimigo a cada X tempo
        self.timer += 1
        if self.timer >= self.wait_time:
            self.timer = 0
            self.spawn_enemy()
            # Próximo tempo de espera aleatório
            self.wait_time = random.randint(60, 180)

    def spawn_enemy(self):
        enemy_model = random.choice(self.available_planes)
        
        # Nasce em um lugar aleatório do mapa, mas não muito perto do jogador
        while True:
            x = random.randint(100, MAP_WIDTH - 100)
            y = random.randint(100, MAP_HEIGHT - 100)
            
            # Verifica distância do jogador (pitágoras simples)
            dx = x - self.game.player.rect.centerx
            dy = y - self.game.player.rect.centery
            dist = (dx*dx + dy*dy)**0.5
            
            if dist > 400: # Só nasce se estiver longe (400px)
                break
                
        e = Enemy(x, y, enemy_model)
        self.game.enemies.add(e)
        self.game.all_sprites.add(e)
