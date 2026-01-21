import pygame
from settings import *

class WeaponSystem:
    def __init__(self):
        self.types = ["VULCAN", "MISSILE", "BOMB"]
        self.current_idx = 0
    
    def switch(self):
        self.current_idx = (self.current_idx + 1) % len(self.types)
        return self.types[self.current_idx]
    
    def get_current(self):
        return self.types[self.current_idx]

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, p_type, is_enemy=False):
        super().__init__()
        self.type = p_type
        self.is_enemy = is_enemy
        
        # Configuração visual baseada no tipo
        if self.type == "VULCAN":
            w, h = int(5*SCALE), int(15*SCALE)
            self.image = pygame.Surface((w, h))
            self.image.fill((255, 255, 0) if not is_enemy else (255, 100, 100))
            self.speed = 15 * SCALE
            self.damage = 10
            
        elif self.type == "MISSILE":
            w, h = int(10*SCALE), int(30*SCALE)
            self.image = pygame.Surface((w, h))
            self.image.fill((200, 200, 255))
            pygame.draw.rect(self.image, (0,0,255), (0,0,w,int(5*SCALE))) # Ponta azul
            self.speed = 10 * SCALE
            self.damage = 50
            
        elif self.type == "BOMB":
            w, h = int(40*SCALE), int(40*SCALE)
            self.image = pygame.Surface((w, h))
            self.image.fill((255, 0, 0))
            self.speed = 5 * SCALE
            self.damage = 500 # Dano em área (simulado)

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        
        if is_enemy:
            self.rect.top = y
            self.direction = 1 # Desce
        else:
            self.rect.bottom = y
            self.direction = -1 # Sobe

    def update(self):
        self.rect.y += self.speed * self.direction
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
