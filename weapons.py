import pygame
import math
import random
from settings import *

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, color, size, lifetime):
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size//2, size//2), size//2)
        self.rect = self.image.get_rect(center=pos)
        self.lifetime = lifetime
        self.original_life = lifetime
        
    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
        else:
            alpha = int((self.lifetime / self.original_life) * 255)
            self.image.set_alpha(alpha)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, missile_type, owner_type="PLAYER"):
        super().__init__()
        self.type = missile_type
        self.owner = owner_type 
        self.stats = MISSILE_STATS.get(missile_type, MISSILE_STATS['VULCAN'])
        
        self.speed = self.stats['vel']
        self.color = self.stats['color']
        self.damage = self.stats.get('dmg', 10)
        self.category = self.stats.get('type', 'MISSILE') # MISSILE, BOMB ou GUN
        self.angle = angle
        
        # --- TIMER DA BOMBA (Impacto no solo) ---
        # Se for bomba, ela tem um tempo de vida curto (cair) e depois explode sozinha
        self.timer = 40 if self.category == 'BOMB' else 200 # 40 frames (~1.3 segs) para cair
        self.should_explode = False # Flag para o main.py saber que bateu no chão
        
        length, width = self.stats['size']
        self.original_image = pygame.Surface((length + 6, width + 6), pygame.SRCALPHA)
        cy = (width + 6) // 2
        
        if self.type == 'VULCAN':
            pygame.draw.circle(self.original_image, self.color, (2, cy), 2)
        else:
            fins = self.stats['fins']
            if fins == 'BOMB' or fins == 'MOAB':
                # Desenho Gordinho da Bomba
                rect_bomb = pygame.Rect(0, cy - width//2, length, width)
                pygame.draw.ellipse(self.original_image, self.color, rect_bomb)
                pygame.draw.line(self.original_image, (255, 255, 0), (length-4, cy - width//2 + 2), (length-4, cy + width//2 - 2), 2)
                pygame.draw.rect(self.original_image, (20, 20, 20), (0, cy - width//2 - 2, 4, width + 4))
            else:
                # Desenho Fino de Míssil
                pygame.draw.rect(self.original_image, self.color, (0, cy - width//2, length, width))
                pygame.draw.polygon(self.original_image, (50, 50, 50), [(length, cy - width//2), (length + 4, cy), (length, cy + width//2)])
                fin_c = (80, 80, 80)
                if fins == 'INTAKE': pygame.draw.rect(self.original_image, (30,30,30), (length//2, cy - width - 1, 4, width + 2))
                elif fins == 'GRID': pygame.draw.line(self.original_image, fin_c, (2, cy - width), (2, cy + width), 2)
                else: pygame.draw.polygon(self.original_image, fin_c, [(0, cy), (4, cy - width - 2), (4, cy + width + 2)])

        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=(x, y))
        
        rad = math.radians(angle)
        self.vx = math.cos(rad) * self.speed
        self.vy = -math.sin(rad) * self.speed 
        self.pos_x, self.pos_y = float(x), float(y)
        
        # Bombas desaceleram (arrasto do ar)
        self.drag = 0.96 if self.category == 'BOMB' else 1.0

    def update(self):
        self.pos_x += self.vx
        self.pos_y += self.vy
        
        # Lógica Específica de Bomba
        if self.category == 'BOMB':
            self.vx *= self.drag
            self.vy *= self.drag
            self.timer -= 1
            if self.timer <= 0:
                self.should_explode = True # Ativa a detonação no chão
        
        self.rect.centerx = int(self.pos_x)
        self.rect.centery = int(self.pos_y)
        
        if (self.rect.x < -100 or self.rect.x > MAP_WIDTH + 100 or
            self.rect.y < -100 or self.rect.y > MAP_HEIGHT + 100):
            self.kill()

class WeaponSystem:
    def __init__(self, missile_type='AIM-120'):
        self.primary = 'VULCAN'
        self.secondary = missile_type
        self.current = self.primary

    def switch(self):
        if self.current == self.primary: self.current = self.secondary
        else: self.current = self.primary
            
    def get_current(self):
        return self.current
